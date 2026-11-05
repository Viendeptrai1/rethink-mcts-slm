# Chương 1. Đặt vấn đề & Cơ sở Lý thuyết

> Đối chiếu trực tiếp từ [Proposal.md](../../Proposal.md), bài báo gốc *RethinkMCTS* ([Rethink_extracted.md](../../Rethink_extracted.md), arXiv:2409.09584v2 / EMNLP 2025), *RAP* ([RAP_extracted.md](../../RAP_extracted.md), arXiv:2305.14992), *LDB* (arXiv:2402.16906) và [HYPOTHESIS_LAB.md](../research/HYPOTHESIS_LAB.md).

## 1.1. Bối cảnh: Từ Sinh mã Tự hồi quy (System 1) đến Tìm kiếm Thời điểm Suy luận (System 2)

- **Hạn chế của sinh tự hồi quy một lượt (Autoregressive / System 1):** Với các bài toán thuật toán có điều kiện biên phức tạp (APPS, HumanEval, CodeContests), sinh mã trực tiếp một lần dễ mắc lỗi cú pháp, sai điều kiện biên (off-by-one, corner cases) hoặc chọn sai cấu trúc dữ liệu ngay từ những token đầu tiên.
- **Bài toán triển khai trên mô hình nhỏ đóng băng trọng số ($\le$ 14B, Frozen Weights):**
  - Các nghiên cứu gốc (như RethinkMCTS trên GPT-3.5-turbo và GPT-4o-mini) dựa vào mô hình thương mại đóng kín qua API.
  - Mô hình mã nguồn mở nhỏ (`Qwen2.5-Coder-7B-Instruct`, `Qwen2.5-Coder-14B-Instruct`) có thể tự chủ hạ tầng (Ollama cục bộ hoặc 1 GPU vLLM), nhưng khả năng giải đúng ngay lần đầu còn thấp — ví dụ `Qwen2.5-Coder-7B` Direct chỉ đạt **14.00% Pass@1** trên APPS-300 ([BENCHMARK_7B_VS_14B_REPORT.md](../results/BENCHMARK_7B_VS_14B_REPORT.md)).

## 1.2. Khoảng trống của các Phương pháp Hiện có (Literature Gap)

| Nhóm phương pháp | Đại diện | Cơ chế | Hạn chế khi áp dụng cho sinh mã trên SLM ($\le$ 14B) |
| :--- | :--- | :--- | :--- |
| **Lấy mẫu độc lập** | Direct, Best-of-$N$ | Sinh $N$ chương trình độc lập, lọc theo public tests | Không tận dụng thông tin lỗi từ lần chạy trước để sửa sai; lãng phí lời gọi khi mô hình lặp lại cùng một lỗi logic. |
| **Sửa lặp tích lũy lịch sử** | Self-Refine, Reflexion, LATS | Lưu toàn bộ code lỗi và lịch sử phản hồi vào bộ nhớ/prompt cho lượt sau | (1) Ngữ cảnh phình to nhanh chóng gây tốn token và trôi ngữ cảnh (context drift) trên SLM; (2) Trong cây tìm kiếm, nút tư duy sai vẫn nằm lại trên đường đi (Paper §1, Table 2). |
| **MCTS với World Model bằng Prompt** | RAP (Hao et al., 2023) | Dùng chính LLM dự đoán trạng thái tiếp theo thông qua prompt | LLM không thể mô phỏng chính xác 100% trình thông dịch Python và giá trị biến runtime $\to$ dễ ảo giác (hallucination) trạng thái thực thi (Proposal §1). |
| **MCTS mức Token / Code** | PG-TD (Zhang et al., 2023) | Tìm kiếm trên từng token hoặc toàn bộ code dựa trên điểm thưởng vô hướng ($v_{test}$) | Không gian hành động quá lớn hoặc thiếu phân rã chiến lược; điểm vô hướng không chỉ ra được dòng/khối lệnh nào gây lỗi. |
| **Gỡ lỗi mức khối lệnh tuần tự** | LDB (Zhong et al., 2024) | Chia code thành basic blocks (CFG), theo dõi biến runtime để sửa tuần tự | Chỉ đi theo một nhánh sửa duy nhất; nếu hướng thuật toán ban đầu sai bản chất thì việc vá cục bộ không thoát khỏi cực trị địa phương. |

## 1.3. Vấn đề Nghiên cứu Đặc thù trên Mô hình Nhỏ (7B–14B)

1. **Chi phí token của phân tích mức khối lệnh (Block-level Analysis Cost):**
   Trong RethinkMCTS, bước trích xuất CFG + trạng thái biến và gọi LLM phân tích khối lệnh chiếm tỷ trọng token lớn nhất. Trên thực nghiệm 14B APPS-300 của đề tài, riêng bước `block_analysis` chiếm tới **51.6% tổng lượng token** (5.84 triệu / 11.33 triệu token).
2. **Suy giảm năng lực tự thẩm định (Critic Degradation) ở mô hình 7B:**
   Bài báo gốc dùng Dual Evaluation ($0.8 \cdot v_{test} + 0.2 \cdot v_{llm}$) trên GPT-3.5/GPT-4o-mini để phân biệt các code cùng pass public tests. Tuy nhiên, trên `Qwen2.5-Coder-7B`, thực nghiệm APPS-300 cho thấy tắt Critic (`Test-only`: **22.67%**) lại tốt hơn bật Critic (`Dual`: **19.00%**).
3. **Độ nhạy với độ phủ của Public Tests:**
   Khi số lượng public tests ít (HumanEval trung bình 2.8 tests; APPS cấu hình 2 public tests), hiện tượng **quá khớp kiểm thử công khai (public test overfitting)** xảy ra thường xuyên: chương trình pass 100% public tests nhưng trượt hidden tests.

## 1.4. Câu hỏi Nghiên cứu (Research Questions)

Kết hợp [Proposal.md](../../Proposal.md), bài báo gốc và [HYPOTHESIS_LAB.md](../research/HYPOTHESIS_LAB.md):

| Mã | Câu hỏi nghiên cứu | Đối chiếu thực nghiệm trong báo cáo |
| :-- | :--- | :--- |
| **RQ1 (Hiệu quả tổng thể)** | RethinkMCTS cải thiện Pass@1 và Hidden Pass Rate bao nhiêu so với Direct, Best-of-$N$ và Iterative Repair trên mô hình 7B và 14B? | Bảng 4.1, 4.2, 4.3 ([Chương 4](04_ket_qua_thuc_nghiem.md)) |
| **RQ2 (Đóng góp thành phần - Ablation)** | Đóng góp của từng thành phần cốt lõi: (a) Cơ chế *Rethink* tại lá, (b) Mức độ phản hồi thực thi (*Facts / Trace / Block CFG*), (c) Chính sách *Max Backup* vs *Mean Backup*? | Mục 5.3, 5.4 ([Chương 5](05_phan_tich_thao_luan.md)) |
| **RQ3 (Quy mô mô hình & LLM Critic)** | Hiệu quả của RethinkMCTS và khả năng tự thẩm định của *Conditional LLM Critic* thay đổi như thế nào khi mở rộng từ 7B lên 14B? | Mục 5.1, 5.2 ([Chương 5](05_phan_tich_thao_luan.md)) |
| **RQ4 (Chi phí & Mở rộng theo ngân sách)** | Chi phí token/lời gọi theo từng vai trò (Expansion, Code, Block Analysis, Rethink, Critic) và đường cong hiệu năng theo số lượt thử (Test-Time Scaling) diễn biến ra sao? | Mục 4.4 ([Chương 4](04_ket_qua_thuc_nghiem.md)) & Mục 5.6 ([Chương 5](05_phan_tich_thao_luan.md)) |

## 1.5. Ranh giới Đóng góp (Attribution & Contribution Boundary)

Theo nguyên tắc tại [LITERATURE_NOTES.md](../research/LITERATURE_NOTES.md) và [DECISION_LOG.md](../research/DECISION_LOG.md):
- **Phần kế thừa từ bài báo gốc (Li et al., 2024/2025; Zhong et al., 2024):** Khung tìm kiếm MCTS mức tư duy (P-UCB), cơ chế sửa tư duy tại lá (*Rethink*), phản hồi mức khối lệnh (Block-level CFG trace) và công thức thưởng kép (*Dual Evaluation*).
- **Phần kỹ thuật & điều chỉnh cho mô hình nhỏ của đề tài:**
  1. Thiết kế lại toàn bộ hệ thống theo kiến trúc **Ports & Adapters (Hexagonal Architecture)** với cơ chế chống rò rỉ kiểm thử ẩn (`PublicProblem` tách biệt `HiddenJudge`), quản lý ngân sách (`BudgetManager`) và dừng sớm (`Early Stopping`).
  2. Bộ prompt nén (`compact_v1` / `native_v2`), giới hạn ngữ cảnh trace (`bounded_trace_context`), và cơ chế kích hoạt Critic có điều kiện giúp chỉ tốn **1.1% tổng token** cho Critic.
  3. Thực nghiệm đối đầu trên phân khúc mô hình mở **7B vs 14B** và phát hiện hiện tượng **Critic Degradation ở 7B** cùng sự bứt phá ở phân tầng Competition khi lên 14B.
  4. Công cụ trực quan hóa cây tìm kiếm và chạy thử nghiệm trực tiếp (**RethinkMCTS Trace Viewer**).
