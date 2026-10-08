# Trạng thái hiện tại — 08/10/2026

## Stable facts

- **Mốc nghiên cứu hiện tại:** Đã phân chia và thực thi thực nghiệm song song giữa 2 thành viên:
  - **Nhánh 7B (`Qwen2.5-Coder-7B-Instruct`):** Do HuyinCP thực hiện trên Modal GPU và CKEY. Toàn bộ tài liệu báo cáo và artifact đã được tích hợp vào [`docs/results/7b/`](../results/7b/).
  - **Nhánh 14B (`Qwen2.5-Coder-14B-Instruct`):** Do Kotori thực hiện trên TLCN với remote endpoint vLLM. Các run đã hoàn thành lưu tại [`runs/`](../../runs/).
- **Bộ dữ liệu chuẩn hóa:** Cả 2 nhánh dùng chung chính xác 100% tập **APPS 300** (`seed=2027`: 100 Intro, 100 Inter, 100 Comp theo [`data/cohorts/apps_benchmark_300.json`](../../data/cohorts/apps_benchmark_300.json)) và **HumanEval 164**.
- **Kết quả HumanEval (164/164 bài):**
  - 7B: Direct 80.49% $\to$ MCTS Test-only 89.63% $\to$ MCTS Dual 91.46%.
  - 14B: Direct 90.24% $\to$ BoN-3 91.46% $\to$ MCTS 93.29%.
  - *Luận điểm được chứng minh:* MCTS giúp 7B vượt qua năng lực của 14B sinh trực tiếp (91.46% vs 90.24%). MCTS trên 14B đạt trần 93.29%.
- **Kết quả APPS (300 bài full: 100 Intro, 100 Inter, 100 Comp):**
  - **7B (Chính thức - HuyinCP):** Direct (14.00% Pass@1, 30.51% Pass Rate) $\to$ MCTS Dual (19.00% Pass@1, 43.04% Pass Rate) $\to$ MCTS Test-only (22.67% Pass@1, 45.34% Pass Rate).
  - **14B (Chính thức - Kotori - ĐÃ HOÀN TẤT 300/300 bài):** MCTS Dual đạt **36.00% Pass@1** (108/300) và **53.49% Hidden Pass Rate**. So với 7B MCTS Dual, 14B tăng vượt bậc **+17.00% Pass@1** (gần gấp đôi) và tăng đặc biệt mạnh ở phân tầng Competition (28.00% vs 5.00%, +23.00%).
- **Phát hiện quan trọng về Ablation & Model Scaling:**
  - Cấu hình Test-only trên 7B cho hiệu quả cao hơn Dual Reward (22.67% vs 19.00%), xác nhận hiện tượng suy giảm năng lực tự thẩm định (critic degradation) của mô hình nhỏ $\le$ 7B.
  - Khi quy mô mô hình tăng lên 14B, khả năng suy luận kết hợp tìm kiếm cây MCTS giải quyết hiệu quả các bài toán thuật toán khó phức tạp (Competition: 28% pass).
- **Kiểm thử tự động:** Toàn bộ 36 tests qua (`pytest -v`), không có regression trong kiến trúc domain/ports/adapters.

## Active operating decisions

1. Tài liệu chi tiết đối đầu 7B vs 14B được chuẩn hóa tại [`docs/results/BENCHMARK_7B_VS_14B_REPORT.md`](../results/BENCHMARK_7B_VS_14B_REPORT.md).
2. Lưu giữ toàn bộ 9 báo cáo gốc của 7B trong [`docs/results/7b/`](../results/7b/) để bảo toàn tính minh bạch nguồn gốc (provenance).
3. Đợt chạy 14B APPS Benchmark 300 bài đã hoàn tất và gom kết quả vào [`runs/benchmark_apps_14b_dual_unified/`](../../runs/benchmark_apps_14b_dual_unified/). Modal GPU containers đã được dừng an toàn để bảo toàn quota.

## Current context

Mục tiêu nghiên cứu: Hoàn tất phần thực nghiệm của tiểu luận / luận văn chuyên ngành với bảng đối đầu đầy đủ giữa 7B và 14B, làm nổi bật vai trò của MCTS và cơ chế phản hồi kiểm thử trong việc nâng cao năng lực suy luận của các mô hình ngôn ngữ nhỏ (SLMs).
