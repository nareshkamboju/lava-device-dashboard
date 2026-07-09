#!/usr/bin/env python3
"""Generate the LAVA HYD device dashboard repo from ser2net.yaml configs."""
import glob, json, os, re, sys, datetime

ROOT = "worker-configs"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lava-device-dashboard"

# ---- device type classification ----
def classify(connection, banner, usb):
    c = connection.lower()
    b = (banner or "").lower()
    u = (usb or "").lower()
    text = " ".join([c, b, u])
    rules = [
        ("Shikra", ["shikra"]),
        ("Glymur", ["glymur"]),
        ("Kaanapali (MTP8850)", ["kaanapali", "mtp8850"]),
        ("Pakala (MTP)", ["pakala"]),
        ("Hamoa IOT EVK", ["hamoa"]),
        ("RB3 Gen2 (Kona)", ["rb3g2", "rb3 gen2", "kona"]),
        ("RB4", ["rb4"]),
        ("RB8 / IQ-9075 EVK", ["rb8", "iq-9075", "9075-evk"]),
        ("QCS8300 RIDE", ["qcs8300", "8300"]),
        ("QCS615 ADP", ["qcs615", "615"]),
        ("LeMans RIDE", ["lemans"]),
        ("UNOQ", ["unoq", "bughopper"]),
    ]
    for name, keys in rules:
        for k in keys:
            if k in text:
                return name
    return "Other"

def parse_ser2net(path):
    entries = []
    cur = None
    with open(path) as f:
        for raw in f:
            s = raw.strip()
            m = re.match(r"connection:\s*&(\S+)", s)
            if m:
                if cur: entries.append(cur)
                cur = {"connection": m.group(1), "port": "", "usb": "", "banner": ""}
                continue
            if cur is None:
                continue
            m = re.match(r"accepter:\s*telnet\(rfc2217\),tcp,(\d+)", s)
            if m:
                cur["port"] = m.group(1); continue
            m = re.match(r"/dev/serial/by-id/(\S+?),?$", s)
            if m:
                cur["usb"] = m.group(1); continue
            m = re.match(r"banner:\s*(.+)", s)
            if m:
                b = m.group(1).replace("\\r", "").replace("\\n", " ").strip()
                cur["banner"] = re.sub(r"\s+", " ", b); continue
        if cur: entries.append(cur)
    return entries

def worker_num(name):
    m = re.search(r"(\d+)$", name)
    return int(m.group(1)) if m else 9999

def collect(prefix):
    rows = []
    paths = sorted(glob.glob(f"{ROOT}/{prefix}-*/ser2net.yaml"),
                   key=lambda p: worker_num(p.split("/")[1]))
    for p in paths:
        worker = p.split("/")[1]
        for e in parse_ser2net(p):
            rows.append({
                "worker": worker,
                "device": e["connection"],
                "banner": e["banner"],
                "port": e["port"],
                "usb": e["usb"],
                "type": classify(e["connection"], e["banner"], e["usb"]),
            })
    return rows

hyd = collect("hyd-worker")
ostt = collect("ostt-lts-hyd")

def summarize(rows):
    types = {}
    workers = set()
    for r in rows:
        types[r["type"]] = types.get(r["type"], 0) + 1
        workers.add(r["worker"])
    return {
        "devices": len(rows),
        "workers": len(workers),
        "types": dict(sorted(types.items(), key=lambda kv: (-kv[1], kv[0]))),
    }

data = {
    "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    "source": "qualcomm-linux/lava-dispatcher-config @ shikra-FTDI-update",
    "groups": {
        "hyd-workers": {"rows": hyd, "summary": summarize(hyd)},
        "ostt-hyd-workers": {"rows": ostt, "summary": summarize(ostt)},
    },
}

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "data.json"), "w") as f:
    json.dump(data, f, indent=2)

# ---- build self-contained index.html ----
DATA_JS = json.dumps(data)
with open("dashboard_template.html") as _tf:
    HTML_TEMPLATE = _tf.read()
html = HTML_TEMPLATE.replace("__DATA__", DATA_JS)
with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(html)

print("HYD:", data["groups"]["hyd-workers"]["summary"])
print("OSTT:", data["groups"]["ostt-hyd-workers"]["summary"])
print("Wrote", os.path.join(OUT, "data.json"), "and index.html")