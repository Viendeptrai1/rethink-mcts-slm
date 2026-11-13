# Đợt chạy v3.1 trên Colab (12–13/11/2026): công cụ chạy tiếp

Đây là các script dùng trong đợt chạy được ghi ở [BENCHMARK_LEDGER.md](../../../docs/results/BENCHMARK_LEDGER.md), mục 12. Đường dẫn trong script được viết cố định cho máy local.

- `plans/`: hàng đợi gửi lên VM. Mỗi model có bản gốc (`*_original.plan`) và bản đã đổi thứ tự. Với Qwen3.5, việc được chia thành hai phần không giao nhau: `qwen35.plan` (Best-of-16 APPS, Direct APPS, HumanEval) và `qwen35b.plan` (chỉ MCTS APPS).
- `relaunch.sh <session> "<lý do>"`: cất log và bản lưu mới nhất vào `colab_results/<session>_lostN`, cho giải lại các bài vướng lỗi CRLF khi resume (`check_resume.py`), rồi chạy `orchestrate_ls.sh` với `SEED_RUNS` cùng `guard_dl.sh`.
- `tonight.sh`: chạy Qwen3.5 theo cặp A/B. Chỉ bật B khi một runtime đã sống quá 30 phút. Dừng hẳn sau 4 lần liên tiếp mất máy sớm, hoặc khi số dư dưới 15 CU.
- Code gửi lên VM là `colab_results/freeze/tlcn_v3.tar.gz`, tức `git archive` của commit `d9666c4` kèm file `GIT_COMMIT`; file này không nằm trong git. Có thể tạo lại bằng `git archive d9666c4` rồi thêm file `GIT_COMMIT`.
- Bản lưu Qwen3.5 mới nhất: `colab_results/qwen35/partial.tar.gz` (A: 68 bài Best-of-16, 113 bài MCTS) và `colab_results/qwen35b/partial.tar.gz` (B: 113 bài MCTS). Khi gộp kết quả, lấy Best-of-16, Direct và HumanEval từ A, lấy MCTS APPS từ B.
