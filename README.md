# LAVA HYD Lab — Device Dashboard

A colorful, manager-friendly dashboard summarizing the devices attached to the
Hyderabad (HYD) LAVA workers. It answers at a glance: **how many devices, what
types, and how they are distributed across workers.**

Data is scraped live from the Foundries LAVA scheduler
(`https://lava.infra.foundries.io/scheduler/worker/<name>`) — each worker's
"Devices Attached" table plus its State/Health.

## View the dashboard

- Open `index.html` in any browser (it is fully self-contained), **or**
- Enable **GitHub Pages** (Settings → Pages → deploy from `main` / root) and
  browse to the published URL.

## What it shows

- **KPI cards** — device count, worker count, distinct device types, and lab totals.
- **Devices by Type** — doughnut chart with a color legend.
- **Devices per Worker** — bar chart of load per worker.
- **Searchable / sortable table** — filter by worker, device, type, state, or health.
- **Two groups** — switch between `hyd-workers` and `ostt-hyd-workers` tabs.

## Snapshot

| Group | Devices | Workers | Distinct Types |
| --- | --- | --- | --- |
| hyd-workers | 34 | 23 | 11 |
| ostt-hyd-workers | 18 | 10 | 8 |

Top device types (hyd-workers): QCS8300 RIDE (5), Kaanapali MTP8850 (4),
RB8 / IQ-9075 EVK (4), Shikra (4), Glymur (3), Hamoa IOT EVK (3), Pakala (3), RB4 (3).

## Files

- `index.html` — the standalone dashboard (Chart.js via CDN).
- `data.json` — structured device data + per-group summaries.
- `hyd-workers.md`, `ostt-hyd-workers.md` — Markdown device tables.
- `lava_scrape.py` + `dashboard_template.html` — scrape LAVA and rebuild everything.
- `deploy.sh` — one command to scrape, rebuild, commit, and push.

## Regenerate

This repo is self-contained. It needs a `worker-configs/` directory (for the
list of worker names), discovered via, in order: `$WORKER_CONFIGS_DIR`, then
`./worker-configs` in this repo, then `../lava-dispatcher-config/worker-configs`.

```bash
./deploy.sh                 # scrape live data, rebuild, commit, push
python3 lava_scrape.py ./out   # or just regenerate locally
```

This fetches each worker page from LAVA and rebuilds `data.json` and `index.html`.
