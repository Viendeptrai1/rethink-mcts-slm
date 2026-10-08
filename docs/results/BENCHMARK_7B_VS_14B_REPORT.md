# Báo cáo Benchmark Đối đầu: Qwen2.5-Coder 7B vs 14B (Chính thức)

> **Dự án:** Cải thiện khả năng suy luận của SLM trong sinh mã nguồn bằng Monte Carlo Tree Search với phản hồi từ kiểm thử tự động.  
> **Ngày cập nhật:** 08/10/2026  
> **Phân công thực nghiệm:**  
> - **Nhánh 7B (`Qwen2.5-Coder-7B-Instruct`):** Do HuyinCP thực hiện ([chi tiết trong `docs/results/7b/`](file:///Users/kotori/Documents/TLCN/docs/results/7b/)). **ĐÃ HOÀN TẤT CHÍNH THỨC**.  
> - **Nhánh 14B (`Qwen2.5-Coder-14B-Instruct`):** Do Kotori thực hiện trên TLCN ([chi tiết trong `runs/benchmark_apps_14b_dual_unified/`](file:///Users/kotori/Documents/TLCN/runs/benchmark_apps_14b_dual_unified/)). **ĐÃ HOÀN TẤT CHÍNH THỨC (300/300 BÀI)**.  

---

## 1. Tóm tắt Kết quả Thực nghiệm Tổng quan

Cả hai nhánh đã hoàn thành toàn bộ thực nghiệm trên cùng tập **300 bài toán Stratified Random Sampling (`seed=2027`: 100 Intro, 100 Inter, 100 Comp)** định nghĩa tại [`data/cohorts/apps_benchmark_300.json`](file:///Users/kotori/Documents/TLCN/data/cohorts/apps_benchmark_300.json) với cùng cấu hình prompting `native_v2`:

### Bảng So sánh Đối đầu APPS Benchmark (300 Bài toán)

| Phân tầng Độ khó | Chỉ số | 7B Direct (Baseline) | 7B MCTS Dual (Huy) | 7B MCTS Test-only (Huy) | 14B MCTS Dual (Kotori - Mới) | Tăng trưởng 14B vs 7B Dual |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Introductory**<br>*(100 bài)* | **Pass@1 (%)**<br>Hidden Pass Rate | 31.00% (31/100)<br>45.84% | 38.00% (38/100)<br>56.70% | **41.00%** (41/100)<br>61.14% | **53.00%** (53/100)<br>**71.26%** | **+15.00%**<br>*(+14.56%)* |
| **Interview**<br>*(100 bài)* | **Pass@1 (%)**<br>Hidden Pass Rate | 7.00% (7/100)<br>26.18% | 14.00% (14/100)<br>42.36% | **18.00%** (18/100)<br>45.46% | **27.00%** (27/100)<br>**50.13%** | **+13.00%**<br>*(+7.77%)* |
| **Competition**<br>*(100 bài)* | **Pass@1 (%)**<br>Hidden Pass Rate | 4.00% (4/100)<br>19.52% | 5.00% (5/100)<br>30.07% | **9.00%** (9/100)<br>29.42% | **28.00%** (28/100)<br>**39.08%** | **+23.00%**<br>*(+9.01%)* |
| **APPS Overall**<br>*(300 bài full)* | **Pass@1 (%)**<br>**Macro Pass Rate** | **14.00%** (42/300)<br>**30.51%** | **19.00%** (57/300)<br>**43.04%** | **22.67%** (68/300)<br>**45.34%** | **36.00%** (108/300)<br>**53.49%** | **+17.00% (Gần gấp đôi!)**<br>*(+10.45%)* |

---

## 2. Hệ thống Biểu đồ Đối đầu Trực quan (Publication Figures)

Toàn bộ biểu đồ dưới đây được kết xuất ở độ phân giải cao 300 DPI bằng script tự động [`scripts/generate_benchmark_charts.py`](file:///Users/kotori/Documents/TLCN/scripts/generate_benchmark_charts.py), sẵn sàng chèn trực tiếp vào báo cáo tiểu luận / luận văn / LaTeX paper:

1. **So sánh Pass@1 trên APPS (4 Phân tầng):**  
   [`docs/results/figures/apps_pass_at_1_comparison.png`](file:///Users/kotori/Documents/TLCN/docs/results/figures/apps_pass_at_1_comparison.png)  
   *Biểu đồ cột trực quan hóa bước nhảy vọt +23% trên phân tầng Competition và +17% trên toàn bộ 300 bài toán.*

2. **So sánh Tỷ lệ Vượt qua Test Ẩn (Hidden Pass Rate):**  
   [`docs/results/figures/apps_hidden_pass_rate_comparison.png`](file:///Users/kotori/Documents/TLCN/docs/results/figures/apps_hidden_pass_rate_comparison.png)  
   *Đối chiếu chất lượng thực thi mã nguồn, 14B đạt 71.26% test ẩn ở mức độ Introductory và 53.49% trung bình toàn cohort.*

3. **Cộng hưởng Mở rộng Quy mô (Cross-Benchmark Scaling Synergy):**  
   [`docs/results/figures/cross_benchmark_scaling.png`](file:///Users/kotori/Documents/TLCN/docs/results/figures/cross_benchmark_scaling.png)  
   *Hình ghép 2 đồ thị: Minh chứng 7B MCTS vượt 14B Direct trên HumanEval (91.5% vs 90.2%) và 14B MCTS bứt phá trên APPS (36.0%).*

4. **Phân phối Tỷ lệ Test Ẩn của 14B (Histogram & CDF):**  
   [`docs/results/figures/apps_14b_pass_rate_distribution.png`](file:///Users/kotori/Documents/TLCN/docs/results/figures/apps_14b_pass_rate_distribution.png)  
   *Phân tích chi tiết 108 bài toán đạt tuyệt đối 100% cùng hàm phân phối tích lũy CDF của 300 bài toán.*

---

## 3. Đối đầu trên HumanEval Benchmark (164 Bài toán Chuẩn)

| Phương pháp | Mô hình | Pass@1 (%) | Số bài Pass (trên 164) | Tăng trưởng vs Direct |
| :--- | :---: | :---: | :---: | :---: |
| **Direct Baseline** | 7B | **80.49%** | 132/164 | — |
| **RethinkMCTS (Test-only)** | 7B | **89.63%** | 147/164 | +9.14% |
| **RethinkMCTS (Dual Reward)**| 7B | **91.46%** | 150/164 | **+10.97%** |
| **Direct Baseline** | 14B | **90.24%** | 148/164 | — |
| **Best-of-3 (BoN-3)** | 14B | **91.46%** | 150/164 | +1.22% |
| **RethinkMCTS** | 14B | **93.29%** | 153/164 | **+3.05%** |

> **Điểm nhấn quan trọng:**
> 1. Mô hình 7B khi được tăng cường bởi RethinkMCTS Dual đạt **91.46%**, vượt qua năng lực sinh trực tiếp của mô hình 14B (**90.24%**).
> 2. Trên mô hình 14B, RethinkMCTS đưa Pass@1 chạm ngưỡng **93.29%**, giải đúng thêm các ca biên phức tạp mà Best-of-N thông thường không thể vượt qua.

---

## 3. Phân tích Chuyên sâu (In-depth Research Insights)

### 3.1. Hiệu ứng Khuếch đại của MCTS theo Quy mô Mô hình (Model Scaling Synergy)
- **Ở bài toán dễ (Introductory):** Nâng cấp từ 7B MCTS lên 14B MCTS tăng Pass@1 từ 38.00% lên 53.00% (+15%). Mô hình 14B giải quyết trọn vẹn hơn một nửa số bài thi nhập môn ngay ở lần chạy đầu tiên.
- **Đột phá ngoạn mục ở bài toán khó (Competition):**
  - Mô hình 7B hầu như chạm trần ở mức độ Competition (Direct chỉ 4%, MCTS Dual chỉ đạt 5%, Test-only đạt 9%). Nguyên nhân là không gian tìm kiếm quá rộng và 7B thiếu kiến thức nền về các cấu trúc dữ liệu nâng cao (Segment Tree, DP trạng thái bit, v.v.).
  - Ngược lại, **14B MCTS Dual đạt tới 28.00% Pass@1** (tăng gấp hơn 5.6 lần so với 7B MCTS Dual). Điều này chứng minh MCTS phát huy sức mạnh tối đa khi mô hình cơ sở đủ mạnh để sinh ra các ý tưởng (thoughts) ban đầu có chất lượng và chiều sâu thuật toán.

### 3.2. So sánh Năng lực Tự Thẩm định (Critic Degradation vs Model Capacity)
- Trên 7B, cấu hình **Test-only (22.67%)** vượt trội hơn **Dual Reward (19.00%)**. Điều này chứng minh mô hình 7B có năng lực tự đánh giá (critic self-evaluation) chưa đủ tin cậy, điểm số LLM critic bị nhiễu và làm sai lệch quyết định chọn nhánh của MCTS.
- Trên 14B, cấu hình Dual Reward đạt tới **36.00% Pass@1** và **53.49% Hidden Pass Rate**, cho thấy ở kích thước 14B, LLM Critic đã bắt đầu hỗ trợ tốt hơn cho việc định hướng tìm kiếm kết hợp với tín hiệu kiểm thử public.

---

## 4. Dữ liệu Artifacts & Quản lý Hạ tầng

Toàn bộ kết quả thực nghiệm 14B đã được tổng hợp, kiểm chứng và lưu trữ tại:
- **Thư mục báo cáo hợp nhất:** [`runs/benchmark_apps_14b_dual_unified/`](file:///Users/kotori/Documents/TLCN/runs/benchmark_apps_14b_dual_unified/)
  - [`summary.json`](file:///Users/kotori/Documents/TLCN/runs/benchmark_apps_14b_dual_unified/summary.json): 300 bản ghi chi tiết từng bài toán, mã sinh ra, hash và thời gian giải.
  - [`summary.md`](file:///Users/kotori/Documents/TLCN/runs/benchmark_apps_14b_dual_unified/summary.md): Bảng phân tích chi tiết toàn bộ 300 bài toán.
- **Tổng số lượt gọi mô hình (Model Calls):** 4,716 calls.
- **Trạng thái GPU & Hạ tầng:** Toàn bộ Modal GPU instances đã được dừng hoàn toàn (0 running tasks), đảm bảo không phát sinh chi phí nền.
