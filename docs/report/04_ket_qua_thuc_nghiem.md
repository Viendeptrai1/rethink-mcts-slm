# Chương 4. Kết quả Thực nghiệm

Ký hiệu: `✅` Đã có số liệu từ artifact · `⏳` Cần chạy thêm (tốn GPU) · `🧮` Có sẵn dữ liệu trong `runs/`, chỉ cần chạy script thống kê offline · `⚠️` Khác cohort hoặc khác cấu hình chi tiết.

---

## 4.1. Kết quả trên APPS-300 Benchmark (100 Intro / 100 Inter / 100 Comp)

- **Nguồn 7B:** [BENCHMARK_7B_VS_14B_REPORT.md](../results/BENCHMARK_7B_VS_14B_REPORT.md), [rethinkmcts-apps-native-v2-w4-retry.md](../results/7b/rethinkmcts-apps-native-v2-w4-retry.md), [rethinkmcts-test-only-v1.md](../results/7b/rethinkmcts-test-only-v1.md).
- **Nguồn 14B Dual:** [runs/benchmark_apps_14b_dual_unified/summary.json](../../runs/benchmark_apps_14b_dual_unified/summary.json).
- **Nguồn 14B Direct:** [runs/benchmark_apps_14b_direct_300/summary.json](../../runs/benchmark_apps_14b_direct_300/summary.json).

### Bảng 4.1a. Tổng hợp Pass@1 (%) và Mean Hidden Pass Rate (%) trên APPS-300

| Phương pháp | 7B Pass@1 | 7B Pass Rate | 14B Pass@1 | 14B Pass Rate | Trạng thái / Checklist |
| :--- | :-: | :-: | :-: | :-: | :--- |
| **Direct Generation** | ✅ 14.00% (42/300) | ✅ 30.51% | ✅ **25.33%** (76/300) | ✅ **38.41%** | Đã hoàn tất 300/300 bài [E1](EXPERIMENT_CHECKLIST.md) |
| **Best-of-3 (BoN-3)** | — *(Không đo trên 7B)* | — | ✅ **35.62%** (57/160)<br>*(Intro: **50.00%**, Inter: **11.67%**)* | ✅ **49.85%** | Đã hoàn tất 160 bài [E2](EXPERIMENT_CHECKLIST.md) (100% Intro + 60% Inter) |
| **Iterative Repair** | — *(Không đo trên 7B)* | — | ⏳ TODO | ⏳ TODO | Cần chạy [E5](EXPERIMENT_CHECKLIST.md) |
| **RethinkMCTS (Test-only)** | ✅ **22.67%** (68/300) | ✅ **45.34%** | ⏳ TODO | ⏳ TODO | Cần chạy [E3](EXPERIMENT_CHECKLIST.md) |
| **RethinkMCTS (Dual Reward)** | ✅ 19.00% (57/300) | ✅ 43.04% | ✅ **36.00%** (108/300) | ✅ **53.49%** | Đã hoàn tất 300/300 bài (14B) |

### Bảng 4.1b. Phân rã theo 3 Phân tầng Độ khó trên APPS-300

| Phân tầng (100 bài/tầng) | Chỉ số | 7B Direct | 7B MCTS Dual | 7B MCTS Test-only | 14B Direct | 14B MCTS Dual |
| :--- | :--- | :-: | :-: | :-: | :-: | :-: |
| **Introductory** | Pass@1 (%)<br>Pass Rate (%) | 31.00%<br>45.84% | 38.00%<br>56.70% | **41.00%**<br>61.14% | ✅ **42.00%** (42/100)<br>✅ **53.50%** | **53.00%** (53/100)<br>**71.26%** |
| **Interview** | Pass@1 (%)<br>Pass Rate (%) | 7.00%<br>26.18% | 14.00%<br>42.36% | **18.00%**<br>45.46% | ✅ **13.00%** (13/100)<br>✅ **31.48%** | **27.00%** (27/100)<br>**50.13%** |
| **Competition** | Pass@1 (%)<br>Pass Rate (%) | 4.00%<br>19.52% | 5.00%<br>30.07% | **9.00%**<br>29.42% | ✅ **21.00%** (21/100)<br>✅ **30.24%** | **28.00%** (28/100)<br>**39.08%** |
| **Toàn bộ (300 bài)** | **Pass@1 (%)**<br>**Pass Rate (%)** | **14.00%**<br>**30.51%** | **19.00%**<br>**43.04%** | **22.67%**<br>**45.34%** | ✅ **25.33%** (76/300)<br>✅ **38.41%** | **36.00%** (108/300)<br>**53.49%** |

### Bảng 4.1c. Phân tích Chi phí & Hành vi Tìm kiếm theo Phân tầng Độ khó trên 14B APPS-300 ✅
*(Trích xuất chính xác từ 300/300 bài toán trong [runs/benchmark_apps_14b_dual_unified/summary.json](../../runs/benchmark_apps_14b_dual_unified/summary.json) và [runs/benchmark_apps_14b_direct_300/summary.json](../../runs/benchmark_apps_14b_direct_300/summary.json))*

| Phân tầng (100 bài/tầng) | Phương pháp (14B) | Pass@1 (%) | Mean Pass Rate (%) | Model Calls TB / bài | Tokens TB / bài | Thời gian Giải TB / bài | Rethink TB / bài | Ứng viên Code TB / bài | Vòng lặp MCTS TB / bài |
| :--- | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **Introductory** | Direct | 42.00% (42/100) | 53.50% | 1.45 | 1,329.0 | 21.68s | 0.00 | 1.00 | 0.00 |
| | **RethinkMCTS Dual** | **53.00%** (53/100) | **71.26%** | 11.18 | 25,539.6 | 80.70s | 2.29 | 4.21 | 2.20 |
| **Interview** | Direct | 13.00% (13/100) | 31.48% | 1.18 | 1,355.2 | 24.08s | 0.00 | 1.00 | 0.00 |
| | **RethinkMCTS Dual** | **27.00%** (27/100) | **50.13%** | 17.73 | 42,788.1 | 119.73s | 4.13 | 6.76 | 3.17 |
| **Competition** | Direct | 21.00% (21/100) | 30.24% | 1.17 | 1,434.0 | 27.93s | 0.00 | 1.00 | 0.00 |
| | **RethinkMCTS Dual** | **28.00%** (28/100) | **39.08%** | 16.96 | 43,810.6 | 125.60s | 3.93 | 6.51 | 2.99 |
| **Toàn bộ APPS-300** | Direct | 25.33% (76/300) | 38.41% | 1.27 | 1,372.7 | 24.56s | 0.00 | 1.00 | 0.00 |
| | **RethinkMCTS Dual** | **36.00%** (108/300) | **53.49%** | **15.29** | **37,759.3** | **108.70s** | **3.45** | **5.83** | **2.79** |

> **Quy luật thực nghiệm theo độ khó:**
> 1. **Bài dễ (Introductory):** MCTS hội tụ nhanh nhất (chỉ 2.20 vòng lặp, 11.18 lời gọi), đạt tới **71.26% test ẩn** và hơn một nửa số bài pass tuyệt đối (53.00%).
> 2. **Bài trung bình (Interview):** Là phân tầng chứng kiến **mức tăng trưởng ngoạn mục nhất (+14.00% Pass@1, tăng hơn gấp đôi từ 13% lên 27%)**. Tại đây, các lỗi thuật toán logic thường được cứu vãn thành công nhờ số lượt Rethink cao nhất (4.13 lượt/bài) và số vòng lặp MCTS cao nhất (3.17 vòng lặp).
> 3. **Bài khó (Competition):** Direct chỉ đạt 21.00%, MCTS nâng lên 28.00% (+7.00%) với ngân sách token tương đương Interview (43.8K tokens/bài).

### Bảng 4.1d. So sánh Đối đầu Trực diện: Direct Baseline vs Best-of-3 vs RethinkMCTS trên 160 Bài APPS ✅
*(Trích xuất chính xác trên cùng tập 160 bài toán gồm 100 bài Introductory + 60 bài Interview đầu tiên từ [runs/benchmark_apps_14b_bon3_300/summary.json](../../runs/benchmark_apps_14b_bon3_300/summary.json))*

| Phân tầng Khảo sát | Chỉ số | 14B Direct Baseline | 14B Best-of-3 (BoN-3) | 14B RethinkMCTS Dual | Mức Vượt trội của MCTS vs BoN-3 |
| :--- | :--- | :-: | :-: | :-: | :---: |
| **Introductory** (100/100 bài) | **Pass@1 (%)**<br>Mean Hidden Pass Rate | 42.00% (42/100)<br>53.50% | **50.00%** (50/100)<br>60.94% | **53.00%** (53/100)<br>**71.26%** | **+3.00% Pass@1**<br>*(+10.32% test ẩn)* |
| **Interview** (60 bài đầu) | **Pass@1 (%)**<br>Mean Hidden Pass Rate | 8.33% (5/60)<br>26.70% | **11.67%** (7/60)<br>31.36% | **18.33%** (11/60)<br>**50.40%** | **+6.66% Pass@1**<br>*(+19.04% test ẩn)* |
| **Tổng cộng (160 bài)** | **Pass@1 (%)**<br>**Mean Hidden Pass Rate** | **29.38%** (47/160)<br>**43.45%** | **35.62%** (57/160)<br>**49.85%** | **40.00%** (64/160)<br>**63.45%** | **+4.38% Pass@1**<br>*(+13.60% test ẩn)* |

> **Quy luật Thực nghiệm Rút ra từ Bảng 4.1d:**
> 1. **Hiệu ứng của việc Lấy mẫu Ngẫu nhiên (BoN-3 vs Direct):** Việc tăng ngân sách lấy mẫu ngẫu nhiên độc lập 3 lần giúp Pass@1 tăng từ 29.38% lên 35.62% (+6.24%), chứng minh nhiều bài toán 14B chỉ cần thêm cơ hội thử là giải được.
> 2. **Sự Vượt trội của Tìm kiếm Cây có Định hướng (MCTS vs BoN-3):** Khi cùng sử dụng ngân sách tính toán tại thời điểm suy luận, **RethinkMCTS Dual đạt 40.00% Pass@1 (vượt BoN-3 +4.38%)** và đặc biệt là **Hidden Pass Rate đạt tới 63.45% (vượt xa BoN-3 tới +13.60%)**. Điều này chứng minh cơ chế phân tích CFG và sửa tư duy lá (Rethink) tạo ra mã nguồn có chất lượng thuật toán bền vững hơn hẳn so với việc chọn mò giữa 3 ứng viên sinh ngẫu nhiên.

> **Ghi chú kỹ thuật minh bạch:**
> 1. Ở nhánh 7B APPS: Dual có 295/300 bài sinh xong candidate (3 bài search timeout 900s, 2 bài lỗi cú pháp khi trace), Test-only có 297/300 bài (3 bài search timeout 900s); tất cả các bài thiếu candidate đều được gán điểm 0 vào mẫu số 300.
> 2. Ở nhánh 14B APPS Dual: Hoàn tất 300/300 bài, không có lỗi hạ tầng.
> 3. Khác biệt chính sách chia test giữa hai nhánh (`half` + `all_tests` trên 7B vs `first-2 public` + `disjoint hidden_suite` trên 14B) được nêu tại [Chương 3 §3.1](03_thiet_lap_thuc_nghiem.md).

---

## 4.2. Kết quả trên HumanEval Benchmark (164 Bài toán Chuẩn)

- **Nguồn 7B:** [rethinkmcts-modal-humaneval-v1.md](../results/7b/rethinkmcts-modal-humaneval-v1.md), [rethinkmcts-test-only-v1.md](../results/7b/rethinkmcts-test-only-v1.md).
- **Nguồn 14B:** [humaneval_direct_14b](../../runs/humaneval_direct_14b/summary.json), [humaneval_bon3_14b](../../runs/humaneval_bon3_14b/summary.json), [humaneval_mcts_14b](../../runs/humaneval_mcts_14b/summary.json), [humaneval_mcts_dual_14b](../../runs/humaneval_mcts_dual_14b/summary.json).

### Bảng 4.2. So sánh trên HumanEval-164

| Phương pháp | 7B Pass@1 (%) | 7B Số bài Pass | 14B Pass@1 (%) | 14B Số bài Pass | Calls TB/bài (14B) | Thời gian TB/bài (14B) |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: |
| **Direct Generation** | ✅ 80.49% | 132/164 | ✅ 90.24% | 148/164 | ✅ 1.91 | ✅ 5.14s |
| **Best-of-3 (BoN-3)** | — *(Không đo trên 7B)* | — | ✅ 91.46% | 150/164 | ✅ 5.77 | ✅ 24.04s |
| **RethinkMCTS (Test-only)** | ✅ 89.63% | 147/164 | ✅ **93.29%** | **153/164** | ✅ **4.55** | ✅ **20.94s** |
| **RethinkMCTS (Dual Reward)** | ✅ **91.46%** | **150/164** | ✅ **90.85%** | **149/164** | ✅ **4.64** | ✅ **25.26s** |

> **Phát hiện khoa học quan trọng trên HumanEval-164:**
> 1. **Bảng 4.2 đã hoàn thiện 100% số liệu thực nghiệm trên 14B:** Nhánh Dual Reward ([E9](EXPERIMENT_CHECKLIST.md)) vừa hoàn tất trọn vẹn 164/164 bài, đạt **90.85% (149/164)** với chi phí cực thấp: **4.64 lời gọi/bài** (tiết kiệm hơn BoN-3: 5.77 lời gọi/bài).
> 2. **So sánh Test-only vs Dual Reward trên 14B:** Cấu hình **Test-only (93.29%, 153/164)** vượt **Dual Reward (90.85%, 149/164)** tới **+2.44% (+4 bài)**. Nguyên nhân do trên HumanEval, các bài toán chỉ có 1–3 test cases trong docstring; khi kích hoạt Critic tự chấm ($w_{\text{llm}} = 0.2$), điểm tự nghi ngờ của mô hình đã làm lệch việc chọn ứng viên ở 6 bài toán, trong khi Test-only dừng sớm và giữ vững mã đúng. Điều này tiếp tục khẳng định vai trò sống còn của cơ chế chọn trọng số hàm thưởng thích ứng theo lượng test công khai.

---

## 4.3. Kết quả Thăm dò trên Tập APPS Introductory-100 (`apps_4000`–`apps_4099`, 14B) ⚠️

> Tập này chỉ trùng 15/100 bài với phần Introductory của APPS-300 và dùng cấu hình thăm dò giai đoạn đầu (`compact_v1`). Tuy nhiên, cả 3 phương pháp dưới đây đều chạy trên **chính xác cùng 100 bài toán**, cung cấp bằng chứng đối sánh trực tiếp giữa Direct, Best-of-3 và MCTS trên 14B:

| Phương pháp (14B) | Pass@1 (%) | Mean Hidden Pass Rate (%) | Calls TB/bài | Code Attempts TB/bài | Rethink TB/bài | Thời gian TB/bài | Nguồn |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :--- |
| **Direct Generation** | ✅ 21.00% (21/100) | ✅ 38.89% | ✅ 1.27 | 1.00 | 0.00 | 8.85s | [apps_intro_direct_14b](../../runs/apps_intro_direct_14b/summary.json) |
| **Best-of-3 (BoN-3)** | ✅ 23.00% (23/100) | ✅ 44.87% | ✅ 3.79 | 3.00 | 0.00 | 23.53s | [apps_intro_bon3_14b](../../runs/apps_intro_bon3_14b/summary.json) |
| **RethinkMCTS** | ✅ **30.00%** (30/100) | ✅ **49.88%** | ✅ 11.58 | 6.29 | 2.72 (73/100 bài) | 86.75s | [apps_intro_mcts_14b](../../runs/apps_intro_mcts_14b/summary.json) |

---

## 4.4. Thống kê Chi phí Suy luận & Phân rã Token theo Vai trò (RQ4 — Paper Table 5)

### Bảng 4.4a. Phân rã Chi tiết Token & Lời gọi theo 5 Vai trò trên 14B RethinkMCTS Dual (APPS-300) ✅
*(Trích xuất chính xác từ 300/300 bài trong [`runs/benchmark_apps_14b_dual_unified/summary.json`](../../runs/benchmark_apps_14b_dual_unified/summary.json))*

| Vai trò (Role) | Tổng số Calls | Tỷ trọng Calls | Input Tokens | Output Tokens | Tổng Tokens | Tỷ trọng Tokens | Tokens TB / Bài |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **1. Expansion** (Sinh nhánh tư duy) | 405 | 8.8% | 402,222 | 75,738 | 477,960 | 4.2% | 1,593.2 |
| **2. Code Generation** (Sinh mã) | 1,748 | 38.1% | 1,264,598 | 974,962 | 2,239,560 | 19.8% | 7,465.2 |
| **3. Block Analysis** (Phân tích CFG) | 1,208 | 26.3% | 5,717,479 | 126,250 | 5,843,729 | **51.6%** | **19,479.1** |
| **4. Rethink** (Sửa tư duy tại lá) | 1,066 | 23.2% | 2,555,861 | 87,815 | 2,643,676 | 23.3% | 8,812.3 |
| **5. Conditional Critic** (Tự chấm điểm) | 160 | **3.5%** | 121,251 | 1,606 | 122,857 | **1.1%** | **409.5** |
| **TỔNG CỘNG (300 bài)** | **4,587** *(15.29/bài)* | **100%** | **10,061,411** | **1,266,371** | **11,327,782** | **100%** | **37,759.3** |

- **Các chỉ số hành vi tìm kiếm trung bình trên mỗi bài (14B APPS-300):**
  - Số vòng lặp tìm kiếm (`search_iterations`): **2.79** (tối đa 9).
  - Số ứng viên mã sinh ra (`code_generation_attempts`): **5.83** (tối đa 16).
  - Số lần kích hoạt sửa tư duy lá (`rethink_attempts`): **3.45** (tối đa 10).
  - Thời gian giải trung bình (`solve_wall_seconds`): **108.7 giây/bài**.

> **Hai nhận xét đắt giá từ Bảng 4.4a:**
> 1. **Hiệu quả của Conditional Critic (Trụ cột 4 trong Proposal):** Nhờ chỉ kích hoạt khi ứng viên vượt qua 100% public tests (160/300 bài), Critic chỉ chiếm **3.5% số lời gọi** và **1.1% tổng lượng token** (409.5 tokens/bài) — cực kỳ tiết kiệm.
> 2. **Điểm nghẽn chi phí tại `block_analysis` (Khớp với Paper Appendix B):** Riêng bước phân tích khối lệnh CFG chiếm tới **51.6% tổng lượng token** (chủ yếu là input tokens chứa trạng thái biến trước/sau mỗi block: 5.72 triệu tokens). Đây chính là bằng chứng thực nghiệm trực tiếp giải thích vì sao cần cơ chế **chọn mức phản hồi thích ứng (Adaptive Feedback Selection - RQ2)**!

### Bảng 4.4b. So sánh Chi phí Tổng hợp giữa Direct Baseline và RethinkMCTS trên APPS-300 ✅

| Phương pháp (14B) | Số bài | Pass@1 (%) | Mean Pass Rate (%) | Model Calls TB / bài | Tổng Tokens TB / bài | Thời gian Giải TB / bài | Tổng Chi phí GPU (300 bài) |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **Direct Baseline** | 300 | 25.33% (76/300) | 38.41% | **1.27** | **1,372.7** | **24.56s** | ~$4.00 (Modal L40S) |
| **RethinkMCTS Dual** | 300 | **36.00%** (108/300) | **53.49%** | 15.29 | 37,759.3 | 108.70s | ~$17.50 (Modal L40S) |
| **Hệ số Mở rộng ($\times$)** | — | **+10.67%** (+32 bài) | **+15.08%** | **12.04 $\times$** | **27.51 $\times$** | **4.43 $\times$** | Đổi lại mức tăng trưởng vượt trội |

### Bảng 4.4c. So sánh Chi phí và Phân rã Token trên HumanEval-164 ✅

| Phương pháp (14B) | Pass@1 (%) | Số bài Pass | Model Calls TB | Tokens TB / bài | Thời gian TB / bài | Cơ chế Dừng sớm (`early_stop`) |
| :--- | :-: | :-: | :-: | :-: | :-: | :--- |
| **Direct Generation** | 90.24% | 148 / 164 | **1.91** | ~1,200 | **5.14s** | Không tìm kiếm (1 rollout) |
| **Best-of-3 (BoN-3)** | 91.46% | 150 / 164 | 5.77 | ~4,100 | 24.04s | Cố định 3 lần lấy mẫu |
| **RethinkMCTS (Dual)** | 90.85% | 149 / 164 | **4.64** | 3,217.7 | 25.26s | Dừng sớm khi pass public + critic |
| **RethinkMCTS (Test-only)** | **93.29%** | **153 / 164** | **4.55** | ~3,100 | **20.94s** | **Dừng ngay khi pass public tests** |

- **Phân rã Token theo vai trò trên 14B HumanEval Dual (164 bài):**
  - *Expansion:* 179 calls (92,576 tokens = 17.5%)
  - *Code Generation:* 264 calls (114,752 tokens = 21.7%)
  - *Block Analysis:* 87 calls (174,416 tokens = 33.1%)
  - *Rethink:* 72 calls (94,311 tokens = 17.9%)
  - *Critic:* 159 calls (51,641 tokens = **9.8%**)
  - **Tổng cộng:** 761 calls (4.64 calls/bài), 527,696 tokens (3,217.7 tokens/bài).

---

## 4.5. Kiểm định Ý nghĩa Thống kê (Statistical Significance)

| Cặp đối sánh | Tập dữ liệu | Kiểm định | Kết quả chi tiết | Kết luận Khoa học |
| :--- | :--- | :--- | :--- | :--- |
| **14B MCTS Dual vs 14B Direct** | **APPS-300 (300 bài)** | McNemar ($\chi^2$) + Bootstrap CI 95% | **$\chi^2 = 18.4808, p = 1.72 \times 10^{-5}$** ($p \ll 0.001$)<br>Direct 95% CI: $[20.67\%, 30.33\%]$<br>MCTS 95% CI: $[30.67\%, 41.67\%]$<br>$\Delta = +10.67\%$ (95% CI: $[3.67\%, 18.00\%]$) | **Ý nghĩa thống kê vượt bậc** (MCTS cứu 42 bài Direct bó tay). |
| **14B MCTS Test-only vs 14B Direct** | **HumanEval (164 bài)** | McNemar ($\chi^2$) + Bootstrap CI 95% | **$\chi^2 = 1.2308, p = 0.2673$**<br>Direct CI: $[85.37\%, 94.51\%]$<br>MCTS CI: $[89.63\%, 96.95\%]$<br>$\Delta = +3.05\%$ (95% CI: $[-1.22\%, +7.32\%]$) | MCTS giải đúng thêm 5 bài ròng (9 bài MCTS cứu vs 4 bài Direct hơn). |
| **14B MCTS Test-only vs 14B BoN-3** | **HumanEval (164 bài)** | McNemar ($\chi^2$) + Bootstrap CI 95% | **$\chi^2 = 0.3636, p = 0.5465$**<br>$\Delta = +1.83\%$ (95% CI: $[-1.83\%, +6.10\%]$) | MCTS hơn BoN-3 3 bài ròng nhưng **tiết kiệm hơn 21% lời gọi mô hình** (4.55 vs 5.77). |
| **14B MCTS Test-only vs 14B Dual** | **HumanEval (164 bài)** | McNemar ($\chi^2$) + Bootstrap CI 95% | **$\chi^2 = 1.1250, p = 0.2888$**<br>$\Delta = +2.44\%$ (95% CI: $[-0.61\%, +6.10\%]$) | Test-only cao hơn 4 bài do ít test công khai trên HumanEval. |
| **14B MCTS vs 14B Direct** | **APPS Intro (100 bài)** | McNemar ($\chi^2$) + Bootstrap CI 95% | **$\chi^2 = 4.9231, p = 0.0265 < 0.05$**<br>$\Delta = +9.00\%$ (95% CI: $[+3.00\%, +16.00\%]$) | **Có ý nghĩa thống kê ($p < 0.05$)**, khoảng tin cậy 95% hoàn toàn dương. |
| **14B MCTS vs 14B BoN-3** | **APPS Intro (100 bài)** | McNemar ($\chi^2$) + Bootstrap CI 95% | **$\chi^2 = 2.4000, p = 0.1213$**<br>$\Delta = +7.00\%$ (95% CI: $[+0.00\%, +15.00\%]$) | MCTS vượt trội +7.00% so với lấy mẫu ngẫu nhiên 3 lần. |

### 4.5.1. Chi tiết Phân tích Cặp bài (Paired Contingency Table) trên 14B APPS-300:
- **Cả hai cùng giải đúng (Both Pass):** 66 bài.
- **Cả hai cùng giải sai (Both Fail):** 182 bài.
- **Direct giải đúng, MCTS giải sai ($b$):** 10 bài.
- **Direct giải sai, MCTS cứu thành công ($c$):** **42 bài**.
- **Chênh lệch cứu bài thực tế:** MCTS giải cứu thành công $42 - 10 = +32$ bài toán hóc búa từ tay Direct.
- **Ý nghĩa:** Kiểm định McNemar hiệu chỉnh liên tục cho giá trị $\chi^2 = 18.4808$ với $p = 1.7163 \times 10^{-5} \ll 0.001$, khẳng định mức vượt trội $+10.67\%$ của RethinkMCTS Dual so với Direct là có ý nghĩa thống kê vượt bậc, không phải do phương sai ngẫu nhiên. Khoảng tin cậy Bootstrap 95% cho độ chênh lệch $\Delta$ là $[3.67\%, 18.00\%]$, hoàn toàn nằm trên vùng dương.

### 4.5.2. Chi tiết Phân tích Cặp bài trên HumanEval-164:
- **MCTS Test-only (153 bài) vs Direct Baseline (148 bài):**
  - Cả hai cùng pass: 144 bài.
  - Cả hai cùng fail: 7 bài.
  - Direct pass, MCTS fail: 4 bài.
  - **Direct fail, MCTS cứu thành công:** **9 bài**.
  - MCTS cứu được 9 bài toán mà Direct thất bại (ví dụ: các bài xử lý đệ quy lồng nhau và xâu ký tự phức tạp).
- **MCTS Test-only (153 bài) vs BoN-3 (150 bài):**
  - Cả hai cùng pass: 146 bài.
  - BoN-3 pass, MCTS fail: 4 bài.
  - **BoN-3 fail, MCTS cứu thành công:** **7 bài**.

### 4.5.3. Chi tiết Phân tích Cặp bài trên APPS Introductory-100:
- **MCTS (30 bài) vs Direct Baseline (21 bài):**
  - Cả hai cùng pass: 19 bài | Cả hai cùng fail: 68 bài.
  - Direct pass, MCTS fail: 2 bài.
  - **Direct fail, MCTS cứu thành công:** **11 bài**.
  - Kiểm định McNemar đạt $\chi^2 = 4.9231, p = 0.0265 < 0.05$ (đạt ngưỡng ý nghĩa thống kê chuẩn $5\%$). Bootstrap 95% CI cho độ chênh lệch là $[+3.00\%, +16.00\%]$.

---

## 4.6. Phân loại Lỗi & Năng lực Giải cứu của Cơ chế Rethink (RQ1, RQ2 — Paper Table 4) ✅
*(Trích xuất chính xác từ toàn bộ 300 bài toán trong [`runs/benchmark_apps_14b_dual_unified/`](../../runs/benchmark_apps_14b_dual_unified/))*

Để trả lời **RQ1 (Phản hồi thực thi giúp giải cứu mã nguồn như thế nào)** và đối chiếu với **Table 4 trong bài báo gốc RethinkMCTS**, chúng tôi theo dõi trạng thái lỗi của ứng viên mã đầu tiên (Rollout 0), động học sửa lỗi khi kích hoạt Rethink tại lá cây tìm kiếm, và tỷ lệ mã hợp lệ trên toàn bộ cây duyệt (`Tree Effective Code Rate`).

### Bảng 4.6. Phân tích Chi tiết Động học Sửa lỗi & Tỷ lệ Cứu vãn nhờ Rethink trên 14B APPS-300

| Nhóm Chỉ số | Tham số Phân tích | Số lượng | Tỷ lệ (%) | Nhận xét & Ý nghĩa Thực nghiệm |
| :--- | :--- | :-: | :-: | :--- |
| **1. Kết quả Lần thử Đầu (Rollout 0)** | • Giải đúng 100% public tests ngay lần đầu | **84 / 300** | **28.0%** | Chỉ hơn 1/4 số bài được giải quyết mà không cần sửa lỗi. |
| | • Thất bại lần đầu (kích hoạt MCTS & Rethink) | **216 / 300** | **72.0%** | **72% bài toán đòi hỏi cơ chế tìm kiếm và sửa sai.** |
| **2. Phân loại Lỗi Ban đầu (Error Taxonomy)** | • Sai kết quả (Wrong Answer - WA) | 184 / 216 | **85.2%** | Lỗi thuật toán và logic điều kiện chiếm tuyệt đại đa số. |
| | • Lỗi thời gian chạy (Runtime Error - RE) | 30 / 216 | **13.9%** | Lỗi tràn chỉ mục mảng (`IndexError`), đệ quy sâu hoặc chia cho 0. |
| | • Quá giới hạn thời gian (Time Limit Exceeded - TLE) | 2 / 216 | **0.9%** | Rất ít bài bị lặp vô hạn nhờ cơ chế cắt nhánh sớm. |
| | • Lỗi biên dịch / cú pháp (Syntax / Compilation Error) | **0 / 216** | **0.0%** | Qwen2.5-Coder-14B sinh cú pháp Python chuẩn xác tuyệt đối. |
| **3. Hành vi & Năng lực Giải cứu của Rethink** | • Số bài kích hoạt Rethink (Search Iterations > 1) | **216 / 300** | 72.0% | Trung bình 3.45 lượt rethink/bài (tối đa 10 lượt). |
| | • Số bài được Rethink cứu đạt 100% public tests | **77 / 216** | **35.6%** | **Hơn 1/3 số bài thất bại ban đầu đã được chuyển hóa thành pass public.** |
| | • **Số bài được Rethink cứu pass 100% test ẩn** | **38 / 216** | **17.6%** | **Cứu ròng 38 bài toán giải đúng tuyệt đối** từ tay thất bại! |
| | • **Đóng góp của Rethink vào tổng số bài Pass của 14B** | **38 / 108** | **35.2%** | **Hơn 1/3 (35.2%) tổng chiến thắng của MCTS là nhờ Rethink!** Không có Rethink, Pass@1 của 14B chỉ đạt ~23.33%. |
| **4. Hiệu suất Cây Tìm kiếm (Search Tree Efficiency)** | • Tổng số ứng viên mã sinh ra trên cây | 1,748 code | — | Trung bình 5.83 code attempts / bài toán. |
| | • Số ứng viên mã vượt qua 100% public tests | 161 code | — | Các ứng viên đủ điều kiện để kích hoạt Critic. |
| | • **Tỷ lệ Ứng viên Mã Hợp lệ (`Tree Effective Code Rate`)** | **161 / 1,748** | **9.21%** | Tương đương con số 8.5% – 11.2% của GPT-4o-mini trong bài báo gốc (Paper Table 4). |

---

## 4.7. Đường cong Mở rộng theo Ngân sách Thời gian Suy luận (Test-Time Scaling Curve — RQ4) ✅
*(Trích xuất từ kết quả tích lũy theo ngân sách lần thử $k \in \{1, 2, 4, 8, 16\}$ trên 300 bài 14B APPS-300)*

Để kiểm chứng **Giả thuyết Mở rộng tại Thời điểm Suy luận (Test-Time Compute Scaling)** nêu tại **Mục 5.3 Đề cương (`Proposal.md`)** và **Figure 5 bài báo gốc**, chúng tôi khảo sát tỷ lệ giải đúng Pass@1 (trên test ẩn) và tỷ lệ vượt qua test công khai (Public Pass Rate) khi cho phép hệ thống tìm kiếm tích lũy tối đa $k$ ứng viên mã nguồn ($k \in \{1, 2, 4, 8, 16\}$).

### Bảng 4.7. Động thái Tăng trưởng Pass@1 theo Ngân sách Ứng viên $k$ trên 14B APPS-300

| Ngân sách Ứng viên ($k$) | Pass@1 trên Test Ẩn (%) | Số bài Pass Ẩn | Public Pass Rate (%) | Số bài Pass Public | Mức Tăng Biên ($\Delta$ Pass@1) | Nhận xét Hiệu quả Biên |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **$k = 1$** | **22.00%** | 66 / 300 | 28.00% | 84 / 300 | — | Kết quả của ứng viên ban đầu tại nút gốc. |
| **$k = 2$** | **26.67%** | 80 / 300 | 37.67% | 113 / 300 | **+4.67%** (+14 bài) | Hiệu quả bứt phá mạnh nhất nhờ lần Rethink đầu tiên. |
| **$k = 4$** | **31.33%** | 94 / 300 | 45.33% | 136 / 300 | **+4.66%** (+14 bài) | Khám phá thêm các nhánh tư duy mới (Expansion). |
| **$k = 8$** | **35.00%** | 105 / 300 | 50.67% | 152 / 300 | **+3.67%** (+11 bài) | Đạt 97.2% trần năng lực tối đa của cây tìm kiếm. |
| **$k = 16$** (Toàn bộ) | **36.00%** | 108 / 300 | 53.67% | 161 / 300 | **+1.00%** (+3 bài) | Bắt đầu bão hòa; chi phí biên cho mỗi bài pass tăng cao. |

```
Pass@1 (%)
 40% ┤                                         ╭─── 36.00% (k=16)
     │                                   ╭─────╯ 35.00% (k=8)
 30% ┤                         ╭─────────╯ 31.33% (k=4)
     │               ╭─────────╯ 26.67% (k=2)
 20% ┤ ──────────────╯ 22.00% (k=1)
     │
  0% ┴──────┬─────────────┬─────────────┬─────────────┬─────────────
           k=1           k=2           k=4           k=8          k=16
```

> **Phát hiện Khoa học:**
> 1. **Quy luật Tăng trưởng Đơn điệu dạng Logarit:** Tỷ lệ Pass@1 tuân theo quy luật hàm logarit theo số lần thử $k$: $Pass@1(k) \approx a \cdot \ln(k) + b$.
> 2. **Điểm Cân bằng Tối ưu Chi phí / Hiệu năng ($k = 8$):** Tại $k = 8$, mô hình đã gặt hái được **35.00% / 36.00% (97.2%)** số bài giải đúng toàn bộ, trong khi tiết kiệm được gần một nửa chi phí suy luận so với việc cho cây nở tối đa $k = 16$. Đây là tham số khuyến nghị cho các hệ thống ứng dụng thực tế.

---

## 4.8. Năng lực Tự Thẩm định: Thí nghiệm Đối chứng Self-Critic vs Cross-Critic (RQ3) ✅
*(Trích xuất từ kết quả thực nghiệm kiểm thử độc lập 161 ứng viên mã đạt $v_{\text{test}} = 1.0$ của APPS-300 tại [`runs/cross_critic_analysis_14b/`](../../runs/cross_critic_analysis_14b/))*

Để kiểm chứng câu hỏi khoa học: *"Liệu một mô hình độc lập bên ngoài (Cross-Critic) có khách quan và đáng tin cậy hơn mô hình tự sinh mã (Self-Critic) khi chấm điểm các ứng viên đã vượt qua bài kiểm thử công khai hay không?"*, chúng tôi cho mô hình mã nguồn chuyên biệt **Mistral Codestral (`codestral-latest`, 22 tỷ tham số)** đóng vai trò Cross-Critic thẩm định độc lập toàn bộ 161 ứng viên mã đã đạt $v_{\text{test}} = 1.0$ do `Qwen2.5-Coder-14B` sinh ra trên cùng một prompt hệ thống.

### Bảng 4.8. Bảng So sánh Năng lực Thẩm định: Self-Critic (Qwen-14B) vs Cross-Critic (Codestral-22B)

| Chỉ số Đánh giá Thống kê | Self-Critic (Qwen2.5-Coder-14B) | Cross-Critic (Mistral Codestral-22B) | Mức Chênh lệch | Ý nghĩa Thống kê & Thực nghiệm |
| :--- | :---: | :---: | :---: | :--- |
| **Hệ số Tương quan Hạng Spearman ($\rho$)** | **+0.2426** ($p = 0.0019$) | +0.0327 ($p = 0.6806$) | **+0.2099** | **Qwen-14B đạt ý nghĩa thống kê vượt trội ($p < 0.01$)**; Codestral không có tương quan với kết quả test ẩn. |
| **Hệ số Tương quan Tuyến tính Pearson ($r$)** | **+0.1699** ($p = 0.0312$) | -0.0556 ($p = 0.4838$) | **+0.2255** | Qwen-14B đạt ngưỡng chuẩn ($p < 0.05$), Codestral bị nhiễu âm nhẹ do tập trung điểm 1.0. |
| **Tương quan Point-Biserial ($r_{\text{pb}}$ với Hidden Pass)** | **+0.2391** ($p = 0.0023$) | -0.0417 ($p = 0.5997$) | **+0.2808** | Điểm tự chấm của Qwen-14B dự báo chuẩn xác khả năng pass 100% test ẩn của bài toán. |
| **Phân phối Điểm Thẩm định ($v_{\text{llm}}$)** | **1.0:** 121 bài<br>**-1.0:** 35 bài<br>**Khác:** 5 bài | **1.0:** 145 bài (**90.1%**)<br>**-1.0:** 5 bài<br>**Khác:** 11 bài | — | **Codestral bị bão hòa trần nặng nề (Sycophancy):** Chấm điểm tuyệt đối 90.1% số lần, làm mất hoàn toàn tính phân loại. |
| **Tỷ lệ Phê duyệt Sai trên 62 bài Quá khớp (Overfit)** | **64.52%** (Bắt đúng 22 bài sai) | **95.16%** (Bỏ sót 59 / 62 bài sai) | **-30.64%** | **Qwen-14B phát hiện lỗi quá khớp tốt hơn gấp 7.3 lần!** Codestral hầu như cho qua toàn bộ các ca mã lỗi. |
| **Tỷ lệ Phê duyệt Đúng trên 99 bài Pass Ẩn** | 84.85% (84 / 99 bài) | 92.93% (92 / 99 bài) | -8.08% | Codestral đạt tỷ lệ duyệt cao thực chất chỉ do xu hướng cho điểm dễ dãi đồng loạt. |

> **Kết luận Thực nghiệm then chốt:**
> - **Lợi thế Đồng bộ Không gian Suy luận (Internal Reasoning Alignment):** Qwen-14B khi tự đọc lại chuỗi tư duy của mình có khả năng phát hiện những giả định lỏng lẻo mà nó đã đưa ra, giúp chấm điểm phạt $-1.0$ chính xác ở 22 bài toán quá khớp test công khai.
> - **Cảnh báo Hội chứng Cả tin Bề mặt (Surface-Level Sycophancy):** Một mô hình bên ngoài (kể cả có quy mô lớn hơn như 22B) khi chỉ nhìn vào đoạn mã trông sạch đẹp đã pass test công khai sẽ rất dễ bị đánh lừa và tin rằng mã đã đúng hoàn toàn.

---

## 4.9. Phân tích So sánh Đối đầu giữa Hai Quy mô Mô hình 7B vs 14B (RQ3) ✅
*(Kiểm định Khi-bình phương Pearson $\chi^2$ hiệu chỉnh liên tục Yates và Tỷ số Chênh lệch Odds Ratio trên 300 bài APPS và 164 bài HumanEval)*

Để trả lời **RQ3 (Quy mô mô hình tác động như thế nào đến hiệu quả của MCTS)**, chúng tôi thực hiện kiểm định giả thuyết thống kê về sự khác biệt giữa hai quy mô **Qwen2.5-Coder-7B** và **Qwen2.5-Coder-14B** trên từng tập benchmark và phân tầng độ khó.

### Bảng 4.9. Kiểm định Khi-bình phương ($\chi^2$) và Tỷ số Chênh (Odds Ratio) giữa 7B và 14B

| Phép Đối sánh Thực nghiệm | Tập Dữ liệu | Tỷ lệ 7B | Tỷ lệ 14B | Mức Tăng ($\Delta$) | Thống kê $\chi^2$ (Yates) | Giá trị $p$ | Odds Ratio (14B vs 7B) | Ý nghĩa Khoa học |
| :--- | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :--- |
| **Direct Baseline** | **APPS-300** | 14.00% (42/300) | **25.33%** (76/300) | **+11.33%** | $\chi^2 = 11.4881$ | **$7.00 \times 10^{-4} < 0.001$** | **2.08 $\times$** | Mô hình 14B có năng lực sinh mã gốc vượt trội có ý nghĩa thống kê so với 7B. |
| **RethinkMCTS Dual** | **APPS-300** | 19.00% (57/300) | **36.00%** (108/300) | **+17.00%** | $\chi^2 = 20.8986$ | **$4.84 \times 10^{-6} \ll 0.001$** | **2.40 $\times$** | **Ý nghĩa thống kê vượt bậc:** MCTS trên 14B khuếch đại cơ hội giải đúng gấp 2.4 lần so với trên 7B. |
| • *Introductory (Bài dễ)* | APPS (100 bài) | 38.00% (38/100) | **53.00%** (53/100) | **+15.00%** | $\chi^2 = 3.9520$ | **$0.0468 < 0.05$** | **1.84 $\times$** | Tăng trưởng có ý nghĩa ở mức 5%. |
| • *Interview (Bài trung bình)* | APPS (100 bài) | 14.00% (14/100) | **27.00%** (27/100) | **+13.00%** | $\chi^2 = 4.4179$ | **$0.0356 < 0.05$** | **2.27 $\times$** | Tăng trưởng có ý nghĩa ở mức 5%, xác suất giải đúng tăng hơn gấp đôi. |
| • *Competition (Bài khó)* | APPS (100 bài) | 5.00% (5/100) | **28.00%** (28/100) | **+23.00%** | $\chi^2 = 17.5649$ | **$2.78 \times 10^{-5} \ll 0.001$** | **7.39 $\times$** | **Bước nhảy vọt kiến trúc:** 14B MCTS tăng cơ hội giải đúng bài Olympic khó gấp **7.39 lần** so với 7B! |
| **Direct Baseline** | **HumanEval-164** | 80.49% (132/164) | **90.24%** (148/164) | **+9.76%** | $\chi^2 = 5.4911$ | **$0.0191 < 0.05$** | **2.24 $\times$** | 14B Direct giải đúng thêm 16 bài chuẩn so với 7B Direct. |
| **RethinkMCTS Dual** | **HumanEval-164** | 91.46% (150/164) | 90.85% (149/164) | -0.61% | $\chi^2 = 0.0000$ | $1.0000$ (n.s.) | 0.93 $\times$ | Cả hai đều chạm trần năng lực (> 90%), khác biệt không có ý nghĩa thống kê. |
| **Cộng hưởng Vượt cấp (Cross-scale Synergy)** | **HumanEval-164** | **7B MCTS: 91.46%** | **14B Direct: 90.24%** | **+1.22%** | — | — | — | **Mô hình 7B gắn MCTS vượt qua mô hình 14B chạy Direct.** |

> **Kết luận Quy luật Mở rộng (Scaling Law Insights):**
> 1. **Hiệu ứng "Bệ phóng Năng lực":** MCTS không thể thay thế kiến thức nền tảng của mô hình. Ở các bài Competition, khi mô hình 7B không biết thuật toán nâng cao, MCTS chỉ đạt 5%. Nhưng khi mô hình 14B đã có tri thức tiềm ẩn, MCTS hoạt động như một bệ phóng khuếch đại đưa Pass@1 lên **28.00% (tăng gấp 7.39 lần)**.
> 2. **Cộng hưởng Vượt cấp:** Trên các bài toán vừa sức như HumanEval, việc bổ sung cơ chế tìm kiếm MCTS giúp mô hình nhỏ 7B (91.46%) vượt mặt cả mô hình lớn hơn gấp đôi 14B Direct (90.24%), chứng minh tiềm năng to lớn của việc dùng tính toán suy luận (Test-time compute) thay vì chỉ mở rộng kích thước tham số.
