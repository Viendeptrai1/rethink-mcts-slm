# Sổ kết quả benchmark

Bảng ghi chép **mọi** thứ của các đợt chạy benchmark: run nào, cấu hình gì, chạy ở đâu, kết quả, chi phí và độ "khỏe" của search. Khung báo cáo: [KHUNG_BAO_CAO_v2.md](../report/KHUNG_BAO_CAO_v2.md). Cấu hình v3: [configs/v3_7b/README.md](../../configs/v3_7b/README.md).

Cập nhật lần cuối: 12/11/2026 (chưa có run v3 nào; phụ lục A và B đã điền từ artifact có sẵn).

## Quy ước

- **Không trộn protocol.** Mỗi mục chỉ chứa run của một protocol: v3 (mục 1–10), pilot v3 (mục 11, không phải kết quả), 14B v1 (phụ lục A), 7B HuyinCP (phụ lục B).
- Mọi con số phải có nguồn là một artifact trong `runs/` hoặc `docs/results/`. Ô chưa có số thì để `—`.
- Trạng thái: `⏳` chưa chạy · `▶` đang chạy · `✅` xong và đã đối chiếu artifact · `⚠️` xong nhưng có vấn đề (ghi chú) · `✗` hủy.
- **Pass@1 (hidden):** tỷ lệ bài mà chương trình được chọn pass toàn bộ hidden test, mẫu số là cả cohort (bài lỗi hoặc không có candidate tính 0). **Pass rate:** trung bình theo bài của tỷ lệ hidden test pass.
- Số liệu v3 lấy bằng `scripts/pilot_report.py` (search, chi phí) và một script phân tích ghép cặp kiểu [analyze_extra_14b.py](../../scripts/analyze_extra_14b.py) (sẽ viết cho v3).
- Tên ngắn của model: `qwen25c7b` = Qwen2.5-Coder-7B-Instruct · `seedcoder8b` = Seed-Coder-8B-Instruct · `qwen35_9b` = Qwen3.5-9B (tắt thinking) · `granite42_8b` = Granite-4.2-8B (dự phòng) · `qwen25c14b` = Qwen2.5-Coder-14B-Instruct.

---

## 1. Sổ đăng ký run v3

Thư mục run đặt theo mẫu `runs/v3_<dataset>_<model>_<method>`. Commit, GPU, phiên bản vLLM và số worker phải điền **trước khi** chạy. Với mỗi model, mọi phương pháp phải chạy trên cùng nền tảng.

| Mã | Run (`runs/…`) | Model | Dataset | Phương pháp | Config | Commit | Nền tảng / GPU | vLLM | Workers | Ngày | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E1 | `v3_apps_qwen25c7b_mcts` | qwen25c7b | APPS-300 | MCTS | `apps_mcts.yaml` | — | — | — | — | — | ⏳ |
| E1 | `v3_apps_seedcoder8b_mcts` | seedcoder8b | APPS-300 | MCTS | `apps_mcts.yaml` | — | — | — | — | — | ⏳ |
| E1 | `v3_apps_qwen35_9b_mcts` | qwen35_9b | APPS-300 | MCTS | `apps_mcts.yaml` | — | — | — | — | — | ⏳ |
| E2 | `v3_apps_qwen25c7b_direct` | qwen25c7b | APPS-300 | Direct | `apps_baseline.yaml` | — | — | — | — | — | ⏳ |
| E2 | `v3_apps_seedcoder8b_direct` | seedcoder8b | APPS-300 | Direct | `apps_baseline.yaml` | — | — | — | — | — | ⏳ |
| E2 | `v3_apps_qwen35_9b_direct` | qwen35_9b | APPS-300 | Direct | `apps_baseline.yaml` | — | — | — | — | — | ⏳ |
| E3 | `v3_apps_qwen25c7b_bon16` | qwen25c7b | APPS-300 | Best-of-16 | `apps_baseline.yaml` | — | — | — | — | — | ⏳ |
| E3 | `v3_apps_seedcoder8b_bon16` | seedcoder8b | APPS-300 | Best-of-16 | `apps_baseline.yaml` | — | — | — | — | — | ⏳ |
| E3 | `v3_apps_qwen35_9b_bon16` | qwen35_9b | APPS-300 | Best-of-16 | `apps_baseline.yaml` | — | — | — | — | — | ⏳ |
| E4 | `v3_humaneval_qwen25c7b_mcts` | qwen25c7b | HE-164 | MCTS | `humaneval_mcts.yaml` | — | — | — | — | — | ⏳ |
| E4 | `v3_humaneval_seedcoder8b_mcts` | seedcoder8b | HE-164 | MCTS | `humaneval_mcts.yaml` | — | — | — | — | — | ⏳ |
| E4 | `v3_humaneval_qwen35_9b_mcts` | qwen35_9b | HE-164 | MCTS | `humaneval_mcts.yaml` | — | — | — | — | — | ⏳ |
| E2 | `v3_humaneval_{qwen25c7b,seedcoder8b,qwen35_9b}_direct` | 3 model | HE-164 | Direct | `humaneval_baseline.yaml` | — | — | — | — | — | ⏳ |
| E3 | `v3_humaneval_{qwen25c7b,seedcoder8b,qwen35_9b}_bon16` | 3 model | HE-164 | Best-of-16 | `humaneval_baseline.yaml` | — | — | — | — | — | ⏳ |
| E5 | `v3_apps_qwen25c7b_norethink` | qwen25c7b | APPS (300 hoặc 150) | MCTS, `max_rethinks_per_node=0` | `apps_mcts.yaml` | — | — | — | — | — | ⏳ (nếu còn tiền) |
| E6 | `v3_apps_qwen25c7b_factsonly` | qwen25c7b | APPS (300 hoặc 150) | MCTS, `feedback.mode=facts_only` | `apps_mcts.yaml` | — | — | — | — | — | ⏳ (nếu còn tiền) |
| E7 | `v3_apps_qwen25c14b_mcts` | qwen25c14b | APPS-300 | MCTS | `apps_mcts.yaml` | — | — | — | — | — | ⏳ (nếu còn tiền) |

Best-of-16 chạy với `--set sampling.code.temperature=0.8 --set sampling.code.top_p=0.95`. Nếu đổi giá trị này, ghi vào cột Config.

## 2. APPS-300, Pass@1 trên hidden test (v3)

| Model | Phương pháp | Hoàn tất / 300 | Intro P@1 % | Inter P@1 % | Comp P@1 % | **Overall P@1 %** | Overall pass rate % | Lỗi kỹ thuật (ID) | Chạm 3600 s | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen25c7b | Direct | — | — | — | — | — | — | — | — | — |
| qwen25c7b | Best-of-16 | — | — | — | — | — | — | — | — | — |
| qwen25c7b | RethinkMCTS | — | — | — | — | — | — | — | — | — |
| seedcoder8b | Direct | — | — | — | — | — | — | — | — | — |
| seedcoder8b | Best-of-16 | — | — | — | — | — | — | — | — | — |
| seedcoder8b | RethinkMCTS | — | — | — | — | — | — | — | — | — |
| qwen35_9b | Direct | — | — | — | — | — | — | — | — | — |
| qwen35_9b | Best-of-16 | — | — | — | — | — | — | — | — | — |
| qwen35_9b | RethinkMCTS | — | — | — | — | — | — | — | — | — |

## 3. HumanEval-164, Pass@1 (v3)

| Model | Phương pháp | Hoàn tất / 164 | **Pass@1 %** | Số bài pass | Lỗi kỹ thuật | Nguồn |
|---|---|---|---|---|---|---|
| qwen25c7b | Direct | — | — | — | — | — |
| qwen25c7b | Best-of-16 | — | — | — | — | — |
| qwen25c7b | RethinkMCTS | — | — | — | — | — |
| seedcoder8b | Direct | — | — | — | — | — |
| seedcoder8b | Best-of-16 | — | — | — | — | — |
| seedcoder8b | RethinkMCTS | — | — | — | — | — |
| qwen35_9b | Direct | — | — | — | — | — |
| qwen35_9b | Best-of-16 | — | — | — | — | — |
| qwen35_9b | RethinkMCTS | — | — | — | — | — |

## 4. Kiểm định ghép cặp (v3)

`a-only` là số bài chỉ phương pháp A pass; `b-only` là số bài chỉ B pass. Dùng McNemar exact. `p (Holm)` hiệu chỉnh trên toàn bộ các so sánh của bảng này. CI là bootstrap 95% (10.000 lần, seed 2027) của chênh lệch Pass@1.

| Dataset | Model | A vs B | n chung | a-only | b-only | p exact | p (Holm) | Δ P@1 (điểm %) | 95% CI | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|
| APPS | qwen25c7b | MCTS vs Direct | — | — | — | — | — | — | — | — |
| APPS | qwen25c7b | MCTS vs Best-of-16 | — | — | — | — | — | — | — | — |
| APPS | qwen25c7b | Best-of-16 vs Direct | — | — | — | — | — | — | — | — |
| APPS | seedcoder8b | MCTS vs Direct | — | — | — | — | — | — | — | — |
| APPS | seedcoder8b | MCTS vs Best-of-16 | — | — | — | — | — | — | — | — |
| APPS | seedcoder8b | Best-of-16 vs Direct | — | — | — | — | — | — | — | — |
| APPS | qwen35_9b | MCTS vs Direct | — | — | — | — | — | — | — | — |
| APPS | qwen35_9b | MCTS vs Best-of-16 | — | — | — | — | — | — | — | — |
| APPS | qwen35_9b | Best-of-16 vs Direct | — | — | — | — | — | — | — | — |
| HE | 3 model | (như trên, mỗi model 3 dòng) | — | — | — | — | — | — | — | — |

## 5. Chi phí (v3)

Token lấy từ `usage.json` (vLLM báo, không ước lượng). GPU-giây lấy từ `modal billing report --show-resources` (hoặc thời gian phiên Colab) cho đúng khoảng thời gian của run. Giá: Modal L40S $1,95/giờ; Colab tính theo compute unit (ghi rõ tỷ giá đã dùng).

| Model | Dataset | Phương pháp | Input token/bài | Output token/bài | Lời gọi/bài | Wall TB (s) | Wall max (s) | GPU-giây | Chi phí $ | $/bài | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | Direct | — | — | — | — | — | — | — | — | — |
| qwen25c7b | APPS | Best-of-16 | — | — | — | — | — | — | — | — | — |
| qwen25c7b | APPS | RethinkMCTS | — | — | — | — | — | — | — | — | — |
| seedcoder8b | APPS | (3 phương pháp) | — | — | — | — | — | — | — | — | — |
| qwen35_9b | APPS | (3 phương pháp) | — | — | — | — | — | — | — | — | — |
| 3 model | HE | (3 phương pháp) | — | — | — | — | — | — | — | — | — |

### 5.1. Token theo vai trò (RethinkMCTS, tổng trên cả run, input / output)

| Model | Dataset | expansion | code | rethink | critic | block_analysis | Tổng | Nguồn |
|---|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | — | — | — | — | — | — | — |
| seedcoder8b | APPS | — | — | — | — | — | — | — |
| qwen35_9b | APPS | — | — | — | — | — | — | — |

## 6. Độ "khỏe" của search (RethinkMCTS, v3)

Lấy từ `scripts/pilot_report.py`. Đây là bằng chứng các cơ chế thật sự chạy. Ví dụ ở v1, cột "analysis vào feedback" là 0%.

| Model | Dataset | Rollout TB | Phân bố độ sâu tối đa | Node được đánh giá TB | Rethink TB | Analysis vào feedback % | Output bị cắt (length) % | `<think>` lọt ra | Bài chạm 3600 s | Lý do dừng | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | — | — | — | — | — | — | — | — | — | — |
| seedcoder8b | APPS | — | — | — | — | — | — | — | — | — | — |
| qwen35_9b | APPS | — | — | — | — | — | — | — | — | — | — |
| 3 model | HE | — | — | — | — | — | — | — | — | — | — |

## 7. Ablation thành phần (qwen25c7b, APPS)

Mỗi biến thể chỉ đổi một yếu tố so với RethinkMCTS đầy đủ, và so trên cùng tập bài.

| Biến thể | Thay đổi | n | Overall P@1 % | Δ so với đầy đủ | a-only / b-only | p exact | Token/bài | Nguồn |
|---|---|---|---|---|---|---|---|---|
| Đầy đủ | — | — | — | — | — | — | — | — |
| Tắt rethink | `search.max_rethinks_per_node=0` | — | — | — | — | — | — | — |
| Chỉ thông tin thực thi | `feedback.mode=facts_only` | — | — | — | — | — | — | — |

## 8. Critic: Dual so với Test-only (chọn lại offline từ E1)

Cùng một cây search, chỉ đổi cách chọn chương trình cuối: max reward dual, hoặc chỉ dùng public pass rate (hòa thì lấy ứng viên sinh trước). Không cần chạy GPU thêm.

| Model | Dataset | Bài có ≥ 2 ứng viên pass public | Dual P@1 % | Test-only P@1 % | Dual-only / Test-only-only | p exact | Nguồn |
|---|---|---|---|---|---|---|---|
| qwen25c7b | APPS | — | — | — | — | — | — |
| seedcoder8b | APPS | — | — | — | — | — | — |
| qwen35_9b | APPS | — | — | — | — | — | — |

## 9. Dừng sớm tính lại offline (từ E1)

Phương án "dừng ở ứng viên đầu tiên pass hết public" được tính lại từ thứ tự sinh ứng viên trong run đầy đủ.

| Model | Dataset | P@1 đầy đủ % | P@1 nếu dừng sớm % | Bài có kết quả khác | Token tiết kiệm % | Nguồn |
|---|---|---|---|---|---|---|
| qwen25c7b | APPS | — | — | — | — | — |
| seedcoder8b | APPS | — | — | — | — | — |
| qwen35_9b | APPS | — | — | — | — | — |

## 10. Đường cong theo ngân sách (APPS)

Best-of-k tính offline từ 16 mẫu của E3. Với mỗi k, lấy trung bình trên các tập con k mẫu, chọn theo public pass rate. MCTS@k là ứng viên tốt nhất sau k lần sinh code đầu tiên của E1.

| Model | Phương pháp | k=1 | k=2 | k=4 | k=8 | k=16 | Nguồn |
|---|---|---|---|---|---|---|---|
| qwen25c7b | Best-of-k | — | — | — | — | — | — |
| qwen25c7b | MCTS@k | — | — | — | — | — | — |
| seedcoder8b | Best-of-k / MCTS@k | — | — | — | — | — | — |
| qwen35_9b | Best-of-k / MCTS@k | — | — | — | — | — | — |

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

## Phụ lục A. 14B v1 (Qwen2.5-Coder-14B, có lỗi đã biết, không dùng cho kết luận)

Lỗi đã biết của v1:
- Kết quả block analysis không vào feedback (0/1.203 lần ở MCTS).
- Rethink không thấy thought cần sửa.
- Dừng khi pass public.
- Ngân sách tính cả rethink, cây sâu tối đa 2.
- Public là 2 test đầu.

Chi tiết: [prompts/README.md](../../prompts/README.md), [configs/README.md](../../configs/README.md). Mọi số ở đây lấy từ [runs/analysis_extra_14b/summary.json](../../runs/analysis_extra_14b/summary.json) (số từng bài: [per_problem.json](../../runs/analysis_extra_14b/per_problem.json)).

### A.1. Run và cấu hình

| Phương pháp | Run (`runs/…`) | Prompt | Ngân sách chính | GPU |
|---|---|---|---|---|
| Direct | `benchmark_apps_14b_direct_300` | native_v2 | 1 lần sinh code (+ critic) | L40S |
| Best-of-3 | `benchmark_apps_14b_bon3_300` (160 bài) + `benchmark_apps_14b_bon3_rest140` | native_v2 | 3 lần sinh code | L40S |
| RethinkMCTS | `benchmark_apps_14b_dual_unified` | native_v2 | 16 lần sinh code (gồm rethink), 64 lời gọi, 65.536 token, 2 rethink/node, dừng khi pass public, 900 s | H200 |
| MCTS tắt rethink | `benchmark_apps_14b_norethink_q1..q4` | native_v2 | như MCTS, `max_rethinks_per_node=0`, 3600 s | L40S |
| Iterative Repair | `benchmark_apps_14b_repair_q1..q4` | native_v2 | như MCTS, 3600 s | L40S |
| HE Direct / BO3 | `humaneval_direct_14b_v2`, `humaneval_bon3_14b_v2` | native_v2 | 1 / 3 lần sinh code | L40S |
| HE RethinkMCTS | `humaneval_mcts_dual_14b` | native_v2 | như MCTS, 600 s | L40S |

Nguồn của cột GPU là billing Modal (ghi nhận 11/2026), không phải artifact trong `runs/`.

### A.2. APPS-300, Pass@1 trên hidden test (%)

Mỗi ô ghi "P@1 hidden / P@1 khi chấm trên toàn bộ test (public + hidden)".

| Phương pháp | Intro | Inter | Comp | **Overall** | Overall pass rate (hidden) | Token TB/bài | Lời gọi TB/bài |
|---|---|---|---|---|---|---|---|
| Direct | 42,0 / 38,0 | 13,0 / 11,0 | 21,0 / 8,0 | **25,33 / 19,00** | 38,41 | 1.373 | 1,27 |
| Best-of-3 | 50,0 / 42,0 | 17,0 / 14,0 | 25,0 / 13,0 | **30,67 / 23,00** | 44,06 | 4.065 | 3,83 |
| RethinkMCTS | 53,0 / 50,0 | 27,0 / 26,0 | 28,0 / 23,0 | **36,00 / 33,00** | 53,49 | 37.379 | 15,29 |
| MCTS tắt rethink | 55,0 / 51,0 | 32,0 / 29,0 | 25,0 / 17,0 | **37,33 / 32,33** | 52,93 | 26.212 | 12,33 |
| Iterative Repair | 56,0 / 49,0 | 24,0 / 21,0 | 25,0 / 16,0 | **35,00 / 28,67** | 49,56 | 42.452 | 11,79 |

Cả 5 phương pháp đều có 300/300 bài hoàn tất. Có 8 bài MCTS tắt rethink chạy quá 900 s (giới hạn của run này là 3600 s). Lời gọi của Direct và BO3 gồm cả critic, vì các run này dùng config dual.

### A.3. APPS-300, kiểm định ghép cặp (hidden; n = 300)

| A vs B | a-only | b-only | p exact | Δ P@1 (điểm %) | 95% CI |
|---|---|---|---|---|---|
| MCTS vs Direct | 42 | 10 | 9,06e-6 | +10,67 | [6,33; 15,33] |
| MCTS vs Best-of-3 | 26 | 10 | 0,0113 | +5,33 | [1,67; 9,33] |
| MCTS vs MCTS tắt rethink | 13 | 17 | 0,585 | −1,33 | [−5,00; 2,33] |
| MCTS vs Iterative Repair | 21 | 18 | 0,749 | +1,00 | [−3,00; 5,33] |
| Iterative Repair vs Direct | 36 | 7 | 8,96e-6 | +9,67 | [5,67; 14,00] |
| MCTS tắt rethink vs Direct | 51 | 15 | 1,01e-5 | +12,00 | [7,00; 17,33] |
| Best-of-3 vs Direct | 20 | 4 | 0,00154 | +5,33 | [2,33; 8,67] |

### A.4. HumanEval-164

| Phương pháp | Pass@1 % | Số bài pass | Token TB/bài | Lời gọi TB/bài |
|---|---|---|---|---|
| Direct | 85,37 | 140 | 633 | 1,90 |
| Best-of-3 | 86,59 | 142 | 1.913 | 5,73 |
| RethinkMCTS | 90,85 | 149 | 3.218 | 4,64 |

| A vs B | a-only | b-only | p exact | Δ (điểm %) | 95% CI |
|---|---|---|---|---|---|
| MCTS vs Direct | 12 | 3 | 0,0352 | +5,49 | [1,22; 10,37] |
| MCTS vs Best-of-3 | 10 | 3 | 0,0923 | +4,27 | [0,00; 8,54] |
| Best-of-3 vs Direct | 2 | 0 | 0,5 | +1,22 | [0,00; 3,05] |

### A.5. Search của RethinkMCTS v1 (APPS-300)

Nguồn: `python3 scripts/pilot_report.py runs/benchmark_apps_14b_dual_unified` (12/11/2026).

| Chỉ số | Giá trị |
|---|---|
| Phân bố độ sâu tối đa | 1: 241 bài, 2: 59 bài |
| Node được đánh giá TB | 2,27 (không tính node gốc) |
| Lần sinh code TB / rethink TB | 5,83 / 3,45 |
| Block analysis vào feedback | 0 / 1.203 (0%) |
| Output bị cắt (length) | 194 / 4.587 lời gọi |
| Lý do dừng | Dừng sớm vì pass public 161; hết ngân sách (sinh code, lời gọi, token hoặc thời gian) 139 |
| Input / output token TB/bài | 33.554 / 4.203 |
| Token theo vai trò (input) | block_analysis 5,72 triệu; rethink 2,56 triệu; code 1,26 triệu; expansion 0,40 triệu; critic 0,12 triệu |

---

## Phụ lục B. 7B nhánh HuyinCP (tham khảo, protocol khác)

Protocol khác:
- 2 rollout, width 3, tối đa 2 rethink.
- Public là một nửa số test; **chấm trên toàn bộ test**, gồm cả public, với timeout 5 giây.
- Temperature 0,2.
- Code trong `external/ReThinkMCTS`, model `qwen2.5-coder:7b-instruct`, Modal L40S.

Không so trực tiếp với v3 hay 14B v1.

| Phương pháp | Intro pass rate / P@1 | Inter pass rate / P@1 | Comp pass rate / P@1 | **Overall pass rate / P@1** | HumanEval P@1 | Nguồn |
|---|---|---|---|---|---|---|
| Direct | 45,84 / 31,00 | 26,18 / 7,00 | 19,52 / 4,00 | **30,51 / 14,00** | 80,49 | [retry](7b/rethinkmcts-apps-native-v2-w4-retry.md) |
| RethinkMCTS dual (native_v2, 295/300 có candidate) | 56,70 / 38,00 | 42,36 / 14,00 | 30,07 / 5,00 | **43,04 / 19,00** | 91,46 (run `native_v1`) | [retry](7b/rethinkmcts-apps-native-v2-w4-retry.md) |
| RethinkMCTS test-only (297/300) | 61,14 / 41,00 | 45,46 / 18,00 | 29,42 / 9,00 | **45,34 / 22,67** | 89,63 | [test-only](7b/rethinkmcts-test-only-v1.md) |
| RethinkMCTS dual (native_v1, đã bị thay thế) | 31,40 / 20,00 | 17,69 / 6,00 | 10,80 / 3,00 | **19,96 / 9,67** | 91,46 | [v2-all-tests](7b/benchmark-v2-all-tests.md); prompt thiếu hướng dẫn stdin/stdout, 106/295 bài in ra rỗng |

Bài thiếu candidate được tính 0. Hàng dual native_v2 và test-only không được kiểm định ghép cặp với nhau.
