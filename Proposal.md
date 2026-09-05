# ĐỀ CƯƠNG NGHIÊN CỨU (RESEARCH PROPOSAL)

## Tên đề tài: Cải thiện khả năng suy luận của LLM trong sinh mã nguồn bằng Monte Carlo Tree Search với phản hồi từ kiểm thử tự động

* **Học viên / Sinh viên thực hiện:** [Họ và tên]
* **Giảng viên hướng dẫn:** [Họ và tên CBHD]
* **Mô hình mục tiêu:** Mô hình ngôn ngữ lớn mã nguồn mở phân khúc $\le$ 14B (Tiêu biểu: *Qwen2.5-Coder-7B-Instruct*, *Qwen2.5-Coder-14B*)

---

### 1. Đặt vấn đề và Tính cấp thiết của Đề tài (Motivation & Problem Statement)

Trong lĩnh vực Kỹ thuật Phần mềm và Trí tuệ Nhân tạo, việc ứng dụng Mô hình Ngôn ngữ Lớn (LLMs) vào bài toán sinh mã nguồn tự động (Code Generation) đã đạt được nhiều bước tiến đáng kể. Tuy nhiên, đối với các bài toán lập trình cấp độ thi đấu hoặc các thuật toán phức tạp (như trên APPS, HumanEval), các mô hình LLM thường gặp khó khăn lớn do bản chất sinh từ tự hồi quy (autoregressive generation) theo kiểu "System 1" (phản xạ nhanh nhưng thiếu tính toán chiến lược), dễ dẫn đến sinh mã sai cú pháp, lỗi logic hoặc vi phạm các trường hợp biên (corner cases).

Để khắc phục hạn chế trên, các phương pháp nâng cao năng lực lập luận (Reasoning) tại thời điểm suy luận (Inference-time Search) đã ra đời:
1. **Reasoning via Planning (RAP):** Đưa thuật toán Monte Carlo Tree Search (MCTS) kết hợp với việc biến LLM thành một "Mô hình thế giới" (World Model) thông qua các câu lệnh prompt. Tuy nhiên, World Model bằng prompt trong RAP rất dễ bị ảo ảnh (hallucination) và việc chạy MCTS thuần túy ở bước suy luận đòi hỏi tài nguyên tính toán khổng lồ.
2. **RethinkMCTS:** Giải quyết bài toán sinh mã nguồn bằng cách dùng MCTS tìm kiếm trên không gian tư duy (Thought-level search) và đưa ra cơ chế *Rethink* — dùng phản hồi từ trình biên dịch và phân tích khối mã (block-level execution trace) để sửa trực tiếp nút tư duy bị lỗi tại nút lá thay vì tích lũy lỗi dài dòng như Reflexion. 

**Điểm nghẽn nghiên cứu hiện tại (Research Gap):**
* Cả RAP và RethinkMCTS đều chỉ là **thuật toán tìm kiếm tĩnh trên các mô hình đã đóng băng trọng số (Frozen Weights)**. Chúng tiêu tốn hàng chục nghìn token và hàng chục lượt gọi mô hình cho mỗi câu hỏi tại bước suy luận (Inference-time latency rất lớn).
* Chính nhóm tác giả của RethinkMCTS đã chỉ ra hạn chế cốt lõi trong bài báo: *khung tìm kiếm sinh ra dữ liệu hành trình tư duy rất chất lượng nhưng chưa hề được nghiên cứu để fine-tune hay tối ưu hóa trọng số cho mô hình*.
* Trong khi đó, các mô hình mã nguồn mở phân khúc $\le$ 14B (như Qwen2.5-Coder-7B) có tiềm năng rất lớn nếu được huấn luyện đúng cách, hoàn toàn phù hợp để triển khai thực tế trên hạ tầng máy chủ tiêu chuẩn hoặc cục bộ.

**Giải pháp đề xuất của đề tài:**
Xây dựng khung phương pháp lai kết hợp giữa **Tìm kiếm cây MCTS với phản hồi kiểm thử tự động** và **Học tăng cường dựa trên phần thưởng kiểm chứng (RLVR / GRPO)** cùng **Huấn luyện hành trình (Journey Learning)**. Phương pháp này dùng MCTS làm "động cơ khám phá" để khai thác các vết tự sửa lỗi thực tế, huấn luyện mô hình $\le$ 14B nội hóa (internalize) năng lực tự phê bình và quay đầu; sau đó dùng MCTS tinh gọn làm công cụ mở rộng năng lực tính toán khi suy luận (Test-Time Scaling) cho các bài toán cực khó.

---

### 2. Mục tiêu Nghiên cứu (Research Objectives)

1. **Mục tiêu 1:** Xây dựng và tối ưu hóa quy trình tìm kiếm trên cây Monte Carlo (MCTS) cho sinh mã nguồn, tích hợp cơ chế phản hồi sâu từ môi trường kiểm thử tự động (Unit Test Execution, Variable State Trace).
2. **Mục tiêu 2:** Thiết kế cơ chế khai thác dữ liệu hành trình tư duy (MCTS-guided Journey Trajectory Mining) và huấn luyện mô hình ngôn ngữ lớn phân khúc $\le$ 14B thông qua **Journey SFT** (với kỹ thuật Masked Loss trên vết lỗi môi trường).
3. **Mục tiêu 3:** Ứng dụng thuật toán **Group Relative Policy Optimization (GRPO)** với hàm phần thưởng kiểm chứng được (Verifiable Test-based Reward) để củng cố khả năng tự suy luận và tự sửa sai nội tại của mô hình.
4. **Mục tiêu 4:** Thiết lập cơ chế suy luận lai (Hybrid Test-Time Compute): mô hình tự sửa lỗi ngầm trong 1 lượt sinh đối với bài toán thông thường, và kích hoạt MCTS gia tốc (với ngân sách rollout giảm 70% so với RethinkMCTS gốc) đối với bài toán phức tạp.
5. **Mục tiêu 5:** Đánh giá thực nghiệm toàn diện trên các tập dữ liệu benchmark chuẩn (HumanEval-Plus, MBPP-Plus, APPS) để chứng minh tính vượt trội về độ chính xác (Pass@1, Pass Rate) và hiệu quả sử dụng tài nguyên token/thời gian.

---

### 3. Đối tượng và Phạm vi Nghiên cứu (Scope & Methodology)

* **Đối tượng nghiên cứu:** 
  * Mô hình ngôn ngữ lớn phân khúc tham số $\le$ 14B (mô hình cơ sở chính: `Qwen2.5-Coder-7B-Instruct` / `Qwen2.5-Coder-14B-Instruct`).
  * Thuật toán tìm kiếm trên cây MCTS (P-UCB, Selection, Expansion, Evaluation, Backpropagation, Rethink).
  * Thuật toán học tăng cường không cần mạng Critic: GRPO (Group Relative Policy Optimization).
* **Phạm vi nghiên cứu:**
  * Ngôn ngữ lập trình mục tiêu: Python 3.
  * Môi trường thực thi: Sandbox Python cô lập (Docker container / safe execution subprocess) đóng vai trò là "World Model chân lý" (Ground-truth World Model) cung cấp phản hồi kiểm thử tự động và phân tích lỗi.
  * **Bộ dữ liệu nghiên cứu chính (Primary Dataset):** Bộ dữ liệu thi đấu lập trình **`deepmind/code_contests`** (Google DeepMind - AlphaCode, *Li et al., Science 2022*):
    * *Quy mô:* 13,328 bài luyện tập (Train), 117 bài xác thực (Validation) và 165 bài kiểm thử chuẩn (Test).
    * *Cơ cấu 3 tầng test case:* Bao gồm `public_tests` (test mẫu đề bài cho MCTS evaluation), `private_tests` (test ẩn cho judge) và `generated_tests` (test đột biến chống học vẹt).
    * *Mỏ vàng tự sửa lỗi:* Chứa cả lời giải đúng (`solutions`) và lời giải sai của con người (`incorrect_solutions`), làm dữ liệu hạt giống lý tưởng cho cơ chế **Rethink** và **Journey SFT**.
    * *Phân tầng độ khó:* Sử dụng chỉ số `cf_rating` từ Codeforces (tập trung phân khúc 800 - 1500 phù hợp với mô hình $\le$ 14B).
  * **Tập dữ liệu mở rộng & Benchmark kiểm chứng chéo:** HumanEval-Plus và MBPP-Plus để chứng minh tính tổng quát hóa ngoài môi trường Competitive Programming.

---

### 4. Kiến trúc và Phương pháp Đề xuất

Phương pháp tiếp cận gồm 4 trụ cột kỹ thuật gắn kết chặt chẽ:

```
+-------------------------------------------------------------------------------+
| Giai đoạn 1: MCTS Journey Mining (Khai thác Hành trình Ngoại vi)               |
| [Prompt] -> MCTS (Thought-level) + Python Sandbox Test -> Journey Trajectories|
| (Vết tư duy: Giả thuyết ban đầu -> Mã lỗi -> Báo lỗi Test -> Rethink -> Mã đúng) |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| Giai đoạn 2: Journey SFT (Dạy mô hình năng lực tự quay đầu)                   |
| - Huấn luyện mô hình <= 14B trên chuỗi Journey đầy đủ                         |
| - Selective Loss Masking: Mask bỏ traceback compiler, chỉ tính loss trên       |
|   những bước tư duy Rethink và đoạn code sửa đổi thành công (wt > 1)          |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| Giai đoạn 3: RLVR via GRPO (Tối ưu hóa bằng Học tăng cường)                   |
| - Lấy mẫu G lời giải cho mỗi bài toán (không cần chạy MCTS trong vòng RL)      |
| - Hàm thưởng kiểm chứng khách quan: r = r_test (Binary) + r_format            |
| - Cập nhật chính sách policy qua GRPO mà không cần Value Model                |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| Giai đoạn 4: Hybrid Inference Engine (Hệ thống Suy luận Lai Thực chiến)       |
| - Chế độ 1 (Standard): 1-pass Generation (Mô hình tự sinh thinking & tự sửa)   |
| - Chế độ 2 (Heavy/Search): Kích hoạt RethinkMCTS (Hội tụ sau 3-5 rollouts     |
|   nhờ Policy đã tối ưu, thay vì 16 rollouts như mô hình đông cứng)           |
+-------------------------------------------------------------------------------+
```

#### 4.1. Refined-MCTS với Phản hồi Kiểm thử Tự động làm World Model Chân lý
Khác với bài toán lập kế hoạch thông thường của RAP (dùng LLM làm World Model dễ sinh ảo ảnh), trong sinh mã nguồn, **trình thực thi mã (Execution Sandbox) là một World Model hoàn hảo 100%**.
* Tại mỗi nút lá, mã nguồn sinh ra được chạy qua bộ kiểm thử tự động (Unit Test Suite).
* Nếu thất bại, hệ thống phân tích vết biến chạy (Block-level analysis) tạo thành chuỗi phản hồi bằng lời (Verbal Feedback $f$).
* Cơ chế **Rethink** thay thế nút tư duy bị lỗi tại chỗ bằng tư duy mới: $z^{new} \sim p(z \mid s, f, z^{old})$, tránh làm phình cửa sổ ngữ cảnh và hướng cây tìm kiếm về nhánh đúng.

#### 4.2. Huấn luyện Hành trình (Journey Learning) với Masked Loss
Hầu hết các kỹ thuật SFT chỉ học trên nghiệm đúng hoàn hảo cuối cùng, bỏ qua bài học từ sai lầm. Phương pháp áp dụng hàm mất mát Journey Loss:
$$\mathcal{L}_{\text{journey}}(\theta) = - \sum_{t=1}^T w_t \log \pi_\theta(a_t \mid s_t)$$
* Các token thuộc phản hồi của hệ thống kiểm thử được gán $w_t = 0$ (mask out).
* Các token thuộc bước nhận diện lỗi, tự phê bình và sửa đổi tư duy (Rethink tokens) được gán $w_t > 1$.
* Giúp mô hình phân khúc $\le$ 14B hấp thu được "trực giác" phát hiện lỗi mà không cần gọi MCTS bên ngoài.

#### 4.3. Tối ưu hóa Chính sách bằng GRPO với Phần thưởng Kiểm chứng (RLVR)
Sử dụng thuật toán GRPO (Group Relative Policy Optimization):
* Không cần mạng Critic (tiết kiệm bộ nhớ GPU cho mô hình 7B/14B).
* Tận dụng hàm thưởng từ kiểm thử tự động:
  $$r = \mathbb{I}(\text{Pass All Tests}) + \alpha \cdot r_{\text{format}}$$
* Tránh được hiện tượng "hack phần thưởng" (Reward Hacking) do phần thưởng kiểm thử là nhị phân và có thể xác minh được 100%.

#### 4.4. Động cơ Suy luận MCTS Gia tốc (Accelerated Test-Time Compute)
Khi gặp các bài toán cực khó ở bước suy luận cuối cùng:
* Kích hoạt lại thuật toán MCTS với phản hồi kiểm thử tự động.
* Do mô hình đã được huấn luyện qua Journey SFT + GRPO, phân phối xác suất tiên nghiệm $p(a \mid s)$ tại các nút nhánh chất lượng cao đã được cải thiện vượt bậc $\to$ MCTS chỉ cần từ 3 đến 5 lượt rollout là tìm ra mã nguồn tối ưu (so với 16 đến 32 rollouts của RethinkMCTS trên mô hình đông cứng), giúp tiết kiệm hơn 70% chi phí tính toán.

---

### 5. Kế hoạch Thực nghiệm và Tiêu chuẩn Đánh giá (Experiments & Evaluation)

#### 5.1. Môi trường Thực nghiệm & Phần cứng
* **Phần cứng:** 1 - 2 GPU NVIDIA (RTX 3090/4090 24GB hoặc A100/A5000) hỗ trợ vLLM và DeepSpeed/TRL.
* **Mô hình nền:** `Qwen2.5-Coder-7B-Instruct` (mô hình mã nguồn mở hàng đầu ở phân khúc $\le$ 14B).
* **Môi trường an toàn:** Thực thi mã trong Docker container với giới hạn tài nguyên CPU và thời gian timeout (2.0s).

#### 5.2. Các Phương pháp So sánh (Baselines)
1. **Base Models:** Qwen2.5-Coder-7B (Direct generation / CoT).
2. **Feedback-based Baselines:** Reflexion, LDB (Language Model Debugger).
3. **Tree Search-based Baselines:** RAP (Hao et al.), ToT (Tree of Thoughts), RethinkMCTS (Li et al., chạy trên model gốc).
4. **Proposed Models:**
   * *Ours (Single-Pass):* Mô hình sau Journey SFT + GRPO sinh trực tiếp.
   * *Ours (Hybrid MCTS):* Mô hình sau huấn luyện kết hợp MCTS có phản hồi kiểm thử với budget rollout nhỏ ($N=4$).

#### 5.3. Tiêu chí Đánh giá (Metrics)
* **Pass@1 (%):** Tỷ lệ bài toán giải quyết đúng hoàn toàn ngay trong lần thử đầu tiên trên tập kiểm thử ẩn (Private Tests).
* **Pass Rate (%):** Tỷ lệ phần trăm test case vượt qua trung bình trên toàn bộ bài toán.
* **Average Token Consumption:** Số lượng token trung bình tiêu tốn để giải một bài toán (đo lường tính tiết kiệm tài nguyên).
* **Rollout Convergence Rate:** Số lượt mô phỏng MCTS trung bình cần thiết để đạt mã nguồn thành công.

#### 5.4. Các Nghiên cứu Triệt tiêu (Ablation Studies)
* Đánh giá đóng góp độc lập của bước **Journey SFT** vs. **GRPO**.
* So sánh hiệu quả của việc huấn luyện trên toàn bộ hành trình (Journey Learning) so với huấn luyện chỉ trên lời giải đúng (STaR / Rejection Sampling).
* Đo lường mức giảm chi phí suy luận (Inference Token Cost) giữa RethinkMCTS truyền thống và Hybrid MCTS với mô hình đã huấn luyện.

---

### 6. Kế hoạch Triển khai Dự kiến (Roadmap)

| Giai đoạn | Thời gian | Nội dung công việc chính | Kết quả đầu ra (Deliverables) |
| :--- | :--- | :--- | :--- |
| **Giai đoạn 1** | Tuần 1 - 3 | Nghiên cứu tài liệu (RAP, RethinkMCTS, GRPO); Xây dựng môi trường sandbox kiểm thử tự động an toàn cho Python; Thiết lập baseline RethinkMCTS trên Qwen2.5-Coder-7B. | Code sandbox hoàn chỉnh; Báo cáo khảo sát phương pháp. |
| **Giai đoạn 2** | Tuần 4 - 6 | Chạy offline RethinkMCTS để thu thập dữ liệu hành trình (Journey Data Mining); Tiền xử lý dữ liệu và áp dụng Masked Loss; Thực hiện Journey SFT cho mô hình $\le$ 14B. | Bộ dữ liệu Journey Trajectories; Checkpoint mô hình sau Journey SFT. |
| **Giai đoạn 3** | Tuần 7 - 9 | Tích hợp vòng lặp RLVR với thuật toán GRPO (TRL/veRL); Tối ưu hóa policy với hàm thưởng kiểm chứng từ Unit Tests. | Checkpoint mô hình hoàn thiện sau GRPO (Ours-Model). |
| **Giai đoạn 4** | Tuần 10 - 12 | Ghép nối mô hình hoàn thiện với động cơ suy luận MCTS; Chạy thực nghiệm toàn diện trên HumanEval-Plus, MBPP-Plus, APPS; Thực hiện Ablation Studies. | Bảng số liệu thực nghiệm, biểu đồ so sánh độ chính xác và token cost. |
| **Giai đoạn 5** | Tuần 13 - 15 | Viết báo cáo toàn văn luận văn / tiểu luận; Soạn thảo slide báo cáo; Hoàn thiện mã nguồn dự án trên GitHub. | Báo cáo hoàn chỉnh, Slide thuyết trình và Source Code. |

---

### 7. Tài liệu Tham khảo Chính (References)

1. **Hao, S., Gu, Y., Ma, H., Hong, J. J., Wang, Z., Wang, D. Z., & Hu, Z. (2023).** *Reasoning with Language Model is Planning with World Model (RAP).* arXiv:2305.14992.
2. **Li, Q., Xia, W., Dai, X., Du, K., Liu, W., Wang, Y., Tang, R., Yu, Y., & Zhang, W. (2024/2025).** *RethinkMCTS: Refining Erroneous Thoughts in Monte Carlo Tree Search for Code Generation.* arXiv:2409.09584.
3. **Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Zhang, M., ... & Guo, D. (2024).** *DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO).* arXiv:2402.03300.
4. **Roitman, H. (2025/2026).** *The Hitchhiker's Guide to Agentic AI: From Foundations to Systems.* Version 1.2.2.
5. **Qin, Y., Li, X., Zou, H., et al. (2024).** *O1 Replication Journey: A Strategic Progress Report (Journey Learning).*
6. **Zhong, L., Wang, Z., & Shang, J. (2024).** *LDB: A Large Language Model Debugger via Verifying Runtime Execution Step-by-Step.* arXiv:2402.16906.
7. **Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S. (2024).** *Reflexion: Language Agents with Verbal Reinforcement Learning.* NeurIPS 2023.
8. **Hui, B., Yang, J., Cui, Z., et al. (2024).** *Qwen2.5-Coder Technical Report.* arXiv:2409.12186.
