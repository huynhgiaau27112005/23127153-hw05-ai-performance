# AI Audit Report — HW05 Performance Testing

**Student:** Huỳnh Gia Âu | **MSSV:** 23127153  
**Declaration:** I use AI tools for the tasks below.

---

### Interaction 1

| Field | Content |
|-------|---------|
| **Tool** | Cursor Agent |
| **Date** | 2026-08-30T23:00+07:00 |
| **Prompt** | Restate HW05 deliverables for EShop API perf testing: JMeter Load/Stress/Spike, CSV, 3 listener types, endurance, Task 2 misinterpretation, Task 3 CI proposal. Student 23127153. |
| **Output** | Checklist of JMX naming, E2E flow, docs, video TODO. No scripts yet. |

### Interaction 2

| Field | Content |
|-------|---------|
| **Tool** | Cursor Agent |
| **Date** | 2026-08-30T23:30+07:00 |
| **Prompt** | Generate Python JMX builder for login→search→detail→cart→checkout with JSONPostProcessor for token and product id. Port 3010. |
| **Output** | `scripts/generate_jmx.py`, `data/users.csv`, four scenario configs. First version had invalid SummaryReport XML — fixed to ResultCollector. |

### Interaction 3

| Field | Content |
|-------|---------|
| **Tool** | Cursor Agent |
| **Date** | 2026-08-31T00:00+07:00 |
| **Prompt** | Run JMeter, fix XML parse errors, produce JTL/HTML. |
| **Output** | Fixed listeners; added `run_all.bat`, `reset-eshop-api.ps1`, `summarize_jtl.py`. Identified seed-before-run requirement. |

### Interaction 4

| Field | Content |
|-------|---------|
| **Tool** | Cursor Agent |
| **Date** | 2026-08-31T00:15+07:00 |
| **Prompt** | Write main report Task 2 table with deliberate AI mistakes corrected from JTL evidence. |
| **Output** | Section 6 in `docs/main-report.md` — four misinterpretation rows. |

---

**Human review:** Verify JTL numbers in `results/summary.json` match report tables before submission.
