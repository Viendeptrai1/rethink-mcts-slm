# ĐỀ CƯƠNG NGHIÊN CỨU (RESEARCH PROPOSAL)

## Tên đề tài: Cải thiện khả năng suy luận của LLM trong sinh mã nguồn bằng Monte Carlo Tree Search với phản hồi từ kiểm thử tự động

* **Học viên / Sinh viên thực hiện:** Phan Quốc Viên (Kotori)
* **Giảng viên hướng dẫn:** [Họ và tên CBHD]
* **Mô hình mục tiêu:** Mô hình ngôn ngữ lớn mã nguồn mở phân khúc $\le$ 14B (Tiêu biểu: *Qwen2.5-Coder-7B-Instruct* chạy trên Ollama cục bộ và *Qwen2.5-Coder-14B* chạy trên Remote vLLM/Modal)
* **Định hướng tiếp cận:** **Tối ưu hóa tính toán tại thời điểm suy luận (Test-Time Compute Optimization) trên mô hình đóng băng trọng số (Frozen Weights)**

---

### 1. Đặt vấn đề và Tính cấp thiết của Đề tài (Motivation & Problem Statement)

Trong lĩnh vực Kỹ thuật Phần mềm và Trí tuệ Nhân tạo, việc ứng dụng Mô hình Ngôn ngữ Lớn (LLMs) vào bài toán sinh mã nguồn tự động (Code Generation) đã đạt được nhiều bước tiến đáng kể. Tuy nhiên, đối với các bài toán lập trình cấp độ thi đấu hoặc các thuật toán phức tạp (như trên APPS, CodeContests, HumanEval), các mô hình LLM thường gặp khó khăn lớn do bản chất sinh từ tự hồi quy (autoregressive generation) theo kiểu "System 1" (phản xạ nhanh nhưng thiếu tính toán chiến lược), dễ dẫn đến sinh mã sai cú pháp, lỗi logic hoặc vi phạm các trường hợp biên (corner cases).

Để khắc phục hạn chế trên, các phương pháp nâng cao năng lực lập luận (Reasoning) tại thời điểm suy luận (Inference-Time Search / Test-Time Scaling) đã ra đời:
1. **Reasoning via Planning (RAP):** Đưa thuật toán Monte Carlo Tree Search (MCTS) kết hợp với việc biến LLM thành một "Mô hình thế giới" (World Model) thông qua các câu lệnh prompt. Tuy nhiên, World Model bằng prompt trong RAP rất dễ bị ảo giác (hallucination) nghiêm trọng vì LLM không thể mô phỏng chính xác 100% môi trường máy tính thực thi.
2. **RethinkMCTS (Li et al., 2024/2025):** Giải quyết bài toán sinh mã nguồn bằng cách dùng MCTS tìm kiếm trên không gian ý tưởng thuật toán (Thought-level search) và đưa ra cơ chế *Rethink* — dùng phản hồi từ trình biên dịch và phân tích khối mã (block-level execution trace) để sửa trực tiếp nút tư duy bị lỗi tại nút lá thay vì tích lũy lỗi dài dòng như Reflexion.

#### Điểm nghẽn nghiên cứu và Động lực của đề tài:
* **Hạn chế của mô hình lớn & Chi phí điện toán:** Hầu hết các nghiên cứu hiện nay tập trung vào các mô hình khổng lồ đóng kín (GPT-4, Claude 3.5 Sonnet) với chi phí API rất cao và không thể triển khai trên hạ tầng nội bộ. Trong khi đó, các mô hình mã nguồn mở phân khúc nhỏ ($\le$ 14B như `Qwen2.5-Coder-7B`) có tiềm năng thương mại và ứng dụng thực tiễn rất lớn (chạy trực tiếp trên máy trạm cá nhân, máy chủ biên tiêu chuẩn), nhưng lại gặp hạn chế về độ dài chuỗi suy luận và dễ bị trôi ngữ cảnh (context drift).
* **Vấn đề "sửa mù quáng" (Blind Refinement) ở mô hình nhỏ:** Khi sinh code lỗi, việc nhồi toàn bộ traceback thô vào prompt (như Self-Refine) khiến mô hình nhỏ bị quá tải ngữ cảnh và có xu hướng lặp lại sai lầm cũ.
* **Chi phí suy luận MCTS nếu áp dụng máy móc:** Thuật toán MCTS truyền thống tiêu tốn lượng token khổng lồ nếu không có cơ chế chặn ngân sách thông minh và phản hồi ngắn gọn, trúng trọng tâm.

#### Giải pháp tiếp cận của đề tài:
Đề tài tập trung vào bài toán **Test-Time Compute Optimization**: Giữ **nguyên trọng số mô hình đóng băng (Frozen-weight Models)**, xây dựng một khung tìm kiếm MCTS tinh gọn kết hợp với **Sandbox thực thi mã đóng vai trò World Model chân lý**. Hệ thống phân tích sâu luồng điều khiển (Bytecode CFG) và biến runtime để cung cấp phản hồi ngữ nghĩa có cấu trúc, giúp mô hình nhỏ tự hiệu chỉnh tư duy tại chỗ (Leaf Revision) và hội tụ về lời giải đúng với số lần gọi mô hình tối thiểu.

---

### 2. Mục tiêu Nghiên cứu (Research Objectives)

1. **Mục tiêu 1:** Thiết kế và hiện thực khung thuật toán **Thought-Level MCTS** hoàn chỉnh theo kiến trúc *Ports & Adapters (Hexagonal Architecture)*, đảm bảo tính tách biệt tuyệt đối giữa lõi thuật toán và các adapter giao tiếp mô hình (Ollama / vLLM) hoặc môi trường thực thi.
2. **Mục tiêu 2:** Xây dựng cơ chế trích xuất vết thực thi sâu (**Execution-Guided Bytecode CFG & Variable State Tracing**) từ môi trường Sandbox Python an toàn, chuyển hóa lỗi runtime thành phản hồi ngắn gọn, loại bỏ hiện tượng ảo giác do traceback thô.
3. **Mục tiêu 3:** Hiện thực hóa cơ chế **Quay đầu tại nút lá (Leaf Revision)** kết hợp chính sách lan truyền phần thưởng **Max Backup ($Q = \max$)**, cho phép sửa đổi ý tưởng sai lầm mà vẫn bảo tồn chuỗi tư duy đúng đắn trước đó.
4. **Mục tiêu 4:** Tối ưu hóa hiệu quả sử dụng tài nguyên suy luận (**Budget-Aware Search & Early Stopping**): Thiết lập cơ chế chặn ngân sách (Tokens, Model Calls, Wall-time) và chính sách kích hoạt mạng Critic có điều kiện nhằm giảm thiểu tối đa chi phí tính toán.
5. **Mục tiêu 5:** Thực nghiệm đánh giá toàn diện trên các bộ dữ liệu benchmark chuẩn (**HumanEval, APPS, CodeContests**), so sánh hiệu quả giải bài (Pass@1, Pass Rate) và chi phí tài nguyên với các phương pháp cơ sở (*Direct Generation, Best-of-N, Self-Refine/Reflexion*).

---

### 3. Đối tượng và Phạm vi Nghiên cứu (Scope & Methodology)

* **Đối tượng nghiên cứu:** 
  * Các mô hình ngôn ngữ lớn chuyên biệt cho mã nguồn mở phân khúc $\le$ 14B: `Qwen2.5-Coder-7B-Instruct` (chạy cục bộ qua Ollama) và `Qwen2.5-Coder-14B` (chạy qua Remote Endpoint vLLM/Modal).
  * Thuật toán tìm kiếm trên cây MCTS mức tư duy: Công thức lựa chọn nhánh P-UCB (Eq. 1 & 2), chuẩn hóa xác suất tiên nghiệm (Prior Policy), lan truyền ngược Max Backup.
* **Phạm vi nghiên cứu:**
  * **Trọng số mô hình:** Giữ **nguyên vẹn (Frozen Weights)** trong toàn bộ quá trình nghiên cứu, không can thiệp huấn luyện lại trọng số (không yêu cầu cụm GPU huấn luyện khổng lồ).
  * **Ngôn ngữ lập trình:** Tập trung chuyên sâu vào ngôn ngữ Python 3.
  * **Môi trường thực thi an toàn:** Sandbox Python cô lập (Trusted Subprocess trên máy trạm và Docker container unprivileged) đóng vai trò World Model cung cấp phản hồi kiểm thử tự động.
  * **Ngăn ngừa rò rỉ kiểm thử (Test Leakage Prevention):** Đảm bảo tính trung thực khoa học bằng cách tách rời tuyệt đối giữa `PublicProblem` (cho MCTS tìm kiếm) và `HiddenProblem` (chỉ mở ra cho tiến trình `HiddenJudge` độc lập sau khi lời giải đã đóng băng).
* **Bộ dữ liệu thực nghiệm:**
  * **`HumanEval` (OpenAI):** 164 bài toán hàm chuẩn hóa để kiểm chứng tính đúng đắn thuật toán.
  * **`APPS` (Hendrycks et al.):** Bộ dữ liệu toán thuật toán phong phú gồm 3 phân tầng: *Introductory*, *Interview*, và *Competition*.
  * **`CodeContests` (Google DeepMind):** Bộ dữ liệu lập trình thi đấu Olympic/Codeforces độ khó cao.

---

### 4. Kiến trúc và Phương pháp Đề xuất

Hệ thống được thiết kế theo 4 trụ cột kỹ thuật tối ưu hóa suy luận tại thời điểm thực thi:

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRỤ CỘT 1: KHÔNG GIAN TÌM KIẾM MỨC TƯ DUY & LỰA CHỌN P-UCB                                      │
│ - Thu hẹp không gian tìm kiếm: Phân rã bài toán thành các bước ý tưởng thuật toán (Thoughts)    │
│   thay vì sinh từng token hay từng dòng lệnh riêng lẻ.                                          │
│ - Thuật toán chọn nhánh P-UCB: Cân bằng khai thác (Exploitation) và khám phá (Exploration)      │
│   kết hợp xác suất tiên nghiệm P(u) do mô hình tự đánh giá.                                     │
└────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRỤ CỘT 2: SANDBOX THỰC THI LÀM "WORLD MODEL CHÂN LÝ" & PHÂN TÍCH CFG                           │
│ - Mã nguồn sinh ra tại mỗi bước được thực thi ngay trong Sandbox với các ca kiểm thử công khai. │
│ - Khi xảy ra lỗi: Trích xuất Đồ thị luồng điều khiển (Bytecode CFG) và chụp biến runtime        │
│   tại khối lệnh thất bại, chuyển hóa thành Verbal Feedback ngắn gọn, chuẩn xác.                  │
└────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRỤ CỘT 3: CƠ CHẾ HIỆU CHỈNH TƯ DUY TẠI LÁ (LEAF REVISION) & MAX BACKUP                         │
│ - Khi code lỗi: Chỉ thay thế nút tư duy tại lá (Leaf Revision) dựa trên feedback thực thi,       │
│   giữ nguyên toàn bộ chuỗi tư duy tổ tiên (Parent Path) đã chứng minh đúng trước đó.            │
│ - Chính sách Max Backup: Cập nhật Q(p) = max Q(u) thay vì trung bình cộng, bảo vệ hướng đi      │
│   tối ưu không bị phạt oan bởi các lần thử nghiệm thất bại.                                     │
└────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRỤ CỘT 4: KIỂM SOÁT NGÂN SÁCH NGHIÊM NGẶT & HÀM THƯỞNG KÉP CÓ ĐIỀU KIỆN                        │
│ - Budget Manager: Kiểm soát chặt chẽ số lần gọi mô hình, số lần sinh mã, token và timeout.      │
│ - Dừng sớm (Early Stopping): Dừng tìm kiếm ngay khi tìm thấy nghiệm vượt qua 100% public tests. │
│ - Conditional Critic: Chỉ kích hoạt mô hình tự đánh giá chất lượng mã khi đã vượt qua 100%     │
│   public tests, loại bỏ lãng phí token vào code lỗi cú pháp.                                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Kiến trúc Phần mềm (Hexagonal Architecture / Clean Code):
Toàn bộ giải pháp được hiện thực hóa trong thư mục [`src/rethink_mcts/`](file:///Users/kotori/Documents/TLCN/src/rethink_mcts) với 5 tầng phân tách rõ ràng:
- **`domain/`**: Chứa các thực thể bất biến (`ProgramCandidate`, `Tree`, `PublicProblem`, `BudgetManager`).
- **`ports/`**: Các giao diện trừu tượng (`ThoughtProposer`, `CodeGenerator`, `PublicExecutor`, `RunStore`).
- **`policies/`**: Hiện thực chính xác các công thức toán học (`PUCBSelector`, `MaxBackupPolicy`, `PaperDualRewardPolicy`).
- **`adapters/`**: Các bộ chuyển đổi công nghệ (`HttpModelGateway`, `Bytecode CFG/DynamicTraceCollector`, `DockerExecutor`, `HumanEval/APPS Adapters`).
- **`application/`**: Các ca sử dụng điều phối (`SearchEngine`, `CandidateEvaluator`, `FeedbackService`, `HiddenJudge`, `MetricsReporter`).

---

### 5. Kế hoạch Thực nghiệm và Tiêu chuẩn Đánh giá (Experiments & Evaluation)

#### 5.1. Môi trường Thực nghiệm & Phần cứng
* **Môi trường cục bộ:** Máy trạm macOS/Linux tiêu chuẩn chạy **Ollama** với mô hình `qwen2.5-coder:7b` (yêu cầu $\le$ 8GB–16GB RAM/VRAM).
* **Môi trường GPU đám mây (nếu cần scale 14B):** 1 GPU NVIDIA (RTX 3090/4090 24GB hoặc A10G trên Modal/vLLM) chạy mô hình `qwen2.5-coder:14b`.
* **Môi trường an toàn:** Thực thi mã trong Docker container unprivileged với cgroup giới hạn CPU và timeout 2.0s mỗi ca kiểm thử.

#### 5.2. Các Phương pháp So sánh (Baselines)
1. **Direct Generation (Zero-shot / CoT):** Sinh mã 1 lần trực tiếp từ prompt mô tả bài toán.
2. **Best-of-N ($N=4, 8$):** Lấy mẫu độc lập $N$ chương trình, chạy public tests và chọn ứng viên có điểm pass rate cao nhất.
3. **Self-Refine / Reflexion:** Phương pháp tự sửa sai truyền thống nhồi traceback thô vào ngữ cảnh lặp lại tuần tự.
4. **RethinkMCTS (Phương pháp đề xuất):** Tìm kiếm cây mức tư duy kết hợp phân tích CFG và cơ chế Leaf Revision.

#### 5.3. Các Nghiên cứu Triệt tiêu (Ablation Studies)
* **Ablation 1 (Chất lượng phản hồi lỗi):** So sánh hiệu quả giữa phản hồi CFG + Variable Snapshot của đề tài với phản hồi chỉ có compiler traceback thô.
* **Ablation 2 (Chính sách lan truyền phần thưởng):** So sánh Max Backup ($Q = \max$) với Mean Backup (MCTS truyền thống).
* **Ablation 3 (Hiệu quả ngân sách & Đường cong mở rộng):** Đo lường Pass@1 theo mức tăng số lượt sinh mã ($N = 1, 2, 4, 8, 16$), chứng minh RethinkMCTS đạt điểm bão hòa chính xác nhanh hơn với chi phí token thấp hơn.
* **Ablation 4 (Trọng số hàm thưởng):** Đánh giá vai trò của trọng số kiểm thử công khai ($w_{\text{test}}$) so với điểm Critic ($w_{\text{llm}}$).

#### 5.4. Tiêu chí Đánh giá (Metrics)
* **Pass@1 (%):** Tỷ lệ bài toán giải quyết đúng 100% bộ kiểm thử ẩn (`hidden_suite`) ngay trong lần thử đầu tiên của ứng viên được chọn (`selected.py`).
* **Mean Hidden Pass Rate (%):** Tỷ lệ phần trăm ca kiểm thử ẩn vượt qua trung bình.
* **Model Calls & Code Attempts:** Tổng số lượt gọi mô hình và số lần thử sinh code cần thiết để tìm ra lời giải.
* **Token Consumption & Wall-Clock Time:** Lượng token tiêu thụ trung bình và thời gian thực thi trên mỗi bài toán.

---

### 6. Kế hoạch Triển khai Dự kiến (Roadmap)

| Giai đoạn | Thời gian | Nội dung công việc chính | Kết quả đầu ra (Deliverables) |
| :--- | :--- | :--- | :--- |
| **Giai đoạn 1** | Tuần 1 - 3 | Hoàn thiện kiến trúc hệ thống MCTS, Sandbox Python an toàn, bộ parser bytecode CFG và tracing biến runtime; thiết lập 36 bài test tự động (đã hoàn thành). | Codebase chuẩn Ports & Adapters; 36/36 tests passed; CLI `rethink` hoạt động hoàn chỉnh. |
| **Giai đoạn 2** | Tuần 4 - 6 | Chuẩn hóa kho dữ liệu benchmark HumanEval và APPS tách rời `public/` và `judge/`; thiết lập các baseline so sánh (Direct, Best-of-N, Self-Refine). | Dữ liệu `prepared/humaneval` và `prepared/apps`; Module `baselines.py` hoàn thiện. |
| **Giai đoạn 3** | Tuần 7 - 9 | Chạy thực nghiệm quy mô trên `Qwen2.5-Coder-7B` (Ollama cục bộ) và `Qwen2.5-Coder-14B` (Remote Endpoint); thu thập bảng số liệu Pass@1, Token, Model Calls. | Tập log kết quả `runs/`; Bảng tổng hợp so sánh hiệu năng các phương pháp. |
| **Giai đoạn 4** | Tuần 10 - 12 | Thực hiện toàn diện các nghiên cứu triệt tiêu (Ablations: CFG vs Traceback thô, Max vs Mean, Scaling curve); phân tích các trường hợp thành công và thất bại. | Biểu đồ scaling curve, phân tích case-study định tính và định lượng. |
| **Giai đoạn 5** | Tuần 13 - 15 | Hoàn thiện toàn văn báo cáo luận văn / tiểu luận chuyên ngành; chuẩn bị slide bảo vệ và đóng gói kho lưu trữ mã nguồn mở trên GitHub. | Báo cáo hoàn chỉnh, Slide thuyết trình và Repository GitHub sẵn sàng nghiệm thu. |

---

### 7. Hướng Phát triển Tương lai (Future Work)

Mặc dù trọng tâm đề tài là tối ưu hóa suy luận với mô hình đóng băng trọng số, toàn bộ quá trình tìm kiếm MCTS đã được tích hợp cơ chế lưu vết chi tiết (**MCTS Journey Trajectory Logging**). Khi có điều kiện tiếp cận các cụm tính toán GPU lớn trong tương lai, kho dữ liệu hành trình tư duy này (chuỗi: *Ý tưởng $\to$ Code lỗi $\to$ Phản hồi thực thi $\to$ Rethink $\to$ Code đúng*) hoàn toàn có thể được khai thác để:
1. Huấn luyện tinh chỉnh chuyên sâu theo hành trình (**Journey SFT**) với kỹ thuật Masked Loss trên vết compiler.
2. Tối ưu hóa chính sách chính xác hơn bằng học tăng cường không cần Critic (**RLVR qua GRPO**).

---

### 8. Tài liệu Tham khảo Chính (References)

1. **Li, Q., Xia, W., Dai, X., Du, K., Liu, W., Wang, Y., Tang, R., Yu, Y., & Zhang, W. (2024/2025).** *RethinkMCTS: Refining Erroneous Thoughts in Monte Carlo Tree Search for Code Generation.* arXiv:2409.09584.
2. **Hao, S., Gu, Y., Ma, H., Hong, J. J., Wang, Z., Wang, D. Z., & Hu, Z. (2023).** *Reasoning with Language Model is Planning with World Model (RAP).* arXiv:2305.14992.
3. **Chen, M., et al. (OpenAI, 2021).** *Evaluating Large Language Models Trained on Code (HumanEval).* arXiv:2107.03374.
4. **Hendrycks, D., et al. (NeurIPS 2021).** *Measuring Coding Challenge Competence With APPS.* NeurIPS 2021.
5. **Li, Y., et al. (Google DeepMind, 2022).** *Competition-level code generation with AlphaCode (CodeContests).* Science, 378(6624), 1092-1097.
6. **Hui, B., Yang, J., Cui, Z., et al. (Qwen Team, 2024).** *Qwen2.5-Coder Technical Report.* arXiv:2409.12186.
7. **Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S. (NeurIPS 2023).** *Reflexion: Language Agents with Verbal Reinforcement Learning.*
8. **Zhong, L., Wang, Z., & Shang, J. (2024).** *LDB: A Large Language Model Debugger via Verifying Runtime Execution Step-by-Step.* arXiv:2402.16906.
