# Sổ kết quả benchmark

Bảng ghi chép **mọi** thứ của các đợt chạy benchmark: run nào, cấu hình gì, chạy ở đâu, kết quả, chi phí và độ "khỏe" của search. Khung báo cáo: [KHUNG_BAO_CAO_v2.md](../report/KHUNG_BAO_CAO_v2.md). Cấu hình v3: [configs/v3_7b/README.md](../../configs/v3_7b/README.md).

Cập nhật lần cuối: 13/11/2026. Đã xong E1–E4 cho `qwen25c7b` và `seedcoder8b`; `qwen35_9b` chạy dở và đang tạm dừng (xem mục 12).

## Quy ước

- **Không trộn protocol.** Sổ này chỉ chứa protocol v3.1 (mục 1–10, 12) và pilot v3.0 (mục 11, không phải kết quả).
- Mọi con số phải có nguồn là một artifact trong `runs/` hoặc `docs/results/`. Ô chưa có số thì để `—`.
- Trạng thái: `⏳` chưa chạy · `▶` đang chạy · `✅` xong và đã đối chiếu artifact · `⚠️` xong nhưng có vấn đề (ghi chú) · `✗` hủy.
- **Pass@1 (hidden):** tỷ lệ bài mà chương trình được chọn pass toàn bộ hidden test, mẫu số là cả cohort (bài lỗi hoặc không có candidate tính 0). **Pass rate:** trung bình theo bài của tỷ lệ hidden test pass.
- Số liệu v3 lấy bằng `scripts/pilot_report.py` (search, chi phí) và [analyze_v3.py](../../scripts/analyze_v3.py) (phân tích ghép cặp, chọn lại offline, Best-of-k).
- Tên ngắn của model: `qwen25c7b` = Qwen2.5-Coder-7B-Instruct · `seedcoder8b` = Seed-Coder-8B-Instruct · `qwen35_9b` = Qwen3.5-9B (tắt thinking) · `granite42_8b` = Granite-4.2-8B (dự phòng) · `qwen25c14b` = Qwen2.5-Coder-14B-Instruct.

---

## 1. Sổ đăng ký run v3

Thư mục run đặt theo mẫu `runs/v3_<dataset>_<model>_<method>`. Commit, GPU, phiên bản vLLM và số worker phải điền **trước khi** chạy. Với mỗi model, mọi phương pháp phải chạy trên cùng nền tảng.

| Mã | Run (`runs/…`) | Model | Dataset | Phương pháp | Config | Commit | Nền tảng / GPU | vLLM | Workers | Ngày | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E1 | `v3_apps_qwen25c7b_mcts` | qwen25c7b | APPS-300 | MCTS | `apps_mcts.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E1 | `v3_apps_seedcoder8b_mcts` | seedcoder8b | APPS-300 | MCTS | `apps_mcts.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E1 | `v3_apps_qwen35_9b_mcts` | qwen35_9b | APPS-300 | MCTS | `apps_mcts.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 13/11/2026 | ⏸ dở (mục 12) |
| E2 | `v3_apps_qwen25c7b_direct` | qwen25c7b | APPS-300 | Direct | `apps_baseline.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E2 | `v3_apps_seedcoder8b_direct` | seedcoder8b | APPS-300 | Direct | `apps_baseline.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E2 | `v3_apps_qwen35_9b_direct` | qwen35_9b | APPS-300 | Direct | `apps_baseline.yaml` | — | — | — | — | — | ⏳ |
| E3 | `v3_apps_qwen25c7b_bon16` | qwen25c7b | APPS-300 | Best-of-16 | `apps_baseline.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ (3 bài giải lại, mục 12) |
| E3 | `v3_apps_seedcoder8b_bon16` | seedcoder8b | APPS-300 | Best-of-16 | `apps_baseline.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E3 | `v3_apps_qwen35_9b_bon16` | qwen35_9b | APPS-300 | Best-of-16 | `apps_baseline.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 13/11/2026 | ⏸ dở (mục 12) |
| E4 | `v3_humaneval_qwen25c7b_mcts` | qwen25c7b | HE-164 | MCTS | `humaneval_mcts.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E4 | `v3_humaneval_seedcoder8b_mcts` | seedcoder8b | HE-164 | MCTS | `humaneval_mcts.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E4 | `v3_humaneval_qwen35_9b_mcts` | qwen35_9b | HE-164 | MCTS | `humaneval_mcts.yaml` | — | — | — | — | — | ⏳ |
| E2 | `v3_humaneval_{qwen25c7b,seedcoder8b,qwen35_9b}_direct` | 3 model | HE-164 | Direct | `humaneval_baseline.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 13/11/2026 | ✅ qwen25c7b, seedcoder8b · ⏳ qwen35_9b |
| E3 | `v3_humaneval_{qwen25c7b,seedcoder8b,qwen35_9b}_bon16` | 3 model | HE-164 | Best-of-16 | `humaneval_baseline.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 13/11/2026 | ✅ qwen25c7b, seedcoder8b · ⏳ qwen35_9b |
| E5 | `v3_apps_qwen25c7b_norethink` | qwen25c7b | APPS (300 hoặc 150) | MCTS, `max_rethinks_per_node=0` | `apps_mcts.yaml` | — | — | — | — | — | ⏳ (nếu còn tiền) |
| E6 | `v3_apps_qwen25c7b_factsonly` | qwen25c7b | APPS (300 hoặc 150) | MCTS, `feedback.mode=facts_only` | `apps_mcts.yaml` | — | — | — | — | — | ⏳ (nếu còn tiền) |
| E7 | `v3_apps_qwen25c14b_mcts` | qwen25c14b | APPS-300 | MCTS | `apps_mcts.yaml` | — | — | — | — | — | ⏳ (nếu còn tiền) |

Best-of-16 chạy với `--set sampling.code.temperature=0.8 --set sampling.code.top_p=0.95`. Nếu đổi giá trị này, ghi vào cột Config.

## 2. APPS-300, Pass@1 trên hidden test (v3)

| Model | Phương pháp | Hoàn tất / 300 | Intro (số bài /100) | Inter (/100) | Comp (/100) | **Overall P@1 %** [Wilson 95%] | Overall pass rate % | Lỗi kỹ thuật (ID) | Chạm 3600 s | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen25c7b | Direct | 300 | 33 | 12 | 7 | **17,3** [13,5–22,0] | 33,0 | 0 | 0 | `runs/v3_apps_qwen25c7b_direct` |
| qwen25c7b | Best-of-16 | 300 | 50 | 21 | 14 | **28,3** [23,5–33,7] | 48,4 | 0 | 0 | `runs/v3_apps_qwen25c7b_bon16` |
| qwen25c7b | RethinkMCTS | 300 | 49 | 25 | 12 | **28,7** [23,8–34,0] | 48,4 | 0 | 0 | `runs/v3_apps_qwen25c7b_mcts` |
| seedcoder8b | Direct | 300 | 33 | 12 | 6 | **17,0** [13,2–21,7] | 30,1 | 0 | 0 | `runs/v3_apps_seedcoder8b_direct` |
| seedcoder8b | Best-of-16 | 300 | 56 | 30 | 19 | **35,0** [29,8–40,6] | 52,7 | 0 | 0 | `runs/v3_apps_seedcoder8b_bon16` |
| seedcoder8b | RethinkMCTS | 300 | 46 | 29 | 17 | **30,7** [25,7–36,1] | 48,8 | 0 | 0 | `runs/v3_apps_seedcoder8b_mcts` |
| qwen35_9b | Direct | — | — | — | — | — | — | — | — | — |
| qwen35_9b | Best-of-16 | — | — | — | — | — | — | — | — | — |
| qwen35_9b | RethinkMCTS | — | — | — | — | — | — | — | — | — |

## 3. HumanEval-164, Pass@1 (v3)

| Model | Phương pháp | Hoàn tất / 164 | **Pass@1 %** [Wilson 95%] | Số bài pass | Lỗi kỹ thuật | Nguồn |
|---|---|---|---|---|---|---|
| qwen25c7b | Direct | 164 | **77,4** [70,5–83,2] | 127 | 0 | `runs/v3_humaneval_qwen25c7b_direct` |
| qwen25c7b | Best-of-16 | 164 | **89,0** [83,3–92,9] | 146 | 0 | `runs/v3_humaneval_qwen25c7b_bon16` |
| qwen25c7b | RethinkMCTS | 164 | **90,9** [85,5–94,4] | 149 | 0 | `runs/v3_humaneval_qwen25c7b_mcts` |
| seedcoder8b | Direct | 164 | **78,7** [71,8–84,2] | 129 | 0 | `runs/v3_humaneval_seedcoder8b_direct` |
| seedcoder8b | Best-of-16 | 164 | **89,6** [84,0–93,4] | 147 | 0 | `runs/v3_humaneval_seedcoder8b_bon16` |
| seedcoder8b | RethinkMCTS | 164 | **90,2** [84,7–93,9] | 148 | 0 | `runs/v3_humaneval_seedcoder8b_mcts` |
| qwen35_9b | Direct | — | — | — | — | — |
| qwen35_9b | Best-of-16 | — | — | — | — | — |
| qwen35_9b | RethinkMCTS | — | — | — | — | — |

## 4. Kiểm định ghép cặp (v3)

`a-only` là số bài chỉ phương pháp A pass; `b-only` là số bài chỉ B pass. Dùng McNemar exact. `p (Holm)` hiệu chỉnh trên toàn bộ các so sánh của bảng này. CI là bootstrap 95% ghép cặp (10.000 lần, seed 0) của chênh lệch Pass@1. Holm tính trên 12 so sánh của 2 model đã xong; khi có qwen35_9b sẽ tính lại trên 18 so sánh. Script: [analyze_v3.py](../../scripts/analyze_v3.py).

| Dataset | Model | A vs B | n chung | a-only | b-only | p exact | p (Holm) | Δ P@1 (điểm %) | 95% CI | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|
| APPS | qwen25c7b | MCTS vs Direct | 300 | 42 | 8 | 1,2e-06 | 1e-05 | +11,3 | [7,0; 15,7] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| APPS | qwen25c7b | MCTS vs Best-of-16 | 300 | 22 | 21 | 1 | 1 | +0,3 | [-4,0; 4,7] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| APPS | qwen25c7b | Best-of-16 vs Direct | 300 | 37 | 4 | 1e-07 | 1e-06 | +11,0 | [7,0; 15,0] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| APPS | seedcoder8b | MCTS vs Direct | 300 | 47 | 6 | 5,8e-09 | 6,4e-08 | +13,7 | [9,3; 18,3] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| APPS | seedcoder8b | MCTS vs Best-of-16 | 300 | 20 | 33 | 0,098 | 0,39 | -4,3 | [-9,0; 0,3] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| APPS | seedcoder8b | Best-of-16 vs Direct | 300 | 59 | 5 | 9e-13 | 1,1e-11 | +18,0 | [13,3; 23,0] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| APPS | qwen35_9b | (3 so sánh) | — | — | — | — | — | — | — | chưa chạy xong |
| HE | qwen25c7b | MCTS vs Direct | 164 | 25 | 3 | 2,7e-05 | 0,00019 | +13,4 | [7,3; 19,5] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| HE | qwen25c7b | MCTS vs Best-of-16 | 164 | 7 | 4 | 0,55 | 1 | +1,8 | [-1,8; 6,1] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| HE | qwen25c7b | Best-of-16 vs Direct | 164 | 20 | 1 | 2,1e-05 | 0,00017 | +11,6 | [6,7; 17,1] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| HE | seedcoder8b | MCTS vs Direct | 164 | 23 | 4 | 0,00031 | 0,0016 | +11,6 | [6,1; 17,7] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| HE | seedcoder8b | MCTS vs Best-of-16 | 164 | 8 | 7 | 1 | 1 | +0,6 | [-3,7; 5,5] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| HE | seedcoder8b | Best-of-16 vs Direct | 164 | 19 | 1 | 4e-05 | 0,00024 | +11,0 | [6,1; 16,5] | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| HE | qwen35_9b | (3 so sánh) | — | — | — | — | — | — | — | chưa chạy xong |

## 5. Chi phí (v3)

Token lấy từ `usage.json` (vLLM báo, không ước lượng). GPU-giây lấy từ `modal billing report --show-resources` (hoặc thời gian phiên Colab) cho đúng khoảng thời gian của run. Giá: Modal L40S $1,95/giờ; Colab tính theo compute unit (ghi rõ tỷ giá đã dùng).

| Model | Dataset | Phương pháp | Input token/bài | Output token/bài | Lời gọi/bài | Wall TB (s) | Wall max (s) | GPU-giây | Chi phí | /bài | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | Direct | 625 | 252 | 1.0 | 9 | 50 | — | — | — | `runs/v3_apps_qwen25c7b_direct` |
| qwen25c7b | APPS | Best-of-16 | 10.001 | 4.214 | 16.0 | 132 | 690 | — | — | — | `runs/v3_apps_qwen25c7b_bon16` |
| qwen25c7b | APPS | RethinkMCTS | 161.378 | 18.316 | 70.5 | 460 | 1620 | — | — | — | `runs/v3_apps_qwen25c7b_mcts` |
| qwen25c7b | HE | Direct | 254 | 73 | 1.0 | 1 | 4 | — | — | — | `runs/v3_humaneval_qwen25c7b_direct` |
| qwen25c7b | HE | Best-of-16 | 4.061 | 1.289 | 16.0 | 20 | 66 | — | — | — | `runs/v3_humaneval_qwen25c7b_bon16` |
| qwen25c7b | HE | RethinkMCTS | 26.130 | 4.581 | 47.1 | 79 | 383 | — | — | — | `runs/v3_humaneval_qwen25c7b_mcts` |
| seedcoder8b | APPS | Direct | 681 | 339 | 1.0 | 12 | 71 | — | — | — | `runs/v3_apps_seedcoder8b_direct` |
| seedcoder8b | APPS | Best-of-16 | 10.898 | 5.006 | 16.0 | 159 | 1013 | — | — | — | `runs/v3_apps_seedcoder8b_bon16` |
| seedcoder8b | APPS | RethinkMCTS | 150.357 | 20.898 | 69.4 | 600 | 1620 | — | — | — | `runs/v3_apps_seedcoder8b_mcts` |
| seedcoder8b | HE | Direct | 309 | 75 | 1.0 | 1 | 6 | — | — | — | `runs/v3_humaneval_seedcoder8b_direct` |
| seedcoder8b | HE | Best-of-16 | 4.942 | 1.298 | 16.0 | 20 | 66 | — | — | — | `runs/v3_humaneval_seedcoder8b_bon16` |
| seedcoder8b | HE | RethinkMCTS | 24.274 | 3.818 | 43.7 | 76 | 404 | — | — | — | `runs/v3_humaneval_seedcoder8b_mcts` |
| qwen35_9b | APPS, HE | (3 phương pháp) | — | — | — | — | — | — | — | — | chưa chạy xong |

**GPU-giây và chi phí từng run để trống:** đợt chạy 12–13/11 bị Colab thu hồi máy nhiều lần, các run chạy chen nhau và chạy lại từ bản lưu, nên không tách được thời gian GPU theo run. Tổng cả đợt (gồm phần Qwen3.5 dở và các lần mất máy): 200 → 77,5 CU = **122,5 CU** (A100 6,73 CU/giờ). Wall là thời gian giải một bài với 16 bài chạy song song trên một GPU, không phải GPU-giây. So sánh chi phí giữa các phương pháp dùng token (cột input/output), vì cùng model và cùng GPU.

### 5.1. Token theo vai trò (RethinkMCTS, tổng trên cả run, input / output)

| Model | Dataset | expansion | code | rethink | critic | block_analysis | Tổng | Nguồn |
|---|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | 4,3M / 0,30M | 6,6M / 2,31M | 10,2M / 0,32M | 0,9M / 0,06M | 26,4M / 2,50M | 48,4M / 5,49M | `runs/v3_apps_qwen25c7b_mcts` |
| qwen25c7b | HE | 0,5M / 0,16M | 1,0M / 0,25M | 0,6M / 0,03M | 1,0M / 0,11M | 1,2M / 0,20M | 4,3M / 0,75M | `runs/v3_humaneval_qwen25c7b_mcts` |
| seedcoder8b | APPS | 4,0M / 0,24M | 6,9M / 2,86M | 9,8M / 0,28M | 1,3M / 0,07M | 23,2M / 2,81M | 45,2M / 6,28M | `runs/v3_apps_seedcoder8b_mcts` |
| seedcoder8b | HE | 0,6M / 0,11M | 1,0M / 0,26M | 0,4M / 0,02M | 1,1M / 0,10M | 0,8M / 0,13M | 4,0M / 0,63M | `runs/v3_humaneval_seedcoder8b_mcts` |
| qwen35_9b | APPS | — | — | — | — | — | — | chưa chạy xong |

## 6. Độ "khỏe" của search (RethinkMCTS, v3)

Lấy từ `scripts/pilot_report.py`. Đây là bằng chứng các cơ chế thật sự chạy. Ví dụ ở v1, cột "analysis vào feedback" là 0%.

| Model | Dataset | Rollout TB | Phân bố độ sâu tối đa | Node được đánh giá TB | Rethink TB | Analysis vào feedback % | Output bị cắt (length) % | `<think>` lọt ra | Bài chạm 3600 s | Lý do dừng | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | 16 | 3: 249, 4: 50, 5: 1 | 16 | 12,8 | 100 | 0,5 (115/21160) | 0 | 0 (max 1620 s) | budget_exhausted 300 | `runs/v3_apps_qwen25c7b_mcts` |
| qwen25c7b | HE | 16 | 3: 145, 4: 19 | 16 | 2,8 | 100 | 0,2 (12/7724) | 0 | 0 (max 383 s) | budget_exhausted 164 | `runs/v3_humaneval_qwen25c7b_mcts` |
| seedcoder8b | APPS | 16 | 3: 221, 4: 78, 5: 1 | 16 | 12,4 | 100 | 1,5 (307/20834) | 0 | 0 (max 1620 s) | budget_exhausted 300 | `runs/v3_apps_seedcoder8b_mcts` |
| seedcoder8b | HE | 16 | 3: 112, 4: 51, 5: 1 | 16 | 1,7 | 100 | 0,1 (9/7172) | 0 | 0 (max 404 s) | budget_exhausted 164 | `runs/v3_humaneval_seedcoder8b_mcts` |
| qwen35_9b | APPS, HE | — | — | — | — | — | — | — | — | — | chưa chạy xong |

## 7. Ablation thành phần (qwen25c7b, APPS)

Mỗi biến thể chỉ đổi một yếu tố so với RethinkMCTS đầy đủ, và so trên cùng tập bài.

| Biến thể | Thay đổi | n | Overall P@1 % | Δ so với đầy đủ | a-only / b-only | p exact | Token/bài | Nguồn |
|---|---|---|---|---|---|---|---|---|
| Đầy đủ | — | — | — | — | — | — | — | — |
| Tắt rethink | `search.max_rethinks_per_node=0` | — | — | — | — | — | — | — |
| Chỉ thông tin thực thi | `feedback.mode=facts_only` | — | — | — | — | — | — | — |

## 8. Critic: Dual so với Test-only (chọn lại offline từ E1)

Cùng một cây search, chỉ đổi cách chọn chương trình cuối: max reward dual, hoặc chỉ dùng public pass rate (hòa thì lấy ứng viên sinh trước). Không cần chạy GPU thêm. Phép tính lại là **chính xác** (trừ nhiễu vLLM): critic chỉ được gọi khi một ứng viên đã pass hết public, nên cây giống hệt cho tới ứng viên pass đầu tiên, và mọi ứng viên pass sau đó đều hòa ở reward 1,0. P@1 ở bảng này là verdict hidden **chấm lại trên máy local** (khớp verdict trên VM ở 298–299/300 bài APPS và 164/164 bài HE), nên có thể lệch 1–2 bài so với mục 2–3.

| Model | Dataset | Bài có ≥ 2 code khác nhau pass public | Dual P@1 % | Test-only P@1 % | Dual-only / Test-only-only | p exact | Nguồn |
|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | 110 | 29,0 | 27,3 | 5 / 0 | 0,062 | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| qwen25c7b | HE | 153 | 90,9 | 92,7 | 1 / 4 | 0,38 | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| seedcoder8b | APPS | 113 | 30,0 | 30,0 | 2 / 2 | 1 | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| seedcoder8b | HE | 155 | 90,2 | 91,5 | 0 / 2 | 0,5 | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| qwen35_9b | APPS | — | — | — | — | — | chưa chạy xong |

## 9. Dừng sớm tính lại offline (từ E1)

Phương án "dừng ở ứng viên đầu tiên pass hết public" được tính lại từ thứ tự sinh ứng viên trong run đầy đủ. Ứng viên được chọn khi dừng sớm trùng với ứng viên được chọn khi bỏ critic (mục 8), nên P@1 giống cột Test-only. Cột token tiết kiệm chưa tính.

| Model | Dataset | P@1 đầy đủ % | P@1 nếu dừng sớm % | Bài có kết quả khác | Token tiết kiệm % | Nguồn |
|---|---|---|---|---|---|---|
| qwen25c7b | APPS | 29,0 | 27,3 | 5 | — | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| qwen25c7b | HE | 90,9 | 92,7 | 5 | — | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| seedcoder8b | APPS | 30,0 | 30,0 | 4 | — | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| seedcoder8b | HE | 90,2 | 91,5 | 2 | — | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| qwen35_9b | APPS | — | — | — | — | chưa chạy xong |

## 10. Đường cong theo ngân sách (APPS)

Best-of-k tính offline từ 16 mẫu của E3: với mỗi k, lấy **k mẫu đầu tiên theo thứ tự sinh** (không lấy trung bình trên các tập con), chọn theo public pass rate, hòa thì lấy mẫu sinh trước, rồi chấm hidden trên máy local. Ô ghi P@1 % (số bài). MCTS@k chưa tính; dòng tham chiếu ghi P@1 của Direct (k=1, temperature 0) và của RethinkMCTS đầy đủ (khoảng 28–29 lần sinh code mỗi bài APPS, 18–19 lần mỗi bài HE).

| Model | Dataset | Phương pháp | k=1 | k=2 | k=4 | k=8 | k=16 | Nguồn |
|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | Best-of-k | 15,0 (45) | 19,7 (59) | 22,7 (68) | 26,0 (78) | 28,7 (86) | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| qwen25c7b | APPS | Tham chiếu: Direct / MCTS | 17,3 | — | — | — | MCTS 28,7 | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| qwen25c7b | HE | Best-of-k | 73,2 (120) | 84,1 (138) | 88,4 (145) | 88,4 (145) | 89,0 (146) | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| qwen25c7b | HE | Tham chiếu: Direct / MCTS | 77,4 | — | — | — | MCTS 90,9 | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| seedcoder8b | APPS | Best-of-k | 14,3 (43) | 23,0 (69) | 28,0 (84) | 32,7 (98) | 35,7 (107) | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| seedcoder8b | APPS | Tham chiếu: Direct / MCTS | 17,0 | — | — | — | MCTS 30,7 | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| seedcoder8b | HE | Best-of-k | 78,7 (129) | 82,3 (135) | 84,1 (138) | 87,2 (143) | 89,6 (147) | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| seedcoder8b | HE | Tham chiếu: Direct / MCTS | 78,7 | — | — | — | MCTS 90,2 | [analysis](v3/analysis_qwen25c7b_seedcoder8b.json) |
| qwen35_9b | APPS, HE | Best-of-k | — | — | — | — | — | chưa chạy xong |

## 12. Nhật ký vận hành đợt chạy 12–13/11/2026 (Colab A100)

Mọi run E1–E4 dùng code đóng băng `d9666c4` (protocol v3.1), cùng cấu hình vLLM (0.31.0, bf16, `--max-model-len 32768`, `--seed 0`), 16 bài song song, `test_workers=4`, `max_test_processes=8`, Python 3.11.17. Log từng phiên: `runs/colab_overnight_logs/` (file `*.log` bị `.gitignore`, chỉ có ở máy local). Các file nặng của mỗi run (`requests.json`, `feedback.json`, `evaluations.json`) được nén trong `runs/v3_raw_archives/<run>.heavy.tar.gz`; một số `evaluations.json` lớn hơn giới hạn 100 MB của GitHub.

1. **Colab thu hồi máy.** Từ khoảng 01:45 đến 10:10 ngày 13/11, gần như mọi runtime đều biến mất sau khoảng 22–25 phút (lỗi 404 từ contents API; CLI không gửi lệnh `unassign` nào), với cả ba model, chạy một mình hay song song. Có vài máy sống lâu (một phiên `seed` từ 06:02 sống 3,75 giờ). Nguyên nhân chưa rõ. Đã loại trừ ssh, việc tải bản lưu và việc chạy song song. Cách xử lý: trên VM đóng gói `runs/` mỗi 5 phút, [guard_dl.sh](../../deploy/colab/guard_dl.sh) tải bản lưu về, rồi chạy tiếp trên VM mới bằng `SEED_RUNS` ([orchestrate_ls.sh](../../deploy/colab/orchestrate_ls.sh)). Resume theo từng bài: bài đã có `completed.json` được giữ nguyên, bài đang chạy dở khi mất máy được giải lại từ đầu. Manifest (cấu hình, dữ liệu, prompt, mã nguồn, runtime) khớp ở mọi lần resume.
2. **Lỗi kiểm tra khi resume (CRLF).** `_load_completed` đọc `selected.py` bằng `read_text()`, hàm này đổi `\r\n` thành `\n` nên mã băm lệch và resume báo "Corrupted resume artifact" dù artifact đúng. Lỗi gặp ở 3 bài Best-of-16 của qwen25c7b (`apps_1684`, `apps_2408`, `apps_3298`). Cách xử lý: chuyển các bài này ra ngoài để chúng được giải lại như một bài lỗi; kết quả lần đầu lưu ở `runs/v3_raw_archives/crlf_resume_victims_q7rest.tar.gz`. Tiêu chí loại chỉ dựa vào ký tự xuống dòng của code, không phụ thuộc verdict, nên không gây thiên lệch. Code đóng băng chưa sửa vì sửa sẽ làm đổi `source_hash` trong manifest; sẽ sửa sau đợt chạy.
3. **Thứ tự chạy.** Với `seedcoder8b` và `qwen35_9b`, thứ tự các run trong hàng đợi được đổi để các run ngắn chạy trước và MCTS APPS chạy sau cùng. Mỗi run có thư mục riêng và cùng code, nên thứ tự không ảnh hưởng kết quả.
4. **qwen35_9b chưa xong, đang tạm dừng.** Gate v3.1 đã qua. Đã có MCTS APPS 113/300 và Best-of-16 APPS 68/300; các run còn lại chưa chạy. Mỗi lần khởi động mất khoảng 9 phút (tải model 55 s, vLLM init khoảng 5 phút), còn máy chỉ sống khoảng 23 phút, nên MCTS (hơn 10 phút mỗi bài) không tiến được. Bản lưu: `colab_results/qwen35_paused/partial_1100_latest.tar.gz` (chỉ ở local).
5. **Kiểm tra chấm lại.** Chấm lại hidden trên máy local cho ra cùng verdict với VM ở 298–299/300 bài APPS và 164/164 bài HE.

---

## 11. Pilot v3 (không phải kết quả, không đưa vào chương 4)

20 bài APPS ngoài cohort ([apps_pilot_20.json](../../data/cohorts/apps_pilot_20.json)). Tiêu chí đạt ở [configs/v3_7b/README.md](../../configs/v3_7b/README.md).

| Bước | Run (`runs/…`) | Model | Phương pháp | Bài | Nền tảng | Ngày | Trạng thái |
|---|---|---|---|---|---|---|---|
| P1 | `v3_pilot_apps_qwen25c7b_mcts_smoke` | qwen25c7b | MCTS | 3 | Colab A100-SXM4-40GB | 12/11/2026 | ✅ |
| P2 | `v3_pilot_apps_qwen25c7b_{mcts,bon16,direct}` | qwen25c7b | 3 phương pháp | 20 | Colab A100-SXM4-40GB | 12/11/2026 | ✅ |
| P2b | `v3_pilot_apps_qwen25c7b_mcts_par` | qwen25c7b | MCTS, 16 worker, `test_workers=4`, `max_test_processes=8` | 20 | Colab A100-SXM4-40GB | 12/11/2026 | ✅ |
| P3 | `v3_pilot_apps_{seedcoder8b,qwen35_9b}_{mcts,direct}` | 2 model | MCTS, Direct | 5 | — | — | ⏳ |
| P3 | `v3_pilot_humaneval_{seedcoder8b,qwen35_9b}_mcts` | 2 model | MCTS (kiểm tra định dạng) | 3 | — | — | ⏳ |
| P4 | `v3_pilot_apps_qwen25c7b_{direct,mcts}_l4` | qwen25c7b | Direct, MCTS trên L4 | 5 | — | — | ⏳ (tùy chọn) |

**Môi trường Colab (P1, P2):** phiên `tlcn`, NVIDIA A100-SXM4-40GB, driver 580.82, CUDA 13.0, 12 vCPU, 83 GB RAM. vLLM 0.31.0 (torch 2.13.0+cu130) chạy trên Python 3.13 hệ thống, với các tham số `--dtype bfloat16 --max-model-len 16384 --gpu-memory-utilization 0.90 --seed 0`, prefix caching bật. Solver, trace và phần chạy test dùng **Python 3.11.17** (`/content/py311`). Code là `git archive` của commit `c325c19`, không có `.git` nên manifest không ghi được commit; `pilot_report.py` đã sửa sau P1 để bỏ node gốc khỏi phép đếm.

**Phát hiện khi dựng môi trường:** với Python 3.13, 3 test về trace fail (`test_i17_recursion…`, `test_trace_invokes_actual_function_harness`): trace bỏ sót lượt chạy, hàm đệ quy chỉ bắt được 1 lượt. Với Python 3.11 cả 82 test pass. Từ đó quy ước: **solver và sandbox phải chạy Python 3.11**.

**P1, số đo (3 bài):** input 90.390 / output 13.503 token TB mỗi bài; 75 lời gọi TB; 30,67 lần sinh code (16 initial + 14,67 rethink); wall TB 352 s, max 456 s với 3 worker; dừng vì hết 16 rollout (3/3).

**P2, số đo (20 bài APPS interview ngoài cohort; không phải kết quả):**

| Run | Input / output token TB/bài | Lời gọi TB | Wall TB / max (s) | Thời gian cả run |
|---|---|---|---|---|
| MCTS, 8 worker, test tuần tự | 127.650 / 15.588 | 75 | 429 / 1.736 | 32,4 phút |
| MCTS, 16 worker, `test_workers=4`, `max_test_processes=8` (P2b) | 128.339 / 15.679 | 74,8 | 531 / 1.136 | **18,9 phút** |
| Best-of-16 (temperature 0,8) | 8.834 / 3.413 | 16 | 196 / 1.501 | 25 phút |
| Direct | 552 / 208 | 1 | 18 / 209 | 9 phút |

Nguồn: `runs/v3_pilot_apps_qwen25c7b_*`, log ở `runs/colab_pilot_logs/`. Phân rã thời gian của P2 MCTS: 54% chờ model, khoảng 30% chờ test timeout (649 lần × 4 s); phần còn lại là khởi động tiến trình test.

**Chạy test song song có làm sai verdict không:** chấm lại **tuần tự** đúng các test bị timeout trong P2b của `apps_18`, `apps_11`, `apps_41`, `apps_25`: 121/122 vẫn timeout. Vậy timeout đến từ code chậm thật, không phải do tranh CPU; chỉ 1 test sát ngưỡng. Kết luận: chốt cấu hình P2b cho run thật. Ngoài ra, giữa P2 và P2b có 2/18 bài đổi verdict hidden và token lệch từng bài, do vLLM với temperature 0 vẫn không tất định khi batch khác nhau. Đây là nhiễu giữa các lần chạy, phải ghi vào threats to validity.

| Tiêu chí | Ngưỡng | P1 | P2 | P3 |
|---|---|---|---|---|
| Lỗi template (`strict_variables`) | 0 | 0 ✅ | 0 ✅ | — |
| Bài lỗi kỹ thuật | ≤ 1/20 | 0/3 ✅ | 0/80 lượt (4 run × 20) ✅ | — |
| Analysis vào feedback | ≥ 90% | 61/61 = 100% ✅ | 100% (MCTS, MCTS song song) ✅ | — |
| Rollout TB / có bài sâu ≥ 3 | 16 / có | 16 / độ sâu 3: 2 bài, 4: 1 bài ✅ | 16 / độ sâu 3: 19, 4: 1 (P2b: 14 / 6) ✅ | — |
| Output bị cắt | ≤ 5% lời gọi | 0/225 ✅ | MCTS 7/1.500, BoN 0/320, Direct 0/20 ✅ | — |
| `<think>` lọt ra | 0 | 0 ✅ | 0 ✅ | — |
| Bài chạm 3600 s | 0 | 0 (max 456 s) ✅ | 0 (max 1.736 s, `apps_6` có 112 public test) ✅ | — |
| GPU-giây/bài → chi phí ước tính 300 bài | trong credit còn lại | — | — | — |

---

## Phụ lục: kết quả trước v3

Kết quả 14B v1 (Qwen2.5-Coder-14B) và nhánh 7B của HuyinCP thuộc protocol khác, có lỗi đã biết (D-006), nên **không dùng cho kết luận**. Ngày 13/11/2026 chúng đã được gỡ khỏi nhánh, cùng các bảng phụ lục A/B trước đây của sổ này. Có thể lấy lại bằng `git show archive/pre-v3-2026-11-13:docs/results/BENCHMARK_LEDGER.md`, hoặc lấy thẳng artifact với `git checkout archive/pre-v3-2026-11-13 -- runs/<run>`.
