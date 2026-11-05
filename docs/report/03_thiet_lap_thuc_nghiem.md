# Chương 3. Thiết lập Thực nghiệm

## 3.1. Bộ dữ liệu & Chính sách Chia Kiểm thử (Dataset & Test Split Policy)

| Bộ dữ liệu | Quy mô thực nghiệm | Phương pháp chọn mẫu | Nguồn dữ liệu trong Repo |
| :--- | :-: | :--- | :--- |
| **APPS-300** | **300 bài** (100 Introductory, 100 Interview, 100 Competition) | Stratified Random Sampling không hoàn lại (`seed=2027`, lọc bài có $\ge 3$ test cases) | [apps_benchmark_300.json](../../data/cohorts/apps_benchmark_300.json) |
| **HumanEval** | **164 bài** (`HumanEval/0` $\to$ `163`) | Toàn bộ tập chuẩn của OpenAI | `prepared/humaneval/` |
| **CodeContests** | Đã có Adapter (`code_contests.py`), **chưa đưa vào bảng chạy chính** | Để lại cho hướng mở rộng (ghi rõ phạm vi thực nghiệm chính tập trung vào APPS-300 & HumanEval-164) | [code_contests.py](../../src/rethink_mcts/adapters/datasets/code_contests.py) |

### ⚠️ Lưu ý Quan trọng về Chính sách Chia Public / Hidden Tests trên APPS
Khi kiểm tra code thực tế giữa hai nhánh thực nghiệm:
- **Nhánh 14B (`TLCN` — [apps.py](../../src/rethink_mcts/adapters/datasets/apps.py#L87-L94)):**
  - `public_tests` (dùng trong MCTS search): Lấy **2 test cases đầu tiên** (`all_cases[:2]`) cho toàn bộ 300 bài.
  - `hidden_suite` (dùng trong `HiddenJudge`): Lấy **các test cases còn lại** (`all_cases[2:]`, đã loại bỏ các test trùng nội dung với `public_tests`).
- **Nhánh 7B (`external/ReThinkMCTS` — [rethinkmcts-apps-native-v2-w4-retry.md](../results/7b/rethinkmcts-apps-native-v2-w4-retry.md)):**
  - `public_tests` (dùng trong MCTS search): Chính sách `half` (**nửa đầu** số test cases: `total // 2`).
  - Bước chấm cuối (`all_tests` rejudge): Chấm trên **toàn bộ** test cases trong `input_output.json`.
- **Trên HumanEval (Cả 7B và 14B):**
  - Đều dùng `given_tests` (các ví dụ trong docstring đề bài) cho quá trình tìm kiếm MCTS và chấm điểm cuối cùng bằng **official test harness** độc lập.

> **Hệ quả phương pháp luận (Cần ghi rõ trong báo cáo):**
> So sánh **nội bộ từng nhánh** (7B Direct vs 7B MCTS; hoặc 14B Direct vs 14B BoN vs 14B MCTS) là hoàn toàn đồng nhất (apple-to-apple). Khi đặt cạnh nhau giữa 7B và 14B trên APPS, cần chú thích rõ sự khác biệt về số lượng public tests (`half` vs `first-two`) và tập chấm cuối (`all_tests` vs `disjoint hidden_suite`), đúng như lưu ý tại `external/ReThinkMCTS/docs/runbooks/benchmark-v2.md`.

### ⚠️ Lưu ý về các Run Thăm dò `runs/apps_intro_*_14b`
- Ba thư mục `apps_intro_direct_14b`, `apps_intro_bon3_14b`, `apps_intro_mcts_14b` chạy trên 100 bài `apps_4000`–`apps_4099`, chỉ trùng **15/100 bài** với phân tầng Introductory của `apps_benchmark_300.json`. Do đó, kết quả này được trình bày ở một bảng thăm dò riêng (Bảng 4.3), **tuyệt đối không gộp chung vào bảng APPS-300**.

---

## 3.2. Cấu hình Mô hình & Tham số Thực nghiệm

| Hạng mục | APPS-300 (14B Dual - Chính thức) | HumanEval-164 (14B MCTS - Hiện có) | APPS-300 (7B Dual & Test-only) |
| :--- | :--- | :--- | :--- |
| **File cấu hình** | [benchmark_apps_14b_dual.yaml](../../configs/benchmark_apps_14b_dual.yaml) | [benchmark_humaneval_14b.yaml](../../configs/benchmark_humaneval_14b.yaml) | [rethinkmcts-apps-native-v2-w4-retry.md](../results/7b/rethinkmcts-apps-native-v2-w4-retry.md) |
| **Model** | `Qwen/Qwen2.5-Coder-14B-Instruct` | `Qwen/Qwen2.5-Coder-14B-Instruct` | `qwen2.5-coder:7b-instruct` |
| **Prompt Bundle** | `native_v2` | `compact_v1` | `native_v2` (APPS), `native_v1` (HumanEval Dual) |
| **Độ rộng / Độ sâu** | `width = 3`, `max_depth = 4` | `width = 3`, `max_depth = 4` | `width = 3`, `rollouts = 2` |
| **P-UCB ($c_{\text{base}}, c$)** | $c_{\text{base}} = 10.0,\; c = 4.0$ | $c_{\text{base}} = 10.0,\; c = 1.5$ | $c_{\text{base}} = 10.0,\; c = 4.0$ |
| **Max Rethinks / Node** | `2` | `1` | `2` |
| **Reward Policy** | **Dual** ($0.8, 0.2$) | **Test-only** ($1.0, 0.0$) *(0 critic calls)* | **Dual** ($0.8, 0.2$) & **Test-only** ($1.0, 0.0$) |
| **Feedback Mode** | `block` | `block` | `block` |
| **Max Code Generations** | `16` (`early_stop: public_all_passed`) | `16` (`early_stop: public_all_passed`) | `2 rollouts` (cộng các lượt rethink) |
| **Timeout / Test** | `5.0s` (Wall cap: `900s`/bài) | `4.0s` (Wall cap: `600s`/bài) | `5.0s` (Wall cap: `900s`/bài) |
| **Seed** | `0` | `42` | `0` |

---

## 3.3. Các Phương pháp So sánh (Baselines) và Nghiên cứu Triệt tiêu (Ablations)

Theo [Proposal.md §5.2–5.3](../../Proposal.md) và bài báo gốc ([Rethink_extracted.md §5–6](../../Rethink_extracted.md)):

### (a) Các Baseline So sánh
1. **Direct Generation (`--solver direct`):** Sinh mã 1 lần duy nhất, không dùng kiểm thử để sửa.
2. **Best-of-$N$ (`--solver best_of_n --samples-n 3`):** Lấy mẫu độc lập $N$ ứng viên mã, chấm trên `public_tests` và chọn ứng viên có `pass_rate` cao nhất.
3. **Iterative Repair / Self-Refine (`--solver iterative_repair`):** Sinh mã ban đầu, sau đó lặp lại việc sửa code tuần tự dựa trên phản hồi thực thi của `public_tests` mà không có cây tìm kiếm tư duy ([baselines.py](../../src/rethink_mcts/application/baselines.py#L141)).

### (b) Các Cấu hình Nghiên cứu Triệt tiêu (Ablation Studies)
1. **Ablation 1 — Vai trò LLM Critic (`Reward Policy`):** So sánh **Dual Reward** $(0.8, 0.2)$ với **Test-only** $(1.0, 0.0)$ (`w/o selfEval` trong Paper Figure 3).
2. **Ablation 2 — Cơ chế Rethink tại Lá (`w/o Rethink`):** Đặt `search.max_rethinks_per_node = 0` (chỉ mở rộng cây MCTS thông thường, không hiệu chỉnh tư duy lá khi lỗi).
3. **Ablation 3 — Mức độ Phản hồi Thực thi (`Feedback Granularity`):** So sánh `feedback.mode` giữa `none` (`w/o VF`), `facts_only` (chỉ báo lỗi thô), `trace` (`w/o blockInfo` - có trace biến nhưng không phân tích block bằng LLM) và `block` (đầy đủ CFG + LLM block analysis).
4. **Ablation 4 — Chính sách Lan truyền Phần thưởng (`Backup Policy`):** So sánh **Max Backup** ($Q = \max$) với **Mean Backup** (`search.backup = mean`) theo [Proposal.md §5.3](../../Proposal.md).

---

## 3.4. Chỉ số Đánh giá (Evaluation Metrics)

1. **Pass@1 (%):** Tỷ lệ phần trăm bài toán trong cohort mà ứng viên được chọn (`selected.py`) vượt qua 100% bài kiểm thử của `HiddenJudge` (mẫu số cố định là tổng số bài của cohort, kể cả các bài timeout hoặc lỗi kỹ thuật).
2. **Mean Hidden Pass Rate (%):** Trung bình cộng (macro-average) tỷ lệ test ẩn vượt qua trên từng bài toán.
3. **Tree Effective Code Rate (%):** Tỷ lệ phần trăm ứng viên mã sinh ra trên toàn bộ cây tìm kiếm đạt $v_{\text{test}} = 1.0$ trên kiểm thử công khai (theo Paper Table 4).
4. **Chi phí Suy luận (Inference Cost):** Số lượt gọi mô hình (`total_model_calls`), số lần sinh mã (`code_generation_attempts`), số lần sửa lá (`rethink_attempts`), lượng token (`input_tokens`, `output_tokens`, `total_tokens` tách theo 5 vai trò) và thời gian giải (`solve_wall_seconds`).
5. **Kiểm định Thống kê:** Khoảng tin cậy 95% (Bootstrap CI 95%) và kiểm định cặp McNemar's test trên cùng tập bài toán.
