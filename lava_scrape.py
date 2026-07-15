#!/usr/bin/env python3
"""Scrape live device data from the Foundries LAVA scheduler.

For each worker it fetches https://lava.infra.foundries.io/scheduler/worker/<name>
and parses the "Devices Attached" table plus the worker State/Health, producing a
data.json compatible with the dashboard.

Usage:  python3 lava_scrape.py ./out

worker-configs/ is discovered in this order:
  1. $WORKER_CONFIGS_DIR (if set)
  2. ./worker-configs next to this script
  3. ../lava-dispatcher-config/worker-configs (sibling checkout)
"""
import glob, html, json, os, re, sys, datetime, urllib.request

# Production LAVA instance and the lava-dispatcher-config branch that describes
# it. Worker names are read from that branch's worker-configs/ so the dashboard
# always tracks production regardless of which branch is checked out locally.
BASE = "https://lava.infra.foundries.io"
CONFIG_REF = os.environ.get("WORKER_CONFIGS_REF", "origin/production")
HERE = os.path.dirname(os.path.abspath(__file__))


def find_worker_configs():
    candidates = [
        os.environ.get("WORKER_CONFIGS_DIR"),
        os.path.join(HERE, "worker-configs"),
        os.path.join(os.path.dirname(HERE), "lava-dispatcher-config", "worker-configs"),
    ]
    for c in candidates:
        if c and os.path.isdir(c):
            return c
    raise SystemExit(
        "ERROR: could not find worker-configs/. Set WORKER_CONFIGS_DIR, or place a "
        "lava-dispatcher-config checkout next to this repo."
    )


ROOT = find_worker_configs()
# Repo root that owns worker-configs/ (parent of ROOT), used for git ls-tree.
ROOT_REPO = os.path.dirname(os.path.abspath(ROOT))
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lava-device-dashboard"

# Groups: which worker-name prefixes belong to which dashboard tab. All hyd
# groups are served by the production instance (BASE); a per-group "base" may
# still be supplied to override it.
GROUPS = {
    "hyd-workers": {"prefixes": ("hyd-worker",)},
    "ostt-hyd-workers": {"prefixes": ("ostt-lts-hyd",)},
}


def worker_names():
    """Worker directory names from the production branch of the config repo.

    Reads worker-configs/ from CONFIG_REF (default origin/production) so the
    dashboard tracks the production LAVA fleet regardless of the branch that
    happens to be checked out. Falls back to the working-tree directory if the
    ref/git is unavailable.
    """
    import subprocess

    try:
        out = subprocess.check_output(
            ["git", "-C", ROOT_REPO, "ls-tree", "--name-only", f"{CONFIG_REF}:worker-configs"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        names = {line.strip() for line in out.splitlines() if line.strip()}
        if names:
            return sorted(names)
    except Exception as e:  # noqa: BLE001
        print(f"WARN: falling back to working-tree worker-configs ({e})", file=sys.stderr)

    names = set()
    for p in glob.glob(f"{ROOT}/*/"):
        names.add(p.rstrip("/").split("/")[-1])
    return sorted(names)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "lava-dashboard-scraper"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def worker_num(name):
    m = re.search(r"(\d+)", name)
    return int(m.group(1)) if m else 9999


def parse_worker(page):
    """Return (state, health, [device dicts]) for a worker page."""
    state = health = ""
    m = re.search(r"<dt>State</dt>.*?<dd[^>]*>(.*?)</dd>", page, re.S)
    if m:
        state = clean(m.group(1))
    m = re.search(r"<dt>Health</dt>.*?<dd>(.*?)</dd>", page, re.S)
    if m:
        health = clean(m.group(1))

    devices = []
    # Only look inside the "Devices Attached" section, and stop before the
    # worker log/history table (its rows contain "lava-health").
    sect = page.split("Devices Attached", 1)
    body = sect[1] if len(sect) > 1 else page
    body = body.split("lava-health", 1)[0]

    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
        dm = re.search(r'/scheduler/device/([^"\']+)"[^>]*>([^<]+)</a>', row)
        if not dm:
            continue
        cells = [clean(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        dtype = ""
        tm = re.search(r"/scheduler/device_type/([^\"']+)", row)
        if tm:
            dtype = tm.group(1)
        d_state = cells[2] if len(cells) > 2 else ""
        d_health = cells[3] if len(cells) > 3 else ""
        devices.append({
            "device": dm.group(2).strip(),
            "type": dtype,
            "state": d_state,
            "health": d_health,
        })
    return state, health, devices


def collect(prefixes, base=BASE):
    rows = []
    for w in worker_names():
        if not any(w.startswith(p) for p in prefixes):
            continue
        url = f"{base}/scheduler/worker/{w}"
        try:
            page = fetch(url)
        except Exception as e:  # noqa: BLE001
            print(f"WARN {w}: {e}", file=sys.stderr)
            continue
        wstate, whealth, devices = parse_worker(page)
        print(f"{w}: state={wstate} health={whealth} devices={len(devices)}")
        for d in devices:
            rows.append({
                "worker": w,
                "worker_state": wstate,
                "worker_health": whealth,
                "device": d["device"],
                "type": d["type"],
                "state": d["state"],
                "health": d["health"],
            })
    return sorted(rows, key=lambda r: (worker_num(r["worker"]), r["device"]))


def summarize(rows):
    types, workers = {}, set()
    online = 0
    for r in rows:
        types[r["type"]] = types.get(r["type"], 0) + 1
        workers.add(r["worker"])
        if r["health"].lower().startswith("good"):
            online += 1
    return {
        "devices": len(rows),
        "workers": len(workers),
        "online": online,
        "types": dict(sorted(types.items(), key=lambda kv: (-kv[1], kv[0]))),
    }


def main():
    groups = {}
    bases = set()
    for gname, cfg in GROUPS.items():
        prefixes = cfg["prefixes"]
        base = cfg.get("base", BASE)
        bases.add(base)
        rows = collect(prefixes, base)
        groups[gname] = {"rows": rows, "summary": summarize(rows)}

    hosts = ", ".join(sorted(b.split("://", 1)[-1].rstrip("/") for b in bases))
    data = {
        "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source": f"live: {hosts}/scheduler/worker/<name>",
        "groups": groups,
    }

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "data.json"), "w") as f:
        json.dump(data, f, indent=2)

    with open(os.path.join(HERE, "dashboard_template.html")) as tf:
        tmpl = tf.read()
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(tmpl.replace("__DATA__", json.dumps(data)))

    for g in groups:
        print(g, groups[g]["summary"])
    print("Wrote", os.path.join(OUT, "data.json"), "and index.html")


if __name__ == "__main__":
    main()