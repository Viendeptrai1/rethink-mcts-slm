# Chương 5. Phân tích & Thảo luận Chuyên sâu

> Bám sát các mục phân tích của bài báo gốc ([Rethink_extracted.md §6 & Appendix B](../../Rethink_extracted.md)) và 4 nghiên cứu triệt tiêu trong [Proposal.md §5.3](../../Proposal.md).

## 5.1. Hiệu ứng Mở rộng Quy mô Mô hình (Model Scaling: 7B vs 14B — RQ3)

- **Trên HumanEval-164:**
  - `Qwen2.5-Coder-7B` khi gắn RethinkMCTS Dual đạt **91.46% (150/164)**, vượt qua `Qwen2.5-Coder-14B` chạy Direct (**90.24%, 148/164**).
  - `Qwen2.5-Coder-14B` khi gắn RethinkMCTS đạt **93.29% (153/164)** chỉ với trung bình **4.55 lời gọi/bài** (ít hơn cả Best-of-3: 5.77 lời gọi/bài).
- **Trên APPS-300 (Đặc biệt ở mức độ Competition & Interview):**
  - Bài báo gốc nhận xét trên GPT-3.5 vs GPT-4o-mini rằng mô hình yếu hơn hưởng lợi nhiều hơn từ RethinkMCTS.
  - Tuy nhiên, ở phân khúc **mô hình nhỏ $\le$ 14B**, kết quả thực nghiệm chỉ ra một quy luật bổ sung quan trọng:
    1. **Ở mức độ khó Competition, mô hình 7B chạm trần kiến thức thuật toán** (Direct 4.00% $\to$ MCTS Dual 5.00% $\to$ Test-only 9.00%), trong khi **14B Direct đạt 21.00%** và **14B MCTS Dual nhảy vọt lên 28.00%** (ngang bằng con số 28% của GPT-4o-mini trong Table 1 bài báo gốc!).
    2. **Ở mức độ khó Interview, MCTS tạo ra bước nhảy vọt lớn nhất (+14.00%):** Direct chỉ đạt **13.00%** (13/100), trong khi MCTS Dual đạt tới **27.00%** (27/100) — **tăng trưởng hơn gấp đôi (+107.7% tương đối)**. Điều này cho thấy với các bài toán phỏng vấn có cấu trúc logic vừa tầm, cơ chế duyệt cây và sửa tư duy lá phát huy tác dụng cứu bài mạnh mẽ nhất.
    3. **Tổng thể trên 300 bài:** RethinkMCTS Dual nâng Pass@1 từ **25.33% (76/300)** lên **36.00% (108/300)** ($\Delta = +10.67\%$, cứu thành công 42 bài mà Direct bó tay, kiểm định McNemar $\chi^2 = 18.48, p = 1.72 \times 10^{-5} \ll 0.001$). Mean Hidden Pass Rate cũng tăng tương ứng từ **38.41%** lên **53.49%** ($+15.08\%$).

---

## 5.2. Vai trò của LLM Critic & Thí nghiệm Đối đầu Self-Critic vs Cross-Critic (RQ3)

### 5.2.1. Hiện tượng *Critic Degradation* ở Mô hình Nhỏ (7B) vs Năng lực Thẩm định ở 14B
- **Bằng chứng trên 7B:** Trên APPS-300, cấu hình **Test-only (22.67%)** vượt **Dual Reward (19.00%)** tới **+3.67% Pass@1**. Ngược lại, trên HumanEval-164 (nơi chỉ có rất ít `given_tests`), 7B Dual (**91.46%**) lại cao hơn 7B Test-only (**89.63%**).
- **Giải thích gắn với lý thuyết bài báo gốc (Paper §6, trang 6):**
  - Bài báo gốc chỉ ra Dual Evaluation đặc biệt quan trọng khi số lượng public tests ít (như HumanEval).
  - Khi số lượng public tests nhiều hơn (như cấu hình `half` của 7B trên APPS), bản thân $v_{\text{test}}$ đã đủ tính phân loại; lúc này điểm tự chấm $v_{\text{llm}}$ của mô hình nhỏ 7B bị nhiễu sẽ làm lệch thứ tự chọn ứng viên.

### 5.2.2. Thí nghiệm Thực chứng Đối đầu: Self-Critic (Qwen2.5-Coder-14B) vs Cross-Critic (Mistral Codestral) ✅
*(Trích xuất từ kết quả thực nghiệm chuẩn hóa trên toàn bộ 161 lượt kích hoạt Critic của APPS-300 tại [`runs/cross_critic_analysis_14b/summary.json`](../../runs/cross_critic_analysis_14b/summary.json))*

Để kiểm tra giả thuyết: *"Liệu một mô hình độc lập bên ngoài (Cross-Critic) có khách quan hơn và ít bị thiên kiến tự xác nhận (Confirmation Bias) hơn so với việc mô hình tự đánh giá code của chính nó (Self-Critic) hay không?"*, chúng tôi cho mô hình chuyên biệt mã nguồn hàng đầu thế giới **Mistral Codestral (`codestral-latest`)** đánh giá chéo độc lập trên chính xác cùng một prompt và 161 ứng viên mã đã vượt qua 100% public tests do Qwen2.5-Coder-14B sinh ra.

#### Bảng 5.2. So sánh Năng lực Thẩm định: Self-Critic (Qwen-14B) vs Cross-Critic (Codestral)

| Chỉ số Thống kê | Self-Critic (Qwen2.5-Coder-14B) | Cross-Critic (Mistral Codestral) | Nhận xét & Ý nghĩa Thống kê |
| :--- | :---: | :---: | :--- |
| **Hệ số Tương quan Hạng Spearman ($\rho$)** | **+0.2426** ($p = 0.0019$) | +0.0327 ($p = 0.6806$) | **Qwen-14B có ý nghĩa thống kê vượt bậc ($p < 0.01$)**, Codestral không có tương quan. |
| **Hệ số Tương quan Tuyến tính Pearson ($r$)** | **+0.1699** ($p = 0.0312$) | -0.0556 ($p = 0.4838$) | **Qwen-14B đạt $p < 0.05$**, Codestral hơi âm nhẹ do quá tập trung điểm trần 1.0. |
| **Tương quan Point-Biserial ($r_{\text{pb}}$ với Hidden Pass)** | **+0.2391** ($p = 0.0023$) | -0.0417 ($p = 0.5997$) | Điểm chấm của Qwen-14B dự đoán chính xác xác suất pass 100% test ẩn. |
| **Phân phối Điểm chấm ($v_{\text{llm}}$)** | 1.0: 121 · **-1.0: 35** · Khác: 5 | 1.0: 145 (90.1%) · -1.0: 5 · Khác: 11 | **Codestral bị bão hòa trần (Sycophancy)**: Cho điểm tuyệt đối 90.1% số lần. |
| **Tỷ lệ Phê duyệt Sai trên 62 bài Quá khớp (Overfit)** | **64.52%** (Bắt trúng 22 bài sai) | **95.16%** (Bỏ sót 59/62 bài sai) | Qwen-14B khắt khe và phát hiện lỗi biên tốt hơn gấp **7.3 lần** so với Codestral. |
| **Tỷ lệ Phê duyệt Đúng trên 99 bài Pass Ẩn** | 84.85% (84/99 bài) | 92.93% (92/99 bài) | Codestral do chấm điểm quá dễ dãi nên tỷ lệ pass cao nhưng mất tính phân loại. |

#### 🧠 Thảo luận & Phát hiện Khoa học Giá trị:
1. **Lợi thế Đồng bộ Không gian Suy luận Nội tại (Internal Reasoning Alignment):**
   - Trái với trực giác ban đầu rằng mô hình ngoài sẽ khách quan hơn, kết quả thực nghiệm cho thấy **mô hình tự sinh mã lại có năng lực phát hiện lỗi biên của chính mình tốt hơn**. Do Qwen2.5-Coder-14B tự sinh ra cây tư duy (`reasoning_path`), khi đóng vai trò Critic đọc lại suy luận và mã của chính mình, nó nhận diện được những bước tư duy "gượng ép" hoặc giả định mong manh mà nó đã tạo ra ở các bước trước, từ đó chấm điểm phạt $-1.0$ (chặn đứng 22 trường hợp quá khớp).
2. **Hội chứng Cả tin Bề mặt (Sycophancy & Surface-Level Plausibility) của Mô hình Ngoài:**
   - Khi một mô hình bên ngoài (Codestral) tiếp nhận một đoạn mã đã định dạng đẹp đẽ kèm tiền đề *"Mã đã vượt qua toàn bộ kiểm thử công khai"*, nó chỉ phân tích ngữ nghĩa bề mặt (Surface-level semantic check). Do không tham gia vào quá trình khám phá cây MCTS và không biết các nhánh lỗi trước đó, Codestral dễ dàng tin tưởng rằng mã đã hoàn thiện, dẫn đến hiện tượng **nịnh bợ / cả tin (Sycophancy)** với 90.1% điểm trần và để lọt tới 95.16% số bài quá khớp!
3. **Đóng góp cho Thiết kế Hệ thống Đa Tác nhân (Multi-Agent Systems):**
   - Kết quả này mang lại khuyến nghị khoa học đắt giá: Khi thiết kế mạng Critic thẩm định trong tìm kiếm cây, **không nên giao phó cho một LLM ngoài đọc mã chay**, mà Critic bên ngoài bắt buộc phải có môi trường sinh ca kiểm thử nghịch đảo (Counterexample Generation) hoặc Symbolic Execution thì mới khắc phục được thiên kiến nịnh bợ bề mặt.

---

## 5.3. Nghiên cứu Triệt tiêu các Thành phần Tìm kiếm (Component Ablations — RQ2)

Đối chiếu với **Figure 3 & 6, Table 4** của bài báo gốc và **Mục 5.3 của Đề cương (`Proposal.md`)**:

| Mã Ablation | Cấu hình so sánh (Full 300 bài APPS) | Nguồn trong Paper / Proposal | Trạng thái |
| :--- | :--- | :--- | :--- |
| **Ablation 1: Critic** | Dual $(0.8, 0.2)$ vs Test-only $(1.0, 0.0)$ | Paper Fig. 3 (`w/o selfEval`), Proposal §5.3 | ✅ Có trên 7B; ⏳ Full 300 bài 14B ([E3](EXPERIMENT_CHECKLIST.md)) |
| **Ablation 2: Rethink** | Có Rethink (`max_rethinks=2`) vs Không Rethink (`max_rethinks=0`) | Paper Fig. 3 (`w/o rethink`) & Table 4 | ⏳ Full 300 bài ([E4](EXPERIMENT_CHECKLIST.md)) |
| **Ablation 3: Mức Feedback** | `block` (CFG) vs `trace` (`w/o blockInfo`) vs `facts_only` | Paper Fig. 3, Proposal §5.3 (Ablation 1), RQ1 | ⏳ Full 300 bài ([E6](EXPERIMENT_CHECKLIST.md)) |
| **Ablation 4: Backup Policy** | Max Backup ($Q = \max$) vs Mean Backup (`search.backup=mean`) | Proposal §5.3 (Ablation 2) | ⏳ Full 300 bài ([E10](EXPERIMENT_CHECKLIST.md)) |

> **Chỉ số bổ sung không tốn GPU (Paper Table 4 — [A3](EXPERIMENT_CHECKLIST.md)):**
> Ngoài Pass@1 trên tập ẩn, bài báo gốc (Table 4) còn đo **tỷ lệ ứng viên mã hợp lệ trên toàn bộ cây tìm kiếm** (số candidate đạt $v_{\text{test}} = 1.0$ chia tổng số candidate sinh ra). Chỉ số này trích xuất được ngay từ `evaluations.json` của 300 bài 14B!

---

## 5.4. RethinkMCTS vs Sửa lỗi Tuần tự (Iterative Repair / Reflection — Paper Table 2)

- Trong bài báo gốc (Table 2), thay thế *Rethink* bằng *Reflection* làm giảm Pass@1 và làm tăng mạnh lượng token tiêu thụ do tích lũy lịch sử lỗi.
- Trong báo cáo của ta:
  - Chạy `--solver iterative_repair` trên toàn bộ **300 bài APPS** ([E5](EXPERIMENT_CHECKLIST.md)).
  - Đo **tỷ lệ lặp lại mã lỗi (`duplicate code_hash`)** và **tỷ lệ tụt lùi (`pass_rate regression`)** giữa các bước sửa ([A4](EXPERIMENT_CHECKLIST.md)).

---

## 5.5. Phân tích Loại Lỗi & Động học Sửa lỗi (Error Taxonomy & Repair Dynamics — [A3](EXPERIMENT_CHECKLIST.md))

Trích xuất trực tiếp từ 300 bài của `runs/benchmark_14b_batch_*` (không tốn GPU):
1. **Phân phối lỗi ở ứng viên đầu tiên (Rollout 0, trước khi Rethink):**
   - Bao nhiêu % bài pass ngay ở lần sinh đầu tiên (không cần rethink)?
   - Bao nhiêu % gặp `SyntaxError / CompilationError`, `RuntimeError`, `TimeLimitExceeded`, `WrongAnswer`?
2. **Xác suất cứu vãn thành công (Rethink Recovery Rate):**
   - Trong số các bài thất bại ở ứng viên đầu tiên nhưng kích hoạt `rethink` (trung bình 3.45 lần/bài), có bao nhiêu bài chuyển từ `Fail` $\to$ `Pass Public` và `Pass Hidden`?
   - Loại lỗi nào được CFG Block Analysis + Rethink sửa hiệu quả nhất?
3. **Hiện tượng Quá khớp Kiểm thử Công khai (Public Overfitting Gap):**
   - Trong **160/300 bài** vượt qua 100% public tests (2 test đầu) trên 14B, chỉ có **108/300 bài** vượt qua 100% hidden tests $\to$ **52 bài (32.5% số bài pass public)** bị overfit hoặc thiếu trường hợp biên ẩn! Đây là con số cực kỳ thuyết phục để bàn luận trong Chương 5.

---

## 5.6. Đường cong Mở rộng tại Thời điểm Suy luận (Test-Time Scaling Curve — Proposal Ablation 3 & Paper Fig. 5)

- **Cách dựng đường cong ngay từ dữ liệu sẵn có ([A6](EXPERIMENT_CHECKLIST.md) — Không tốn GPU!):**
  Trong mỗi bài của `runs/benchmark_14b_batch_*`, file `candidates.jsonl` và `evaluations.json` lưu thứ tự thời gian của từng ứng viên mã sinh ra ($k = 1, 2, \dots, 16$). Ta có thể vẽ đường cong **Pass@1 và Public Pass Rate theo ngân sách số lần sinh mã $k \in \{1, 2, 4, 8, 16\}$** (Any-time Performance Curve), chứng minh sự tăng trưởng ổn định khi cấp thêm ngân sách tìm kiếm!

---

## 5.7. Nghiên cứu Tình huống Điển hình (Qualitative Case Studies — Paper Appendix C.5 & C.6)

Chọn từ dữ liệu thật trong `runs/benchmark_14b_batch_*` ([A7](EXPERIMENT_CHECKLIST.md)):
1. **Case Study 1 (Thành công nhờ Block Analysis + Rethink):** 1 bài toán mà ứng viên đầu tiên bị `WrongAnswer` hoặc `IndexError`, CFG trace chỉ ra đúng biến bị sai trong vòng lặp, bước `rethink` sửa lại tư duy tại lá và ứng viên tiếp theo đạt 100% hidden tests (kèm ảnh chụp cây từ **Trace Viewer**).
2. **Case Study 2 (Thành công nhờ 14B vượt 7B ở bài Competition):** 1 bài Competition mà 7B thất bại nhưng 14B phân rã đúng thuật toán quy hoạch động / đồ thị.
3. **Case Study 3 (Thất bại điển hình — Public Overfitting):** 1 trong 52 bài pass cả 2 public tests nhưng trượt hidden test (ví dụ do TLE với input lớn hoặc thiếu corner case $N=0$), minh họa giới hạn của bộ kiểm thử công khai ít mẫu.
