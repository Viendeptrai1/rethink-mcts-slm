# Sổ kết quả benchmark

Bảng ghi chép **mọi** thứ của các đợt chạy benchmark: run nào, cấu hình gì, chạy ở đâu, kết quả, chi phí và độ "khỏe" của search. Khung báo cáo: [KHUNG_BAO_CAO_v2.md](../report/KHUNG_BAO_CAO_v2.md). Cấu hình v3: [configs/v3_7b/README.md](../../configs/v3_7b/README.md).

Cập nhật lần cuối: 14/11/2026. Đã xong E1–E4 cho cả ba model (18 run) và các phân tích offline (critic theo mức khó, dừng sớm, MCTS@k; mục 8–10). Với `qwen35_9b`: 5 run chạy trên Modal, MCTS APPS chạy trên Colab (mục 1, mục 12); các ô APPS có cảnh báo output bị cắt (mục 6.1).

## Quy ước

- **Không trộn protocol.** Sổ này chỉ chứa protocol v3.1 (mục 1–10, 12) và pilot v3.0 (mục 11, không phải kết quả).
- Mọi con số phải có nguồn là một artifact trong `runs/` hoặc `docs/results/`. Ô chưa có số thì để `—`.
- Trạng thái: `⏳` chưa chạy · `▶` đang chạy · `✅` xong và đã đối chiếu artifact · `⚠️` xong nhưng có vấn đề (ghi chú) · `✗` hủy.
- **Pass@1 (hidden):** tỷ lệ bài mà chương trình được chọn pass toàn bộ hidden test, mẫu số là cả cohort (bài lỗi hoặc không có candidate tính 0). **Pass rate:** trung bình theo bài của tỷ lệ hidden test pass.
- Số liệu v3 lấy bằng `scripts/pilot_report.py` (search, chi phí) và [analyze_v3.py](../../scripts/analyze_v3.py) (phân tích ghép cặp, chọn lại offline, Best-of-k).
- Tên ngắn của model: `qwen25c7b` = Qwen2.5-Coder-7B-Instruct · `seedcoder8b` = Seed-Coder-8B-Instruct · `qwen35_9b` = Qwen3.5-9B (tắt thinking) · `granite42_8b` = Granite-4.2-8B (dự phòng).

---

## 1. Sổ đăng ký run v3

Thư mục run đặt theo mẫu `runs/v3_<dataset>_<model>_<method>`. Commit, GPU, phiên bản vLLM và số worker phải điền **trước khi** chạy. Với mỗi model, mọi phương pháp phải chạy trên cùng nền tảng.

| Mã | Run (`runs/…`) | Model | Dataset | Phương pháp | Config | Commit | Nền tảng / GPU | vLLM | Workers | Ngày | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E1 | `v3_apps_qwen25c7b_mcts` | qwen25c7b | APPS-300 | MCTS | `apps_mcts.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E1 | `v3_apps_seedcoder8b_mcts` | seedcoder8b | APPS-300 | MCTS | `apps_mcts.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E1 | `v3_apps_qwen35_9b_mcts` | qwen35_9b | APPS-300 | MCTS | `apps_mcts.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 13–14/11/2026 | ⚠️ (output bị cắt, 17 bài không có candidate; mục 6.1) |
| E2 | `v3_apps_qwen25c7b_direct` | qwen25c7b | APPS-300 | Direct | `apps_baseline.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E2 | `v3_apps_seedcoder8b_direct` | seedcoder8b | APPS-300 | Direct | `apps_baseline.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E2 | `v3_apps_qwen35_9b_direct` | qwen35_9b | APPS-300 | Direct | `apps_baseline.yaml` | `d9666c4` | Modal A100-SXM4-40GB | 0.31.0 | 16 | 13/11/2026 | ⚠️ (output bị cắt, mục 6.1) |
| E3 | `v3_apps_qwen25c7b_bon16` | qwen25c7b | APPS-300 | Best-of-16 | `apps_baseline.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ (3 bài giải lại, mục 12) |
| E3 | `v3_apps_seedcoder8b_bon16` | seedcoder8b | APPS-300 | Best-of-16 | `apps_baseline.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E3 | `v3_apps_qwen35_9b_bon16` | qwen35_9b | APPS-300 | Best-of-16 | `apps_baseline.yaml` | `d9666c4` | Modal A100-SXM4-40GB | 0.31.0 | 16 | 13/11/2026 | ⚠️ (output bị cắt, mục 6.1) |
| E4 | `v3_humaneval_qwen25c7b_mcts` | qwen25c7b | HE-164 | MCTS | `humaneval_mcts.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E4 | `v3_humaneval_seedcoder8b_mcts` | seedcoder8b | HE-164 | MCTS | `humaneval_mcts.yaml` | `d9666c4` | Colab A100-SXM4-40GB | 0.31.0 | 16 | 12–13/11/2026 | ✅ |
| E4 | `v3_humaneval_qwen35_9b_mcts` | qwen35_9b | HE-164 | MCTS | `humaneval_mcts.yaml` | `d9666c4` | Modal A100-SXM4-40GB | 0.31.0 | 16 | 13/11/2026 | ✅ |
| E2 | `v3_humaneval_{qwen25c7b,seedcoder8b,qwen35_9b}_direct` | 3 model | HE-164 | Direct | `humaneval_baseline.yaml` | `d9666c4` | Colab (qwen25c7b, seedcoder8b) · Modal (qwen35_9b), A100-SXM4-40GB | 0.31.0 | 16 | 13/11/2026 | ✅ |
| E3 | `v3_humaneval_{qwen25c7b,seedcoder8b,qwen35_9b}_bon16` | 3 model | HE-164 | Best-of-16 | `humaneval_baseline.yaml` | `d9666c4` | Colab (qwen25c7b, seedcoder8b) · Modal (qwen35_9b), A100-SXM4-40GB | 0.31.0 | 16 | 13/11/2026 | ✅ |
| E5 | `v3_apps_qwen25c7b_norethink` | qwen25c7b | APPS (300 hoặc 150) | MCTS, `max_rethinks_per_node=0` | `apps_mcts.yaml` | — | — | — | — | — | ⏳ (nếu còn tiền) |
| E6 | `v3_apps_qwen25c7b_factsonly` | qwen25c7b | APPS (300 hoặc 150) | MCTS, `feedback.mode=facts_only` | `apps_mcts.yaml` | — | — | — | — | — | ⏳ (nếu còn tiền) |

Best-of-16 chạy với `--set sampling.code.temperature=0.8 --set sampling.code.top_p=0.95`. Nếu đổi giá trị này, ghi vào cột Config.

**Ngoại lệ về nền tảng của `qwen35_9b`:** 5 run chạy trên Modal, còn MCTS APPS chạy trên Colab. Cả hai đều là A100-SXM4-40GB, cùng code `d9666c4`, cùng cấu hình vLLM, và gate của hai nền tảng khớp 12/13 bài. Tuy vậy vẫn là hai nền tảng khác nhau (Colab chạy kernel Linux 6.6, Modal chạy gVisor), nên quy tắc "cùng nền tảng" bị vi phạm ở ô APPS của model này. Phải ghi điều này vào threats to validity.

## 2. APPS-300, Pass@1 trên hidden test (v3)

| Model | Phương pháp | Hoàn tất / 300 | Intro (số bài /100) | Inter (/100) | Comp (/100) | **Overall P@1 %** [Wilson 95%] | Overall pass rate % | Lỗi kỹ thuật (ID) | Chạm 3600 s | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen25c7b | Direct | 300 | 33 | 12 | 7 | **17,3** [13,5–22,0] | 33,0 | 0 | 0 | `runs/v3_apps_qwen25c7b_direct` |
| qwen25c7b | Best-of-16 | 300 | 50 | 21 | 14 | **28,3** [23,5–33,7] | 48,4 | 0 | 0 | `runs/v3_apps_qwen25c7b_bon16` |
| qwen25c7b | RethinkMCTS | 300 | 49 | 25 | 12 | **28,7** [23,8–34,0] | 48,4 | 0 | 0 | `runs/v3_apps_qwen25c7b_mcts` |
| seedcoder8b | Direct | 300 | 33 | 12 | 6 | **17,0** [13,2–21,7] | 30,1 | 0 | 0 | `runs/v3_apps_seedcoder8b_direct` |
| seedcoder8b | Best-of-16 | 300 | 56 | 30 | 19 | **35,0** [29,8–40,6] | 52,7 | 0 | 0 | `runs/v3_apps_seedcoder8b_bon16` |
| seedcoder8b | RethinkMCTS | 300 | 46 | 29 | 17 | **30,7** [25,7–36,1] | 48,8 | 0 | 0 | `runs/v3_apps_seedcoder8b_mcts` |
| qwen35_9b | Direct ⚠️ | 300 | 64 | 46 | 23 | **44,3** [38,8–50,0] | 52,3 | 0 | 0 | `runs/v3_apps_qwen35_9b_direct` |
| qwen35_9b | Best-of-16 ⚠️ | 300 | 82 | 75 | 46 | **67,7** [62,2–72,7] | 74,4 | 0 | 0 | `runs/v3_apps_qwen35_9b_bon16` |
| qwen35_9b | RethinkMCTS ⚠️ | 300 | 81 | 70 | 43 | **64,7** [59,1–69,9] | 73,5 | 0 (17 bài không có candidate, tính 0; mục 6.1) | 0 | `runs/v3_apps_qwen35_9b_mcts` |

⚠️ Output của `qwen35_9b` bị cắt nhiều ở cả ba phương pháp (mục 6.1). Pass rate của MCTS tính trên cả 300 bài, bài không có candidate tính 0.

## 3. HumanEval-164, Pass@1 (v3)

| Model | Phương pháp | Hoàn tất / 164 | **Pass@1 %** [Wilson 95%] | Số bài pass | Lỗi kỹ thuật | Nguồn |
|---|---|---|---|---|---|---|
| qwen25c7b | Direct | 164 | **77,4** [70,5–83,2] | 127 | 0 | `runs/v3_humaneval_qwen25c7b_direct` |
| qwen25c7b | Best-of-16 | 164 | **89,0** [83,3–92,9] | 146 | 0 | `runs/v3_humaneval_qwen25c7b_bon16` |
| qwen25c7b | RethinkMCTS | 164 | **90,9** [85,5–94,4] | 149 | 0 | `runs/v3_humaneval_qwen25c7b_mcts` |
| seedcoder8b | Direct | 164 | **78,7** [71,8–84,2] | 129 | 0 | `runs/v3_humaneval_seedcoder8b_direct` |
| seedcoder8b | Best-of-16 | 164 | **89,6** [84,0–93,4] | 147 | 0 | `runs/v3_humaneval_seedcoder8b_bon16` |
| seedcoder8b | RethinkMCTS | 164 | **90,2** [84,7–93,9] | 148 | 0 | `runs/v3_humaneval_seedcoder8b_mcts` |
| qwen35_9b | Direct | 164 | **86,0** [79,8–90,5] | 141 | 0 | `runs/v3_humaneval_qwen35_9b_direct` |
| qwen35_9b | Best-of-16 | 164 | **93,3** [88,4–96,2] | 153 | 0 | `runs/v3_humaneval_qwen35_9b_bon16` |
| qwen35_9b | RethinkMCTS | 164 | **94,5** [89,9–97,1] | 155 | 0 (1 bài không sinh được candidate nào, `python_128`, tính 0) | `runs/v3_humaneval_qwen35_9b_mcts` |

## 4. Kiểm định ghép cặp (v3)

`a-only` là số bài chỉ phương pháp A pass; `b-only` là số bài chỉ B pass. Dùng McNemar exact. `p (Holm)` hiệu chỉnh trên toàn bộ các so sánh của bảng này. CI là bootstrap 95% ghép cặp (10.000 lần, seed 0) của chênh lệch Pass@1. Holm tính trên cả 18 so sánh (3 model × 2 dataset × 3 cặp). Với Holm, Best-of-16 vs Direct của qwen35_9b trên HE không còn có ý nghĩa ở mức 0,05 (p Holm 0,053). Script: [analyze_v3.py](../../scripts/analyze_v3.py).

| Dataset | Model | A vs B | n chung | a-only | b-only | p exact | p (Holm) | Δ P@1 (điểm %) | 95% CI | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|
| APPS | qwen25c7b | MCTS vs Direct | 300 | 42 | 8 | 1,2e-06 | 1,5e-05 | +11,3 | [7,0; 15,7] | [analysis](v3/analysis_v3_3models.json) |
| APPS | qwen25c7b | MCTS vs Best-of-16 | 300 | 22 | 21 | 1 | 1 | +0,3 | [-4,0; 4,7] | [analysis](v3/analysis_v3_3models.json) |
| APPS | qwen25c7b | Best-of-16 vs Direct | 300 | 37 | 4 | 1e-07 | 1,4e-06 | +11,0 | [7,0; 15,0] | [analysis](v3/analysis_v3_3models.json) |
| APPS | seedcoder8b | MCTS vs Direct | 300 | 47 | 6 | 5,8e-09 | 8,7e-08 | +13,7 | [9,3; 18,3] | [analysis](v3/analysis_v3_3models.json) |
| APPS | seedcoder8b | MCTS vs Best-of-16 | 300 | 20 | 33 | 0,098 | 0,59 | -4,3 | [-9,0; 0,3] | [analysis](v3/analysis_v3_3models.json) |
| APPS | seedcoder8b | Best-of-16 vs Direct | 300 | 59 | 5 | 9e-13 | 1,4e-11 | +18,0 | [13,3; 23,0] | [analysis](v3/analysis_v3_3models.json) |
| APPS | qwen35_9b | MCTS vs Direct ⚠️ | 300 | 68 | 7 | 1,2e-13 | 2e-12 | +20,3 | [15,3; 25,7] | [analysis](v3/analysis_v3_3models.json) |
| APPS | qwen35_9b | MCTS vs Best-of-16 ⚠️ | 300 | 10 | 19 | 0,14 | 0,68 | -3,0 | [-6,7; 0,3] | [analysis](v3/analysis_v3_3models.json) |
| APPS | qwen35_9b | Best-of-16 vs Direct ⚠️ | 300 | 73 | 3 | 1,9e-18 | 3,5e-17 | +23,3 | [18,3; 28,3] | [analysis](v3/analysis_v3_3models.json) |
| HE | qwen25c7b | MCTS vs Direct | 164 | 25 | 3 | 2,7e-05 | 0,0003 | +13,4 | [7,3; 19,5] | [analysis](v3/analysis_v3_3models.json) |
| HE | qwen25c7b | MCTS vs Best-of-16 | 164 | 7 | 4 | 0,55 | 1 | +1,8 | [-1,8; 6,1] | [analysis](v3/analysis_v3_3models.json) |
| HE | qwen25c7b | Best-of-16 vs Direct | 164 | 20 | 1 | 2,1e-05 | 0,00025 | +11,6 | [6,7; 17,1] | [analysis](v3/analysis_v3_3models.json) |
| HE | seedcoder8b | MCTS vs Direct | 164 | 23 | 4 | 0,00031 | 0,0028 | +11,6 | [6,1; 17,7] | [analysis](v3/analysis_v3_3models.json) |
| HE | seedcoder8b | MCTS vs Best-of-16 | 164 | 8 | 7 | 1 | 1 | +0,6 | [-3,7; 5,5] | [analysis](v3/analysis_v3_3models.json) |
| HE | seedcoder8b | Best-of-16 vs Direct | 164 | 19 | 1 | 4e-05 | 0,0004 | +11,0 | [6,1; 16,5] | [analysis](v3/analysis_v3_3models.json) |
| HE | qwen35_9b | MCTS vs Direct | 164 | 17 | 3 | 0,0026 | 0,021 | +8,5 | [3,7; 13,4] | [analysis](v3/analysis_v3_3models.json) |
| HE | qwen35_9b | MCTS vs Best-of-16 | 164 | 7 | 5 | 0,77 | 1 | +1,2 | [-3,0; 5,5] | [analysis](v3/analysis_v3_3models.json) |
| HE | qwen35_9b | Best-of-16 vs Direct | 164 | 15 | 3 | 0,0075 | 0,053 | +7,3 | [2,4; 12,8] | [analysis](v3/analysis_v3_3models.json) |

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
| seedcoder8b | APPS | RethinkMCTS | 150.860 | 20.955 | 69.4 | 600 | 1620 | — | — | — | `runs/v3_apps_seedcoder8b_mcts` |
| seedcoder8b | HE | Direct | 309 | 75 | 1.0 | 1 | 6 | — | — | — | `runs/v3_humaneval_seedcoder8b_direct` |
| seedcoder8b | HE | Best-of-16 | 4.942 | 1.298 | 16.0 | 20 | 66 | — | — | — | `runs/v3_humaneval_seedcoder8b_bon16` |
| seedcoder8b | HE | RethinkMCTS | 24.274 | 3.818 | 43.7 | 76 | 404 | — | — | — | `runs/v3_humaneval_seedcoder8b_mcts` |
| qwen35_9b | APPS | Direct | 626 | 1.813 | 1.0 | 30 | 70 | — | — | — | `runs/v3_apps_qwen35_9b_direct` |
| qwen35_9b | APPS | Best-of-16 | 10.012 | 30.673 | 16.0 | 508 | 1100 | — | — | — | `runs/v3_apps_qwen35_9b_bon16` |
| qwen35_9b | APPS | RethinkMCTS | 112.692 | 49.944 | 53.6 | 972 | 2860 | — | — | — | `runs/v3_apps_qwen35_9b_mcts` |
| qwen35_9b | HE | Direct | 249 | 194 | 1.0 | 3 | 53 | — | — | — | `runs/v3_humaneval_qwen35_9b_direct` |
| qwen35_9b | HE | Best-of-16 | 3.978 | 3.133 | 16.0 | 55 | 620 | — | — | — | `runs/v3_humaneval_qwen35_9b_bon16` |
| qwen35_9b | HE | RethinkMCTS | 21.967 | 6.149 | 41.9 | 121 | 756 | — | — | — | `runs/v3_humaneval_qwen35_9b_mcts` |

**Token của bài có lời gọi thiếu số đếm:** 4 bài MCTS APPS (`seedcoder8b`: `apps_4181`; `qwen35_9b`: `apps_3013`, `apps_3869`, `apps_624`) có một lời gọi `block_analysis` không có số token, nên `usage.json` ghi null cho tổng token của cả bài. Từ 14/11/2026, token của các bài này được cộng từ log từng request (`requests.json`, mọi lời gọi khác đều có số), thay vì tính 0 hoặc bỏ bài. Vì vậy hai dòng trên tăng so với bản trước (150.357 / 20.898 và 110.003 / 49.484); các phân tích và hình đều dùng số mới.

**GPU-giây và chi phí từng run để trống:** đợt chạy 12–13/11 bị Colab thu hồi máy nhiều lần, các run chạy chen nhau và chạy lại từ bản lưu, nên không tách được thời gian GPU theo run. Tổng cả đợt (gồm phần Qwen3.5 dở và các lần mất máy): 200 → 77,5 CU = **122,5 CU** (A100 6,73 CU/giờ). Wall là thời gian giải một bài với 16 bài chạy song song trên một GPU, không phải GPU-giây. So sánh chi phí giữa các phương pháp dùng token (cột input/output), vì cùng model và cùng GPU. Với `qwen35_9b`, 5 run trên Modal chạy liên tiếp trong một container, nên cũng không tách GPU-giây theo run; trang billing Modal ghi khoảng 30,4 USD cho cả đợt (gồm các lần khởi động lỗi và lần bị hủy lúc 17:28). MCTS APPS của `qwen35_9b` trên Colab, tối 13/11 đến sáng 14/11: 66,43 → 30,52 CU = **35,9 CU** (gồm một lần mất máy sau 27 phút và khoảng 25 phút máy chạy không sau khi xong, do `watch_ls.sh` bị treo). Output token của `qwen35_9b` trên APPS cao hơn hai model kia nhiều (Direct 1.813 so với 252–339) vì model viết lập luận dài trong comment của code (mục 6.1).

### 5.1. Token theo vai trò (RethinkMCTS, tổng trên cả run, input / output)

| Model | Dataset | expansion | code | rethink | critic | block_analysis | Tổng | Nguồn |
|---|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | 4,3M / 0,30M | 6,6M / 2,31M | 10,2M / 0,32M | 0,9M / 0,06M | 26,4M / 2,50M | 48,4M / 5,49M | `runs/v3_apps_qwen25c7b_mcts` |
| qwen25c7b | HE | 0,5M / 0,16M | 1,0M / 0,25M | 0,6M / 0,03M | 1,0M / 0,11M | 1,2M / 0,20M | 4,3M / 0,75M | `runs/v3_humaneval_qwen25c7b_mcts` |
| seedcoder8b | APPS | 4,0M / 0,24M | 6,9M / 2,86M | 9,8M / 0,28M | 1,3M / 0,07M | 23,3M / 2,82M | 45,3M / 6,29M | `runs/v3_apps_seedcoder8b_mcts` |
| seedcoder8b | HE | 0,6M / 0,11M | 1,0M / 0,26M | 0,4M / 0,02M | 1,1M / 0,10M | 0,8M / 0,13M | 4,0M / 0,63M | `runs/v3_humaneval_seedcoder8b_mcts` |
| qwen35_9b | APPS | 3,1M / 0,83M | 5,4M / 11,59M | 6,0M / 0,28M | 4,1M / 0,19M | 15,2M / 2,10M | 33,8M / 14,98M (thiếu số của 3 lời gọi `block_analysis`) | `runs/v3_apps_qwen35_9b_mcts` |
| qwen35_9b | HE | 0,5M / 0,20M | 0,9M / 0,50M | 0,3M / 0,01M | 1,3M / 0,14M | 0,5M / 0,16M | 3,6M / 1,01M | `runs/v3_humaneval_qwen35_9b_mcts` |

## 6. Độ "khỏe" của search (RethinkMCTS, v3)

Lấy từ `scripts/pilot_report.py`. Đây là bằng chứng các cơ chế thật sự chạy. Ví dụ ở v1, cột "analysis vào feedback" là 0%.

| Model | Dataset | Rollout TB | Phân bố độ sâu tối đa | Node được đánh giá TB | Rethink TB | Analysis vào feedback % | Output bị cắt (length) % | `<think>` lọt ra | Bài chạm 3600 s | Lý do dừng | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | 16 | 3: 249, 4: 50, 5: 1 | 16 | 12,8 | 100 | 0,5 (115/21160) | 0 | 0 (max 1620 s) | budget_exhausted 300 | `runs/v3_apps_qwen25c7b_mcts` |
| qwen25c7b | HE | 16 | 3: 145, 4: 19 | 16 | 2,8 | 100 | 0,2 (12/7724) | 0 | 0 (max 383 s) | budget_exhausted 164 | `runs/v3_humaneval_qwen25c7b_mcts` |
| seedcoder8b | APPS | 16 | 3: 221, 4: 78, 5: 1 | 16 | 12,4 | 100 | 1,5 (307/20834) | 0 | 0 (max 1620 s) | budget_exhausted 300 | `runs/v3_apps_seedcoder8b_mcts` |
| seedcoder8b | HE | 16 | 3: 112, 4: 51, 5: 1 | 16 | 1,7 | 100 | 0,1 (9/7172) | 0 | 0 (max 404 s) | budget_exhausted 164 | `runs/v3_humaneval_seedcoder8b_mcts` |
| qwen35_9b | APPS | 14,7 | 0: 17, 1: 5, 2: 3, 3: 151, 4: 84, 5: 27, 6: 8, 7: 5 | 14,7 | 6,2 | 100 | ⚠️ 16,4 (2638/16084; `code` 28%) | 0 | 0 (max 2860 s) | budget_exhausted 273, tree_exhausted 27 | `runs/v3_apps_qwen35_9b_mcts` |
| qwen35_9b | HE | 15,9 | 0: 1, 3: 99, 4: 63, 5: 1 | 15,9 | 1,0 | 100 | 1,2 (84/6872) | 0 | 0 (max 756 s) | budget_exhausted 163, tree_exhausted 1 | `runs/v3_humaneval_qwen35_9b_mcts` |

### 6.1. Output bị cắt ở `qwen35_9b` trên APPS ⚠️

Tiêu chí pilot là tối đa 5% lời gọi bị cắt (`finish_reason=length`). `qwen35_9b` (tắt thinking) không đạt tiêu chí này trên APPS: model viết lập luận rất dài trong comment của code cho tới khi chạm giới hạn 4096 token của vai trò `code`, và viết expansion dài quá giới hạn 1024 token. HumanEval không bị ảnh hưởng (Direct 0/164, Best-of-16 14/2624, MCTS 84/6872). Hai model kia gần như không bị (Direct APPS: `qwen25c7b` 0/300, `seedcoder8b` 1/300).

| Run | Lời gọi bị cắt | Ghi chú | Nguồn |
|---|---|---|---|
| Direct APPS | 78/300 (26%) | không bài nào trong 78 bài này pass hidden | `runs/v3_apps_qwen35_9b_direct` (`requests.json`) |
| Best-of-16 APPS | 1402/4800 (29%) | | `runs/v3_apps_qwen35_9b_bon16` |
| MCTS APPS | 2638/16084 (16%): `code` 1765/6284 (28%), `expansion` 259/2311 (11%), `block_analysis` 389/2689, `rethink` 132/2001, `critic` 93/2799 | **17 bài không có candidate nào**: cả hai lời gọi expansion ở gốc đều bị cắt, không tách được ý tưởng nào, cây dừng (`tree_exhausted`) sau khoảng 40 s. Các bài này tính 0. | `runs/v3_apps_qwen35_9b_mcts` (`requests.json`) |

Vì cả ba phương pháp dùng cùng giới hạn token, so sánh ghép cặp trong `qwen35_9b` vẫn cùng cấu hình. Nhưng P@1 tuyệt đối của `qwen35_9b` trên APPS bị kéo xuống, và mức ảnh hưởng không giống nhau giữa các phương pháp: chỉ MCTS có bước expansion, nên chỉ MCTS mất trắng bài khi expansion bị cắt (17 bài). Đây là quan sát, chưa phải kết luận. Quyết định D-010 (14/11/2026): giữ nguyên protocol và kết quả, ghi vấn đề này vào threats to validity, không chạy lại.

## 7. Ablation thành phần (qwen25c7b, APPS)

Mỗi biến thể chỉ đổi một yếu tố so với RethinkMCTS đầy đủ, và so trên cùng tập bài.

| Biến thể | Thay đổi | n | Overall P@1 % | Δ so với đầy đủ | a-only / b-only | p exact | Token/bài | Nguồn |
|---|---|---|---|---|---|---|---|---|
| Đầy đủ | — | — | — | — | — | — | — | — |
| Tắt rethink | `search.max_rethinks_per_node=0` | — | — | — | — | — | — | — |
| Chỉ thông tin thực thi | `feedback.mode=facts_only` | — | — | — | — | — | — | — |

## 8. Critic: Dual so với Test-only (chọn lại offline từ E1)

Cùng một cây search, chỉ đổi cách chọn chương trình cuối: max reward dual, hoặc chỉ dùng public pass rate (hòa thì lấy ứng viên sinh trước). Không cần chạy GPU thêm. Phép tính lại là **chính xác** (trừ nhiễu vLLM): critic chỉ được gọi khi một ứng viên đã pass hết public, nên cây giống hệt cho tới ứng viên pass đầu tiên, và mọi ứng viên pass sau đó đều hòa ở reward 1,0. P@1 ở bảng này là verdict hidden **chấm lại trên máy local** (khớp verdict trên VM ở 298–300/300 bài APPS và 164/164 bài HE), nên có thể lệch 1–2 bài so với mục 2–3.

| Model | Dataset | Bài có ≥ 2 code khác nhau pass public | Dual P@1 % | Test-only P@1 % | Dual-only / Test-only-only | p exact | Nguồn |
|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | 110 | 29,0 | 27,3 | 5 / 0 | 0,062 | [analysis](v3/analysis_v3_3models.json) |
| qwen25c7b | HE | 153 | 90,9 | 92,7 | 1 / 4 | 0,38 | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | APPS | 113 | 30,0 | 30,0 | 2 / 2 | 1 | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | HE | 155 | 90,2 | 91,5 | 0 / 2 | 0,5 | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | APPS | 212 | 64,7 | 65,0 | 1 / 2 | 1 | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | HE | 162 | 94,5 | 93,9 | 3 / 2 | 1 | [analysis](v3/analysis_v3_3models.json) |

Theo mức khó (APPS, số bài pass /100 mỗi mức, **Dual / Test-only**, chấm lại local):

| Model | Introductory | Interview | Competition | Tổng /300 | Nguồn |
|---|---|---|---|---|---|
| qwen25c7b | 49 / 47 | 26 / 24 | 12 / 11 | 87 / 82 | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | 46 / 46 | 29 / 29 | 15 / 15 | 90 / 90 | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | 81 / 82 | 70 / 70 | 43 / 43 | 194 / 195 | [analysis](v3/analysis_v3_3models.json) |

Số bài hai cách chọn **cùng một chương trình**, và pass rate hidden trung bình (%). Pass rate của Dual là verdict trên VM (mục 2–3). Pass rate của Test-only lấy verdict trên VM khi hai cách chọn cùng chương trình, và chấm lại local cho chương trình khác.

| Model | Dataset | Chọn cùng chương trình | Pass rate Dual | Pass rate Test-only | Nguồn |
|---|---|---|---|---|---|
| qwen25c7b | APPS | 275 / 300 | 48,4 | 46,7 | [analysis](v3/analysis_v3_3models.json) |
| qwen25c7b | HE | 142 / 164 | 90,9 | 92,7 | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | APPS | 267 / 300 | 48,8 | 48,7 | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | HE | 108 / 164 | 90,2 | 91,5 | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | APPS | 265 / 300 (gồm 17 bài không có candidate) | 73,5 | 73,5 | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | HE | 148 / 164 | 94,5 | 93,9 | [analysis](v3/analysis_v3_3models.json) |

**Dual có thể chọn chương trình chưa pass hết public.** Với Dual, chương trình pass hết public có reward 0,8 + 0,2·v_llm, thấp nhất là 0,6 khi critic chấm −1, còn chương trình chưa pass hết public có reward bằng tỷ lệ pass public. Vì vậy một chương trình sai vài public test có thể thắng một chương trình pass hết. Chuyện này xảy ra ở 2 bài trên cả 6 ô: `apps_3736` của qwen25c7b (reward 0,967 so với 0,960) và `apps_4029` của qwen35_9b (0,692 so với 0,600).

## 9. Dừng sớm tính lại offline (từ E1)

Phương án "dừng ở chương trình đầu tiên pass hết public" được tính lại từ log request của run đầy đủ: bỏ mọi lời gọi sau lời gọi sinh ra chương trình đó (kể cả lời gọi critic cho chính nó). Bài không có chương trình nào pass hết public thì chạy đủ như cũ. Chương trình được chọn khi dừng sớm trùng với chương trình được chọn khi bỏ critic (mục 8), nên P@1 giống cột Test-only. Mỗi lời gọi sinh code ứng với đúng một chương trình theo thứ tự sinh; điều này đã được kiểm tra trên cả 6 run MCTS. Token là input / output trung bình mỗi bài.

| Model | Dataset | P@1 đầy đủ % | P@1 dừng sớm % | Bài dừng sớm | Token đầy đủ | Token dừng sớm | Lời gọi/bài | **Token tiết kiệm %** | Nguồn |
|---|---|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | 29,0 | 27,3 | 125 | 161.378 / 18.316 | 128.255 / 14.177 | 70,5 → 50,2 | **20,7** | [analysis](v3/analysis_v3_3models.json) |
| qwen25c7b | HE | 90,9 | 92,7 | 159 | 26.130 / 4.581 | 6.145 / 1.010 | 47,1 → 6,1 | **76,7** | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | APPS | 30,0 | 30,0 | 120 | 150.860 / 20.955 | 120.156 / 16.423 | 69,4 → 50,2 | **20,5** | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | HE | 90,2 | 91,5 | 162 | 24.274 / 3.818 | 3.416 / 593 | 43,7 → 4,1 | **85,7** | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | APPS | 64,7 | 65,0 | 225 | 112.692 / 49.944 | 50.168 / 27.264 | 53,6 → 19,7 | **52,4** | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | HE | 94,5 | 93,9 | 162 | 21.967 / 6.149 | 1.980 / 607 | 41,9 → 2,9 | **90,8** | [analysis](v3/analysis_v3_3models.json) |

P@1 chấm lại local, như mục 8. Trên APPS, phần lớn bài của qwen25c7b và seedcoder8b không có chương trình nào pass hết public (175–180/300 bài), nên với các bài đó dừng sớm không giúp gì và mức tiết kiệm chỉ khoảng 21%.

## 10. Đường cong theo ngân sách (APPS)

Best-of-k tính offline từ 16 mẫu của E3: với mỗi k, lấy **k mẫu đầu tiên theo thứ tự sinh** (không lấy trung bình trên các tập con), chọn theo public pass rate, hòa thì lấy mẫu sinh trước, rồi chấm hidden trên máy local. Ô ghi P@1 % (số bài). Token của Best-of-k bằng k/16 token của Best-of-16 (16 mẫu độc lập, nên đúng theo kỳ vọng).

**RethinkMCTS@k** là run MCTS đầy đủ cắt sau rollout thứ k: chỉ giữ các chương trình sinh trong k rollout đầu (kể cả bản rethink của chúng), chọn như run đầy đủ (reward lớn nhất, hòa thì lấy chương trình sinh trước), chấm hidden trên máy local. Search chạy tuần tự và P-UCB không phụ thuộc tổng ngân sách, nên đây đúng là kết quả của một run k rollout (trừ nhiễu vLLM). Kiểm tra: ở k=16, chương trình được chọn trùng với run thật ở 300/300 bài APPS và 164/164 bài HE của mọi model. Ô ghi P@1 % (số bài) · token TB/bài (input + output). Dòng tham chiếu ghi P@1 chính thức của Direct và RethinkMCTS. Hình: `docs/report/figures/v3/H3_cost_vs_pass.pdf`.

| Model | Dataset | Phương pháp | k=1 | k=2 | k=4 | k=8 | k=16 | Nguồn |
|---|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | Best-of-k | 15,0 (45) | 19,7 (59) | 22,7 (68) | 26,0 (78) | 28,7 (86) | [analysis](v3/analysis_v3_3models.json) |
| qwen25c7b | APPS | Tham chiếu: Direct / MCTS | 17,3 | — | — | — | MCTS 28,7 | [analysis](v3/analysis_v3_3models.json) |
| qwen25c7b | APPS | RethinkMCTS@k | 18,7 (56) · 8,8k | 20,7 (62) · 16,9k | 23,7 (71) · 42,9k | 26,3 (79) · 86,5k | 29,0 (87) · 179,7k | [analysis](v3/analysis_v3_3models.json) |
| qwen25c7b | HE | Best-of-k | 73,2 (120) | 84,1 (138) | 88,4 (145) | 88,4 (145) | 89,0 (146) | [analysis](v3/analysis_v3_3models.json) |
| qwen25c7b | HE | Tham chiếu: Direct / MCTS | 77,4 | — | — | — | MCTS 90,9 | [analysis](v3/analysis_v3_3models.json) |
| qwen25c7b | HE | RethinkMCTS@k | 87,8 (144) · 1,9k | 90,9 (149) · 3,8k | 90,2 (148) · 8,0k | 89,6 (147) · 15,8k | 90,9 (149) · 30,7k | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | APPS | Best-of-k | 14,3 (43) | 23,0 (69) | 28,0 (84) | 32,7 (98) | 35,7 (107) | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | APPS | Tham chiếu: Direct / MCTS | 17,0 | — | — | — | MCTS 30,7 | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | APPS | RethinkMCTS@k | 19,3 (58) · 8,8k | 22,3 (67) · 16,6k | 27,7 (83) · 40,5k | 28,3 (85) · 82,8k | 30,0 (90) · 171,8k | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | HE | Best-of-k | 78,7 (129) | 82,3 (135) | 84,1 (138) | 87,2 (143) | 89,6 (147) | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | HE | Tham chiếu: Direct / MCTS | 78,7 | — | — | — | MCTS 90,2 | [analysis](v3/analysis_v3_3models.json) |
| seedcoder8b | HE | RethinkMCTS@k | 84,8 (139) · 1,9k | 89,0 (146) · 3,6k | 90,2 (148) · 7,5k | 90,2 (148) · 14,5k | 90,2 (148) · 28,1k | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | APPS ⚠️ | Best-of-k | 40,3 (121) | 50,3 (151) | 57,7 (173) | 63,3 (190) | 66,0 (198) | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | APPS | Tham chiếu: Direct / MCTS | 44,3 | — | — | — | MCTS 64,7 | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | APPS | RethinkMCTS@k | 53,0 (159) · 10,0k | 59,0 (177) · 18,2k | 62,0 (186) · 41,8k | 63,3 (190) · 82,9k | 64,7 (194) · 162,6k | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | HE | Best-of-k | 84,1 (138) | 89,0 (146) | 90,9 (149) | 92,1 (151) | 93,3 (153) | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | HE | Tham chiếu: Direct / MCTS | 86,0 | — | — | — | MCTS 94,5 | [analysis](v3/analysis_v3_3models.json) |
| qwen35_9b | HE | RethinkMCTS@k | 91,5 (150) · 1,9k | 94,5 (155) · 3,8k | 94,5 (155) · 7,5k | 94,5 (155) · 14,3k | 94,5 (155) · 28,1k | [analysis](v3/analysis_v3_3models.json) |

Token TB/bài của Best-of-k ở k=1 / k=16: qwen25c7b APPS 0,9k / 14,2k, HE 0,3k / 5,3k; seedcoder8b APPS 1,0k / 15,9k, HE 0,4k / 6,2k; qwen35_9b APPS 2,5k / 40,7k, HE 0,4k / 7,1k. Trên APPS, ở cùng mức token, đường Best-of-k luôn nằm trên đường RethinkMCTS@k (ví dụ qwen25c7b: Best-of-16 28,7% ở 14,2k token, RethinkMCTS@1 18,7% ở 8,8k và @4 23,7% ở 42,9k). Trên HE, RethinkMCTS@2 (3,6k–3,8k token) đạt 149 / 146 / 155 bài, so với Best-of-16 (5,3k–7,1k token) 146 / 147 / 153 bài (qwen25c7b / seedcoder8b / qwen35_9b, chấm local), tức chênh không quá 3 bài với ít token hơn. Đây là quan sát; chênh lệch trên HE chỉ vài bài.

Với `qwen35_9b` APPS, chấm lại local khớp verdict trên Modal ở 295/300 bài (k=16: local 198, Modal 203). Cả 5 bài lệch đều pass trên Modal và TLE ở giới hạn 4 s khi chấm local lúc máy đang chạy 4 bài song song; chấm lại riêng thì 2/5 bài pass. Vậy các ô Best-of-k của ô này có thể thấp hơn thực tế khoảng 1–2 điểm %. Verdict chính thức (mục 2) là verdict trên Modal.

## 12. Nhật ký vận hành đợt chạy 12–13/11/2026 (Colab A100)

Mọi run E1–E4 dùng code đóng băng `d9666c4` (protocol v3.1), cùng cấu hình vLLM (0.31.0, bf16, `--max-model-len 32768`, `--seed 0`), 16 bài song song, `test_workers=4`, `max_test_processes=8`, Python 3.11.17. Log từng phiên: `runs/colab_overnight_logs/` (file `*.log` bị `.gitignore`, chỉ có ở máy local). Các file nặng của mỗi run (`requests.json`, `feedback.json`, `evaluations.json`) được nén trong `runs/v3_raw_archives/<run>.heavy.tar.gz`; một số `evaluations.json` lớn hơn giới hạn 100 MB của GitHub.

1. **Colab thu hồi máy.** Từ khoảng 01:45 đến 10:10 ngày 13/11, gần như mọi runtime đều biến mất sau khoảng 22–25 phút (lỗi 404 từ contents API; CLI không gửi lệnh `unassign` nào), với cả ba model, chạy một mình hay song song. Có vài máy sống lâu (một phiên `seed` từ 06:02 sống 3,75 giờ). Nguyên nhân chưa rõ. Đã loại trừ ssh, việc tải bản lưu và việc chạy song song. Cách xử lý: trên VM đóng gói `runs/` mỗi 5 phút, [guard_dl.sh](../../deploy/colab/guard_dl.sh) tải bản lưu về, rồi chạy tiếp trên VM mới bằng `SEED_RUNS` ([orchestrate_ls.sh](../../deploy/colab/orchestrate_ls.sh)). Resume theo từng bài: bài đã có `completed.json` được giữ nguyên, bài đang chạy dở khi mất máy được giải lại từ đầu. Manifest (cấu hình, dữ liệu, prompt, mã nguồn, runtime) khớp ở mọi lần resume.
2. **Lỗi kiểm tra khi resume (CRLF).** `_load_completed` đọc `selected.py` bằng `read_text()`, hàm này đổi `\r\n` thành `\n` nên mã băm lệch và resume báo "Corrupted resume artifact" dù artifact đúng. Lỗi gặp ở 3 bài Best-of-16 của qwen25c7b (`apps_1684`, `apps_2408`, `apps_3298`). Cách xử lý: chuyển các bài này ra ngoài để chúng được giải lại như một bài lỗi; kết quả lần đầu lưu ở `runs/v3_raw_archives/crlf_resume_victims_q7rest.tar.gz`. Tiêu chí loại chỉ dựa vào ký tự xuống dòng của code, không phụ thuộc verdict, nên không gây thiên lệch. Code đóng băng chưa sửa vì sửa sẽ làm đổi `source_hash` trong manifest; sẽ sửa sau đợt chạy.
3. **Thứ tự chạy.** Với `seedcoder8b` và `qwen35_9b`, thứ tự các run trong hàng đợi được đổi để các run ngắn chạy trước và MCTS APPS chạy sau cùng. Mỗi run có thư mục riêng và cùng code, nên thứ tự không ảnh hưởng kết quả.
4. **qwen35_9b MCTS APPS trên Colab.** Gate v3.1 trên Colab đã qua. Ngày 13/11, mỗi lần khởi động mất khoảng 9 phút (tải model 55 s, vLLM init khoảng 5 phút), máy chỉ sống khoảng 23–29 phút, còn MCTS cần hơn 10 phút mỗi bài, nên run dừng ở 116/300; hai lần thử 19:27–20:24 không thêm được bài nào. Tối 13/11 chạy tiếp từ bản lưu: phiên từ 22:29 mất sau 27 phút (118/300), phiên từ 22:58 sống liên tục tới khi xong (hàng đợi xong 03:29 ngày 14/11, 300/300). Mọi lần resume đều khớp manifest, không có bài nào bị loại vì lỗi CRLF. Sau khi xong, `colab exec` của ô keep-busy trong [watch_ls.sh](../../deploy/colab/watch_ls.sh) bị treo nên script không tự tải kết quả và tắt máy; đã tải và tắt bằng tay lúc khoảng 04:00, và đã sửa script (ô keep-busy chạy nền). Bản lưu Colab còn chứa 59 bài Best-of-16 APPS cũ; bỏ phần đó, vì Best-of-16 APPS chính thức là run trên Modal. Kết quả đầy đủ: `colab_results/qwen35b/results.tar.gz` (chỉ ở local).
6. **qwen35_9b trên Modal.** [modal_v31_runner.py](../../deploy/modal_v31_runner.py) dựng lại môi trường của VM Colab: cùng archive code `d9666c4`, vLLM 0.31.0, Python 3.11.17 cho solver. Runner từ chối mọi GPU không phải A100-SXM4. Plan: [qwen35_modal.plan](../../deploy/colab/v31_campaign/plans/qwen35_modal.plan). Gate chạy lại trên Modal (`runs/v3_gate_modal_*`) và khớp gate Colab ở 12/13 bài. Sau đó chạy Direct APPS, ba run HumanEval và Best-of-16 APPS. Lúc 17:28 Best-of-16 APPS bị hủy ở 255/300 vì `modal run` gắn với máy local đã tắt. Run được tiếp tục bằng `modal deploy` + `Function.spawn()`, resume đúng 255 bài đã xong (manifest khớp). Không chạy tiếp được bản dở của Colab trên Modal, vì `runtime.platform` trong manifest khác nhau.
7. **Output bị cắt ở qwen35_9b APPS:** xem mục 6.1.
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
