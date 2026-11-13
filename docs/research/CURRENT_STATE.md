# Trạng thái hiện tại: 13/11/2026

## Thông tin đã chắc chắn

- **Protocol:** v3.1, code đóng băng ở commit `d9666c4` ([PROTOCOL.md](PROTOCOL.md) mục 8; quyết định D-006, D-007, D-008 trong [DECISION_LOG.md](DECISION_LOG.md)).
- **Nguồn số liệu duy nhất:** [BENCHMARK_LEDGER.md](../results/BENCHMARK_LEDGER.md) và [docs/results/v3/](../results/v3/). Mọi kết quả trước v3 đã gỡ khỏi nhánh và lưu ở tag `archive/pre-v3-2026-11-13`.
- **Đã xong E1–E4:** Qwen2.5-Coder-7B và Seed-Coder-8B (Colab A100), mỗi model đủ 6 run, không có lỗi kỹ thuật.
- **Qwen3.5-9B:**
  - Chạy trên Modal A100-SXM4-40GB: gate (khớp gate Colab ở 12/13 bài), Direct APPS, cả ba run HumanEval. Best-of-16 APPS đang chạy.
  - MCTS APPS chạy trên Colab: 116/300, đang dừng vì Colab thu hồi runtime khoảng mỗi 27 phút.

## Quan sát (chưa phải kết luận)

Số liệu ở ledger mục 2–10 và trong file phân tích.

- MCTS và Best-of-16 đều hơn Direct rõ rệt ở mọi ô đã có.
- MCTS không hơn Best-of-16 ở ô nào. MCTS tốn khoảng 12 lần token cho mỗi bài giải được trên APPS.
- Critic không giúp một cách nhất quán (cộng 5 ô: thắng 11, thua 10).
- Search, chưa tính critic, cải thiện rất rõ so với chương trình đầu tiên mà nó sinh ra.

## Việc đang mở

- Chạy xong MCTS APPS của Qwen3.5 (Colab khi ổn định, hoặc chạy lại từ đầu trên Modal nếu tăng hạn mức). Sau đó chạy `analyze_v3.py` cho cả 3 model và cập nhật ledger.
- Sửa lỗi kiểm tra CRLF khi resume ([RA_SOAT_2026-11-13.md](../RA_SOAT_2026-11-13.md) mục 2.2). Thêm test cho `analyze_v3.py`.
- Viết lại các chương báo cáo theo [KHUNG_BAO_CAO_v2.md](../report/KHUNG_BAO_CAO_v2.md).
- Tùy chọn: E5–E7.
