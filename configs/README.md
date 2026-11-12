# Cấu hình

Nguồn sự thật cho mọi run là `runs/<run>/manifest.json` (trường `config`). Bảng dưới cho biết file YAML nào tái tạo đúng config đã chạy.

| Run (thư mục `runs/`) | File config | Ghi chú |
|---|---|---|
| `benchmark_14b_batch_*`, `last_one`, `retry_*` → `benchmark_apps_14b_dual_unified` | `benchmark_apps_14b_dual.yaml` (hoặc `batches/*.yaml`) | Trùng manifest, chỉ khác `model.base_url` |
| `benchmark_apps_14b_direct_300`, `benchmark_apps_14b_bon3_300` | `benchmark_apps_14b_direct.yaml` | Chạy với `--problem-ids`, nên `data.cohort_path` khác |
| `humaneval_mcts_dual_14b` | `extra_14b/humaneval_14b_base.yaml` | Chép từ manifest |
| Protocol v3 (nhiều model 7–9B, từ 11/2026) | `v3_7b/*.yaml` | Xem [v3_7b/README.md](v3_7b/README.md) |
| Các run bổ sung tháng 11/2026 (`*_norethink_q*`, `*_repair_q*`, `*_bon3_rest140`, `humaneval_*_14b_v2`) | `extra_14b/*.yaml` + override trong `scripts/launch_extra_14b.sh` | `budget.max_wall_seconds=3600`, `model.request_timeout_seconds=600` |

Không dùng để tái tạo kết quả:
- `benchmark_apps_14b.yaml`, `benchmark_apps_14b_test_only.yaml`, `benchmark_humaneval_14b.yaml`: cấu hình cũ (prompt `compact_v1`, Test-only, c=1.5). Vẫn được giữ vì `tests/acceptance/test_scenario_c.py` và một số tài liệu cũ tham chiếu.
- `smoke_mock.yaml`, `research_smoke.yaml`, `research_base.yaml`: smoke test và mock.
- `benchmark_apps_7b.yaml`, `benchmark_humaneval_7b.yaml`: chưa từng dùng cho kết quả 7B. Nhánh 7B chạy trong `external/ReThinkMCTS`.

Các trường config **không có tác dụng** (chỉ được ghi vào manifest, code không đọc), xác minh ngày 11/11/2026:
- `execution.per_test_timeout_seconds` và `execution.python_time_multiplier`: thời gian chờ thực tế lấy từ dữ liệu đã chuẩn bị, là **4 giây/test với APPS và 3 giây/test với HumanEval**.
- `execution.memory_mb`, `execution.stdout_limit_bytes`, `execution.network`: chỉ có ý nghĩa với Docker hoặc lấy từ dữ liệu.
- `model.max_format_retries`, `model.structured_output`, `model.context_window_tokens`, `model.concurrency`: không có vòng thử lại khi sai định dạng, và không kiểm tra độ dài ngữ cảnh.
- `reward.invalid_critic_policy`: critic lỗi thì nhận 0, không thử lại.
- `feedback.max_failed_tests`, `feedback.on_trace_failure`, `feedback.max_snapshot_depth`.
- `search.algorithm`, `search.selection`, `search.prior`, `search.leaf_revision_policy`, `experiment.*` (trừ `seed`, `stage`): chỉ là nhãn.
