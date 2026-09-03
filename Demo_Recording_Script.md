# Demo Recording Script — HW05 (≥ 6 phút, tiếng Việt)

**Sinh viên:** Huỳnh Gia Âu — 23127153

## 0:00–0:45 — Giới thiệu
- Môn Kiểm thử phần mềm, HW05 Performance Testing, SUT EShop API port 3010.
- Công cụ: JMeter 5.6.3, CSV users, 4 kịch bản.

## 0:45–2:00 — Cấu trúc test plan
- Mở GUI JMeter hoặc file `23127153_Load_20260830.jmx`.
- Chỉ Thread Group, CSV Data Set, 5 HTTP sampler (login → checkout).
- Header `X-Student-Id: 23127153`.

## 2:00–3:30 — Chạy Load + xem report
- `scripts\run_all.bat` hoặc chỉ Load.
- Mở `results/load/html-report/index.html` — throughput, response time.
- Mở JTL trong text editor, lọc `success=false`.

## 3:30–4:30 — Stress + Task Manager
- Mở kết quả Stress/Aggregate Report.
- **Chụp Task Manager** CPU/RAM trong lúc Stress (bắt buộc bài tập).

## 4:30–5:30 — Spike & Endurance
- Spike: ramp 5s, 50 threads — giải thích spike latency.
- Endurance: 600s — nói về soak test, không memory leak chỉ từ JTL.

## 5:30–6:30 — Task 2 & kết luận
- Đọc 1 dòng AI hiểu sai (ví dụ “60% lỗi = server chết”) và cách sửa từ JTL.
- Task 3: CI chạy Load smoke mỗi push.
- Kết: bottleneck SQLite local, cần seed user trước test.

**Lưu ý:** Quay màn hình thật, giọng Việt rõ, ≥ 6 phút.
