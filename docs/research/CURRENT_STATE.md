# Trạng thái hiện tại: 14/11/2026

## Thông tin đã chắc chắn

- **Protocol:** v3.1, code đóng băng ở commit `d9666c4` ([PROTOCOL.md](PROTOCOL.md) mục 8; quyết định D-006, D-007, D-008 trong [DECISION_LOG.md](DECISION_LOG.md)).
- **Nguồn số liệu duy nhất:** [BENCHMARK_LEDGER.md](../results/BENCHMARK_LEDGER.md) và [docs/results/v3/](../results/v3/). Phân tích cả 3 model: [analysis_v3_3models.json](../results/v3/analysis_v3_3models.json). Mọi kết quả trước v3 đã gỡ khỏi nhánh và lưu ở tag `archive/pre-v3-2026-11-13`.
- **Đã xong E1–E4 cho cả ba model (18 run), không có lỗi kỹ thuật.**
  - Qwen2.5-Coder-7B và Seed-Coder-8B: chạy trên Colab A100.
  - Qwen3.5-9B: 5 run chạy trên Modal A100-SXM4-40GB, MCTS APPS chạy trên Colab A100-SXM4-40GB. Gate của hai nền tảng khớp 12/13 bài. Ô APPS của model này vi phạm quy tắc "cùng nền tảng" (ledger mục 1).
- ⚠️ **Qwen3.5-9B bị cắt output trên APPS** (ledger mục 6.1). Khi tắt thinking, model viết lập luận trong comment của code và chạm giới hạn token.
  - Tỷ lệ lời gọi `code` bị cắt: Direct 26%, Best-of-16 29%, MCTS 28%.
  - Riêng MCTS có 17 bài không sinh được candidate nào, vì expansion ở gốc bị cắt.
  - Đã quyết định giữ nguyên kết quả và ghi vào threats to validity, không chạy lại (D-010).

## Quan sát (chưa phải kết luận)

Số liệu ở ledger mục 2–10 và trong file phân tích.

- **So với Direct:** MCTS hơn Direct có ý nghĩa sau Holm ở cả 6 ô. Best-of-16 hơn Direct có ý nghĩa ở 5/6 ô; riêng Qwen3.5 HumanEval thì p Holm = 0,053.
- **So với Best-of-16:** MCTS không hơn Best-of-16 ở ô nào. Trên APPS, MCTS thua về số (Seed-Coder −4,3 điểm, Qwen3.5 −3,0 điểm) nhưng chưa có ý nghĩa.
- **Chi phí:** tính theo token cho mỗi bài giải được trên APPS, MCTS tốn khoảng 12 lần Best-of-16 với hai model 7–8B, và khoảng 4 lần với Qwen3.5.
- **Critic:** không giúp một cách nhất quán (cộng 6 ô: thắng 12, thua 12), ở mọi mức khó của APPS. Critic chỉ xếp hạng lại các chương trình đã pass public, và với cách cộng reward hiện tại có 2 bài Dual chọn chương trình chưa pass hết public (ledger mục 8).
- **Dừng sớm:** dừng ở chương trình đầu tiên pass hết public cho cùng P@1 với bỏ critic và tiết kiệm 20,5–20,7% token trên APPS với hai model 7–8B, 52,4% với Qwen3.5, và 76,7–90,8% trên HE (ledger mục 9).
- **MCTS@k:** trên APPS, ở cùng mức token, Best-of-k luôn hơn RethinkMCTS cắt sau k rollout. Trên HE, RethinkMCTS sau 2 rollout (khoảng 3,7k token) đã ngang Best-of-16 (5,3k–7,1k token), chênh không quá 3 bài (ledger mục 10).
- **Search so với chương trình đầu tiên:** search, chưa tính critic, cải thiện rất rõ so với chương trình đầu tiên mà nó sinh ra (Qwen3.5 APPS: thắng 57, thua 0).

## Việc đang mở

- Sửa lỗi kiểm tra CRLF khi resume ([RA_SOAT_2026-11-13.md](../RA_SOAT_2026-11-13.md) mục 2.2).
- Viết lại các chương báo cáo theo [KHUNG_BAO_CAO_v2.md](../report/KHUNG_BAO_CAO_v2.md).
- Tùy chọn: E5–E6 (E7 đã bỏ, D-009).
