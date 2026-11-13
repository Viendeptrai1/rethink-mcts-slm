# Cấu hình

Nguồn sự thật cho mọi run là `runs/<run>/manifest.json` (trường `config`).

| File | Dùng cho |
|---|---|
| `v3_7b/*.yaml` | Protocol v3.1: mọi run E1–E4 (`runs/v3_*`). Xem [v3_7b/README.md](v3_7b/README.md) |
| `smoke_mock.yaml` | Smoke test với model mock (không gọi mạng) |
| `research_smoke.yaml` | Smoke test benchmark trên fixture (`tests/fixtures/benchmark/`) |

Config của các protocol cũ (14B v1, batch 10 GPU, 7B) đã gỡ khỏi nhánh và lưu ở tag `archive/pre-v3-2026-11-13`.

Các trường config **không có tác dụng** (chỉ được ghi vào manifest, code không đọc), xác minh ngày 11/11/2026:
- `execution.per_test_timeout_seconds` và `execution.python_time_multiplier`: thời gian chờ thực tế lấy từ dữ liệu đã chuẩn bị, là **4 giây/test với APPS và 3 giây/test với HumanEval**.
- `execution.memory_mb`, `execution.stdout_limit_bytes`, `execution.network`: chỉ có ý nghĩa với Docker hoặc lấy từ dữ liệu.
- `model.max_format_retries`, `model.structured_output`, `model.context_window_tokens`, `model.concurrency`: không có vòng thử lại khi sai định dạng, và không kiểm tra độ dài ngữ cảnh.
- `reward.invalid_critic_policy`: critic lỗi thì nhận 0, không thử lại.
- `feedback.max_failed_tests`, `feedback.on_trace_failure`, `feedback.max_snapshot_depth`.
- `search.algorithm`, `search.selection`, `search.prior`, `search.leaf_revision_policy`, `experiment.*` (trừ `seed`, `stage`): chỉ là nhãn.
