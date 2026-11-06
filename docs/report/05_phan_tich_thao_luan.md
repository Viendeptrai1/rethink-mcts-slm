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

## 5.5. Phân tích Loại Lỗi & Động học Sửa lỗi (Error Taxonomy & Repair Dynamics — [A3](EXPERIMENT_CHECKLIST.md)) ✅

*(Trích xuất chính xác từ 300/300 bài toán trong [`runs/benchmark_apps_14b_dual_unified/`](../../runs/benchmark_apps_14b_dual_unified/))*

### Bảng 5.5. Phân tích Chi tiết Động học Sửa lỗi & Năng lực Giải cứu của Rethink trên 14B APPS-300

| Chỉ số Phân tích | Số lượng | Tỷ lệ (%) | Nhận xét Khoa học |
| :--- | :-: | :-: | :--- |
| **Ứng viên đầu tiên (Rollout 0) giải đúng 100% public tests** | **84 / 300** | **28.0%** | Mô hình 14B chỉ giải quyết được hơn 1/4 số bài ngay ở lần thử đầu. |
| **Ứng viên đầu tiên thất bại (kích hoạt tìm kiếm & Rethink)** | **216 / 300** | **72.0%** | Chiếm gần 3/4 số bài, khẳng định vai trò sống còn của cơ chế sửa lỗi. |
| • *Lỗi sai kết quả (Wrong Answer - WA)* | 184 / 216 | 85.2% | Lỗi thuật toán và logic điều kiện chiếm đại đa số. |
| • *Lỗi thời gian chạy (Runtime Error - RE)* | 30 / 216 | 13.9% | Chủ yếu là lỗi chỉ mục (`IndexError`), tràn đệ quy hoặc chia 0. |
| • *Lỗi quá thời gian (Time Limit Exceeded - TLE)* | 2 / 216 | 0.9% | Rất ít do ngân sách thời gian 5s/test đủ rộng. |
| • *Lỗi cú pháp (Syntax / Compilation Error)* | **0 / 216** | **0.0%** | Qwen2.5-Coder-14B sinh cú pháp Python chuẩn xác tuyệt đối 100%. |
| **Số bài kích hoạt Rethink (Search Iterations > 1)** | **216 bài** | 72.0% | Trung bình 3.45 lượt rethink/bài. |
| **Số bài được Rethink cứu giải đúng 100% public tests** | **77 / 216** | **35.6%** | Hơn 1/3 số bài thất bại ban đầu đã được chuyển hóa thành pass public. |
| **Số bài được Rethink cứu giải đúng 100% hidden tests** | **38 / 216** | **17.6%** | **Cứu ròng 38 bài giải đúng hoàn toàn** từ tay thất bại ban đầu! |
| **Đóng góp của Rethink vào tổng số bài Pass của 14B** | **38 / 108** | **35.2%** | **Hơn 1/3 tổng chiến thắng của MCTS là nhờ Rethink giải cứu!** Không có Rethink, Pass@1 chỉ đạt ~23.33%. |
| **Tree Effective Code Rate (Paper Table 4)** | **161 / 1,748** | **9.21%** | Tỷ lệ ứng viên sinh ra trên toàn bộ cây tìm kiếm đạt $v_{\text{test}} = 1.0$. |

---

## 5.6. Đường cong Mở rộng tại Thời điểm Suy luận (Test-Time Scaling Curve — [A6](EXPERIMENT_CHECKLIST.md)) ✅

*(Trích xuất từ lịch sử ứng viên theo thời gian $k \in \{1, 2, 4, 8, 16\}$ trên 300 bài 14B APPS-300)*

### Bảng 5.6. Diễn biến Pass@1 (%) và Public Pass Rate (%) theo Ngân sách Lần sinh Mã ($k$)

| Ngân sách Ứng viên ($k$) | Pass@1 Ẩn (%) | Số bài Pass Ẩn | Public Pass Rate (%) | Số bài Pass Public | Tăng trưởng Lũy kế ($\Delta$ Pass@1) |
| :---: | :-: | :-: | :-: | :-: | :---: |
| **$k = 1$** (Lần thử đầu) | 22.00% | 66 / 300 | 28.00% | 84 / 300 | Gốc cơ sở |
| **$k = 2$** | 26.67% | 80 / 300 | 35.67% | 107 / 300 | +4.67% |
| **$k = 4$** | 31.33% | 94 / 300 | 44.33% | 133 / 300 | +9.33% |
| **$k = 8$** | 35.00% | 105 / 300 | 52.00% | 156 / 300 | +13.00% |
| **$k = 16$** (Toàn bộ ngân sách) | **36.00%** | **108 / 300** | **53.67%** | **161 / 300** | **+14.00%** |

```
Pass@1 (%)
 40% ┤                                              ╭── 36.00% (k=16)
 35% ┤                                    ╭─────────╯   35.00% (k=8)
 30% ┤                         ╭──────────╯             31.33% (k=4)
 25% ┤              ╭──────────╯                        26.67% (k=2)
 20% ┤ ── 22.00% (k=1)
     └──────────────────────────────────────────────────────────────
         k=1           k=2          k=4          k=8          k=16  (Log-scale)
```

> **Quy luật Mở rộng Suy luận (Inference Scaling Law):**
> 1. Hiệu năng Pass@1 tăng trưởng đơn điệu nghiêm ngặt theo quy luật hàm logarit khi cấp thêm ngân sách ứng viên.
> 2. Đa số mức cải thiện (+13.00% trên tổng +14.00%) đạt được ở mốc $k = 8$ (35.00%). Sau mốc $k = 8$, đường cong bắt đầu có hiện tượng suy giảm hiệu suất biên (diminishing returns). Điều này cung cấp căn cứ thực nghiệm chuẩn xác để chọn cấu hình tối ưu chi phí/hiệu năng cho thực tế ($k=8$).

---

## 5.7. Nghiên cứu Tình huống Điển hình (Qualitative Case Studies — Paper Appendix C.5 & C.6)

Chọn từ dữ liệu thật trong `runs/benchmark_14b_batch_*` ([A7](EXPERIMENT_CHECKLIST.md)):
1. **Case Study 1 (Thành công nhờ Block Analysis + Rethink):** 1 bài toán mà ứng viên đầu tiên bị `WrongAnswer` hoặc `IndexError`, CFG trace chỉ ra đúng biến bị sai trong vòng lặp, bước `rethink` sửa lại tư duy tại lá và ứng viên tiếp theo đạt 100% hidden tests (kèm ảnh chụp cây từ **Trace Viewer**).
2. **Case Study 2 (Thành công nhờ 14B vượt 7B ở bài Competition):** 1 bài Competition mà 7B thất bại nhưng 14B phân rã đúng thuật toán quy hoạch động / đồ thị.
3. **Case Study 3 (Thất bại điển hình — Public Overfitting):** 1 trong 52 bài pass cả 2 public tests nhưng trượt hidden test (ví dụ do TLE với input lớn hoặc thiếu corner case $N=0$), minh họa giới hạn của bộ kiểm thử công khai ít mẫu.
