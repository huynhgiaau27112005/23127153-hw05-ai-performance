---
name: hw05-jmeter-perf
description: Generate and run JMeter performance test plans (Load, Stress, Spike, Endurance) for EShop HW05. Use when building JMX files, CSV data, JTL/HTML reports, or analyzing performance results for student 23127153.
---

# HW05 JMeter Performance Testing

End-to-end API performance workflow for EShop homework.

## Prerequisites

- Java 17+ and Apache JMeter 5.6.3 (`tools/apache-jmeter-5.6.3`)
- EShop API on `http://127.0.0.1:3010`
- Python 3 for `scripts/generate_jmx.py`, `seed_users.py`, `summarize_jtl.py`

## Quick Start

```powershell
# Reset API + seed perf users + run all scenarios
powershell -ExecutionPolicy Bypass -File scripts/run_all.ps1

# Regenerate JMX only
python scripts/generate_jmx.py

# Summarize JTL metrics
python scripts/summarize_jtl.py
```

## Test Plans

| Scenario | JMX | Threads | Listener |
|----------|-----|---------|----------|
| Load | `23127153_Load_20260830.jmx` | 15 | Summary Report |
| Stress | `23127153_Stress_20260830.jmx` | 35 | Aggregate Report |
| Spike | `23127153_Spike_20260830.jmx` | 50 | View Results Tree |
| Endurance | `23127153_Endurance_20260830.jmx` | 10 / 600s | Summary Report |

E2E flow per iteration: Login → Search products → Product detail → Add cart → Checkout.

CSV: `data/users.csv` (15 perf users, `Perf1234!`).

## Outputs

- Raw JTL: `results/{scenario}/23127153_{Scenario}_20260830.jtl`
- HTML dashboard: `results/{scenario}/html-report/`
- Summary JSON: `results/summary.json`

## Human TODO

- Task Manager / dxdiag hardware screenshots during Stress run
- Demo video ≥6 min (Vietnamese narration)
- Personalize AI critique reflection sections
