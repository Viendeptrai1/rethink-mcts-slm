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
| **Best-of-3 (BoN-3)** | ⏳ TODO | ⏳ TODO | ⏳ TODO | ⏳ TODO | Cần chạy [E2](EXPERIMENT_CHECKLIST.md) |
| **Iterative Repair** | ⏳ TODO | ⏳ TODO | ⏳ TODO | ⏳ TODO | Cần chạy [E5](EXPERIMENT_CHECKLIST.md) |
| **RethinkMCTS (Test-only)** | ✅ **22.67%** (68/300) | ✅ **45.34%** | ⏳ TODO | ⏳ TODO | Cần chạy [E3](EXPERIMENT_CHECKLIST.md) |
| **RethinkMCTS (Dual Reward)** | ✅ 19.00% (57/300) | ✅ 43.04% | ✅ **36.00%** (108/300) | ✅ **53.49%** | Đã hoàn tất 300/300 bài (14B) |

### Bảng 4.1b. Phân rã theo 3 Phân tầng Độ khó trên APPS-300

| Phân tầng (100 bài/tầng) | Chỉ số | 7B Direct | 7B MCTS Dual | 7B MCTS Test-only | 14B Direct | 14B MCTS Dual |
| :--- | :--- | :-: | :-: | :-: | :-: | :-: |
| **Introductory** | Pass@1 (%)<br>Pass Rate (%) | 31.00%<br>45.84% | 38.00%<br>56.70% | **41.00%**<br>61.14% | ✅ **42.00%** (42/100)<br>✅ **53.50%** | **53.00%** (53/100)<br>**71.26%** |
| **Interview** | Pass@1 (%)<br>Pass Rate (%) | 7.00%<br>26.18% | 14.00%<br>42.36% | **18.00%**<br>45.46% | ✅ **13.00%** (13/100)<br>✅ **31.48%** | **27.00%** (27/100)<br>**50.13%** |
| **Competition** | Pass@1 (%)<br>Pass Rate (%) | 4.00%<br>19.52% | 5.00%<br>30.07% | **9.00%**<br>29.42% | ✅ **21.00%** (21/100)<br>✅ **30.24%** | **28.00%** (28/100)<br>**39.08%** |
| **Toàn bộ (300 bài)** | **Pass@1 (%)**<br>**Pass Rate (%)** | **14.00%**<br>**30.51%** | **19.00%**<br>**43.04%** | **22.67%**<br>**45.34%** | ✅ **25.33%** (76/300)<br>✅ **38.41%** | **36.00%** (108/300)<br>**53.49%** |

> **Ghi chú kỹ thuật minh bạch:**
> 1. Ở nhánh 7B APPS: Dual có 295/300 bài sinh xong candidate (3 bài search timeout 900s, 2 bài lỗi cú pháp khi trace), Test-only có 297/300 bài (3 bài search timeout 900s); tất cả các bài thiếu candidate đều được gán điểm 0 vào mẫu số 300.
> 2. Ở nhánh 14B APPS Dual: Hoàn tất 300/300 bài, không có lỗi hạ tầng.
> 3. Khác biệt chính sách chia test giữa hai nhánh (`half` + `all_tests` trên 7B vs `first-2 public` + `disjoint hidden_suite` trên 14B) được nêu tại [Chương 3 §3.1](03_thiet_lap_thuc_nghiem.md).

---

## 4.2. Kết quả trên HumanEval Benchmark (164 Bài toán Chuẩn)

- **Nguồn 7B:** [rethinkmcts-modal-humaneval-v1.md](../results/7b/rethinkmcts-modal-humaneval-v1.md), [rethinkmcts-test-only-v1.md](../results/7b/rethinkmcts-test-only-v1.md).
- **Nguồn 14B:** [humaneval_direct_14b](../../runs/humaneval_direct_14b/summary.json), [humaneval_bon3_14b](../../runs/humaneval_bon3_14b/summary.json), [humaneval_mcts_14b](../../runs/humaneval_mcts_14b/summary.json).

### Bảng 4.2. So sánh trên HumanEval-164

| Phương pháp | 7B Pass@1 (%) | 7B Số bài Pass | 14B Pass@1 (%) | 14B Số bài Pass | Calls TB/bài (14B) | Thời gian TB/bài (14B) |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: |
| **Direct Generation** | ✅ 80.49% | 132/164 | ✅ 90.24% | 148/164 | ✅ 1.91 | ✅ 5.14s |
| **Best-of-3 (BoN-3)** | ⏳ TODO | — | ✅ 91.46% | 150/164 | ✅ 5.77 | ✅ 24.04s |
| **RethinkMCTS (Test-only)** | ✅ 89.63% | 147/164 | ✅ **93.29%** ⚠️ | **153/164** | ✅ **4.55** | ✅ **20.94s** |
| **RethinkMCTS (Dual Reward)** | ✅ **91.46%** | **150/164** | ⏳ TODO ([E9](EXPERIMENT_CHECKLIST.md)) | — | — | — |

> **Phát hiện quan trọng từ kiểm tra artifact `runs/humaneval_mcts_14b`:**
> - Toàn bộ 164 file `usage.json` trong `runs/humaneval_mcts_14b/problems/*/usage.json` đều có `critic calls = 0` vì chạy theo config [benchmark_humaneval_14b.yaml](../../configs/benchmark_humaneval_14b.yaml) (`test_weight: 1.0, llm_weight: 0.0`, `bundle: compact_v1`, `c: 1.5`, `max_rethinks_per_node: 1`). Như vậy kết quả **93.29% (153/164)** của 14B trên HumanEval thực chất là cấu hình **RethinkMCTS Test-only**, còn **14B Dual Reward trên HumanEval** chưa được chạy!
> - Đáng chú ý: Trên HumanEval 14B, RethinkMCTS không những đạt Pass@1 cao hơn Best-of-3 (**93.29% vs 91.46%**) mà còn **tốn ít lời gọi mô hình hơn (4.55 calls/bài vs 5.77 calls/bài)** và **nhanh hơn (20.94s vs 24.04s)** nhờ cơ chế `early_stop: public_all_passed` (chỉ có 16/164 bài phải kích hoạt rethink)!

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

---

## 4.5. Kiểm định Ý nghĩa Thống kê (Statistical Significance)

| Cặp đối sánh | Tập dữ liệu | Kiểm định | Kết quả chi tiết | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **14B MCTS Dual vs 14B Direct** | **APPS-300 (300 bài)** | McNemar ($\chi^2$) + Bootstrap CI 95% | **$\chi^2 = 18.4808, p = 1.72 \times 10^{-5}$** ($p \ll 0.001$)<br>Direct 95% CI: $[20.67\%, 30.33\%]$<br>MCTS 95% CI: $[30.67\%, 41.67\%]$<br>$\Delta = +10.67\%$ (95% CI: $[3.67\%, 18.00\%]$) | ✅ **Hoàn thành [A2]** |
| 14B MCTS vs 14B Direct & BoN-3 | HumanEval (164 bài) | McNemar + Bootstrap CI 95% | Xem chi tiết bên dưới | 🧮 Làm ngay được ([A2](EXPERIMENT_CHECKLIST.md)) |
| 14B MCTS vs 14B Direct & BoN-3 | APPS Intro thăm dò (100 bài) | McNemar + Bootstrap CI 95% | Xem chi tiết bên dưới | 🧮 Làm ngay được ([A2](EXPERIMENT_CHECKLIST.md)) |
| 7B Test-only vs 7B Dual vs 7B Direct | APPS-300 (300 bài) | McNemar + Bootstrap CI 95% | Cần ghép bảng kết quả theo bài của 7B | 🧮 Làm ngay được ([A5](EXPERIMENT_CHECKLIST.md)) |

### Chi tiết Phân tích Cặp bài (Paired Contingency Table) trên 14B APPS-300:
- **Cả hai cùng giải đúng (Both Pass):** 66 bài.
- **Cả hai cùng giải sai (Both Fail):** 182 bài.
- **Direct giải đúng, MCTS giải sai ($b$):** 10 bài.
- **Direct giải sai, MCTS cứu thành công ($c$):** **42 bài**.
- **Chênh lệch cứu bài thực tế:** MCTS giải cứu thành công $42 - 10 = +32$ bài toán hóc búa từ tay Direct.
- **Ý nghĩa:** Kiểm định McNemar hiệu chỉnh liên tục cho giá trị $\chi^2 = 18.4808$ với $p = 1.7163 \times 10^{-5} \ll 0.001$, khẳng định mức vượt trội $+10.67\%$ của RethinkMCTS Dual so với Direct là có ý nghĩa thống kê vượt bậc, không phải do phương sai ngẫu nhiên. Khoảng tin cậy Bootstrap 95% cho độ chênh lệch $\Delta$ là $[3.67\%, 18.00\%]$, hoàn toàn nằm trên vùng dương.
