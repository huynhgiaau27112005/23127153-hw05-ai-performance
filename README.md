# HW05 - AI Performance Testing (EShop)

**Student:** Huynh Gia Au  
**Student ID:** 23127153  
**SUT:** [https://github.com/ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut) API @ `http://127.0.0.1:3010`  
**GitHub (this homework):** [https://github.com/huynhgiaau27112005/23127153-hw05-ai-performance](https://github.com/huynhgiaau27112005/23127153-hw05-ai-performance)  
**Demo video:** STUDENT-TODO / pending

## Structure

```
23127153_HW05_AI_Performance_100/
  data/users.csv              # CSV-driven perf accounts
  test-plans/*.jmx            # Load, Stress, Spike, Endurance
  results/*/                  # JTL + html-report per scenario
  scripts/                    # generate_jmx, seed, run_all, summarize
  k6/load.js                  # Optional k6 backup script
  docs/                       # Reports (main, audit, critique)
  skills/hw05-jmeter-perf/    # Agent Skill
```

## Run

```powershell
# From repo root - resets DB, starts API :3010, seeds users, runs JMeter
powershell -ExecutionPolicy Bypass -File scripts/run_all.ps1
python scripts/summarize_jtl.py
```

JMeter binary: `../tools/apache-jmeter-5.6.3/bin/jmeter.bat`

## Scenarios

| Type | Plan | Purpose |
|------|------|---------|
| Load | `23127153_Load_20260830.jmx` | Steady 15 users, 6 loops |
| Stress | `23127153_Stress_20260830.jmx` | 35 users ramp |
| Spike | `23127153_Spike_20260830.jmx` | 50 users, 5s ramp |
| Endurance | `23127153_Endurance_20260830.jmx` | 10 users, 600s soak |

## Docs

- `docs/main-report.md` - analysis + Task 2 misinterpretation hunt + Task 3 CI proposal
- `docs/ai-audit.md` - AI interaction log
- `docs/ai-critique.md` - reflection
- `Demo_Recording_Script.md` - video outline (Vietnamese)

**Declaration:** AI-assisted; see `docs/ai-audit.md`.
