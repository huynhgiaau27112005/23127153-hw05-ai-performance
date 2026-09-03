# AI Critique — HW05

**Student:** Huỳnh Gia Âu | **MSSV:** 23127153

## What AI did well

- Generated repeatable JMX structure and CSV data faster than manual GUI recording.
- Mapped E2E API flow consistently with HW04 automation scope.
- Produced Task 2 misinterpretation examples tied to real JTL fields (`success`, response codes).

## What I corrected

- Listener XML must use `ResultCollector` with `guiclass`, not custom element names — JMeter 5.6 rejected the first plans.
- Perf users must be registered **before** load tests; otherwise AI blamed "server crash" for 401 errors.
- PowerShell `$ErrorActionPreference = Stop` treated JMeter stderr warnings as fatal — switched to `run_all.bat` / `rerun_clean.py`.
- `LoopController.loops` must be `intProp` (not `stringProp`); string form made Load run indefinitely (~19k samples instead of 450).

## Limits

- AI cannot capture Task Manager / dxdiag screenshots — human only.
- AI initial endurance analysis ignored in-memory cart growth in `server.js`; I added monitor note in Task 2 row 4.

## Personal reflection

Khi dùng AI cho performance testing, mình học được rằng **không được tin summary report hay giải thích của AI nếu chưa đối chiếu số mẫu với cấu hình thread × loop**. Lần đầu Load “chạy mãi” vì property loops sai kiểu XML — AI vẫn báo “đang chạy bình thường”. Bài học: luôn seed user trước khi load, xóa JTL cũ, và đọc `summary.json` / HTML dashboard trước khi viết kết luận bottleneck.
