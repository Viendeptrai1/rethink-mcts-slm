# Chương 6. Hạn chế, Đe dọa Giá trị Thực nghiệm & Hướng Phát triển

> Tổng hợp trung thực theo chuẩn khoa học từ [PROTOCOL.md](../research/PROTOCOL.md), [DECISION_LOG.md](../research/DECISION_LOG.md), [Proposal.md §7](../../Proposal.md) và Mục Limitations của bài báo gốc ([Rethink_extracted.md §7](../../Rethink_extracted.md)).

## 6.1. Các Đe dọa tới Giá trị Thực nghiệm (Threats to Validity)

| Nhóm | Điểm hạn chế | Bằng chứng trong Repo | Cách xử lý & Trình bày trong Báo cáo |
| :--- | :--- | :--- | :--- |
| **Internal Validity (Độ giá trị nội tại)** | **Khác biệt chính sách chia Public/Hidden APPS giữa nhánh 7B và 14B:** 7B dùng `half` public + chấm `all_tests`; 14B dùng `first-2` public + chấm `disjoint hidden_suite`. | [apps.py](../../src/rethink_mcts/adapters/datasets/apps.py#L87) vs [rethinkmcts-apps-native-v2-w4-retry.md](../results/7b/rethinkmcts-apps-native-v2-w4-retry.md) | Nêu rõ trong Chương 3; đảm bảo mọi so sánh giữa các thuật toán (Direct vs BoN vs MCTS) đều thực hiện **nội bộ trên cùng một pipeline**; hoặc chạy bổ sung 1script rejudge đồng nhất. |
| **Internal Validity** | **Khác biệt cấu hình giữa HumanEval 14B MCTS và APPS 14B MCTS:** HumanEval 14B chạy `compact_v1`, Test-only, `c=1.5`, `rethinks=1`; APPS 14B chạy `native_v2`, Dual, `c=4.0`, `rethinks=2`. | [benchmark_humaneval_14b.yaml](../../configs/benchmark_humaneval_14b.yaml) vs [benchmark_apps_14b_dual.yaml](../../configs/benchmark_apps_14b_dual.yaml) | Ghi chính xác nhãn cấu hình ở Bảng 4.2; có thể chạy bổ sung HumanEval 14B Dual ([E9](EXPERIMENT_CHECKLIST.md)) vì HumanEval rất nhẹ. |
| **Internal Validity** | **5 bài thiếu candidate ở 7B APPS Dual (3 bài ở Test-only):** Do chạm ngưỡng search timeout 900s hoặc lỗi cú pháp khi trace. | [rethinkmcts-apps-native-v2-w4-retry.md](../results/7b/rethinkmcts-apps-native-v2-w4-retry.md) | Giữ nguyên mẫu số 300 (tính điểm 0 cho bài thiếu candidate) để không làm thiên lệch kết quả theo hướng có lợi. |
| **Statistical Conclusion Validity** | **Một hạt giống ngẫu nhiên (Single Seed):** Các run chính chạy với 1 seed (`seed=0` trên APPS, `seed=42` trên HumanEval). | Config YAML & Paper Appendix B (Table 7) | Dùng kiểm định cặp **McNemar's test** và **Paired Bootstrap 95% CI** trên 300 bài toán (và 164 bài HumanEval) để đánh giá độ bất định thống kê. |
| **Construct Validity** | **Giới hạn Token Cap mềm (Soft Token Cap):** Kiểm tra ngân sách diễn ra ở biên giữa các lời gọi; một lời gọi đang chạy có thể vượt nhẹ ngưỡng. | [PROTOCOL.md §5](../research/PROTOCOL.md) | Báo cáo lượng token thực tế tiêu thụ (**Realized Tokens**) như ở Bảng 4.4a thay vì chỉ nêu ngưỡng cấu hình. |
| **External Validity (Khả năng khái quát hóa)** | **Phạm vi mô hình & ngôn ngữ:** Thực nghiệm tập trung vào họ `Qwen2.5-Coder` (7B, 14B) và ngôn ngữ Python 3 trên APPS & HumanEval (chưa chạy thực nghiệm quy mô lớn trên `CodeContests` hay mô hình 3B). | [Proposal.md §3](../../Proposal.md) | Khẳng định kết luận trong phạm vi Python + họ Qwen2.5-Coder; kiến trúc `ports/datasets.py` đã có sẵn `code_contests.py` cho công việc mở rộng. |

---

## 6.2. Hạn chế Bản chất của Thuật toán RethinkMCTS

1. **Chi phí Token của Phân tích Khối lệnh (`block_analysis`):**
   Như chứng minh ở Bảng 4.4a, `block_analysis` chiếm **51.6% tổng lượng token** (19,479 tokens/bài trên 14B). Với các lỗi đơn giản như `SyntaxError` hay `NameError`, việc trích xuất toàn bộ CFG và gọi LLM phân tích từng block là chưa thật sự cần thiết.
2. **Hiện tượng Quá khớp Kiểm thử Công khai (Public Test Overfitting):**
   Khi đề bài chỉ có 2 test mẫu công khai, có tới **52/160 bài (32.5%)** trên 14B vượt qua 100% public tests nhưng vẫn thất bại ở bộ kiểm thử ẩn (do độ phức tạp thuật toán TLE hoặc thiếu điều kiện biên).
3. **Chỉ sửa nút lá gần nhất (Single-Leaf Refinement Limitation — Paper §7 Limitations):**
   Thuật toán hiện chỉ hiệu chỉnh bước tư duy ở nút lá vừa sinh mã lỗi; nếu sai lầm chiến lược nằm ngay từ nút gốc hoặc nút tầng 1, cây tìm kiếm phải dựa vào P-UCB quay lui sang nhánh khác thay vì sửa trực tiếp nút tổ tiên.

---

## 6.3. Hướng Phát triển Tương lai (Future Work)

1. **Bộ điều khiển Phản hồi Thích ứng (Adaptive Feedback Controller — RQ2):**
   Chỉ dùng `facts_only` hoặc `trace` ở lần lỗi đầu tiên và tự động leo thang lên `block_analysis` khi `pass_rate` không cải thiện, giúp cắt giảm đáng kể 51.6% chi phí token của `block_analysis`.
2. **Khai thác Hành trình Tìm kiếm để Huấn luyện Mô hình Nhỏ (Journey SFT & RLVR/GRPO — Proposal §7):**
   Tận dụng trực tiếp kho dữ liệu hành trình tìm kiếm đã thu thập trong `runs/` (chuỗi: *Thought sai $\to$ Code lỗi $\to$ CFG Feedback $\to$ Rethink Thought $\to$ Code đúng*) để tinh chỉnh có giám sát (Masked-loss Journey SFT) hoặc học tăng cường với phần thưởng kiểm chứng được (RLVR qua GRPO) cho các mô hình 3B–7B.
3. **Ứng dụng Thực tế (End-User Copilot & Self-Healing CI/CD):**
   Tích hợp chế độ đối đầu trực tiếp (A/B Duel View) và trợ lý tự động sửa lỗi theo Unit Test trên giao diện Web/IDE ([demo_scenarios.md](../demo_scenarios.md)).
