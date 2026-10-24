# APPS native_v2: đánh giá bổ sung sau retry

Kiểm tra ngày 2026-10-05. Báo cáo này cập nhật [snapshot 286/300](rethinkmcts-apps-native-v2-w4-provisional.md) sau khi chạy lại 14 bài thiếu candidate. Không sửa code đã sinh và không gọi LLM trong bước rejudge.

## Protocol

- Cohort: `data/samples/benchmark_v2/apps_test_300.json`, 100 ID mỗi mức độ khó.
- Search run: `rethinkmcts_apps_interface_v2_half_w4`; model `qwen2.5-coder:7b-instruct`, digest `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`, Modal L40S, 4 worker, 2 rollouts, width 3, public policy `half`, giới hạn 900 giây/problem.
- Rejudge run: `rethinkmcts_apps_interface_v2_half_w4_all_tests`; 5 giây/test, 2 CPU worker, chấm **toàn bộ** test trong `input_output.json`.
- Artifact đánh giá: `outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_apps_interface_v2_half_w4_all_tests/qwen2.5-coder_7b-instruct/apps/`.
- Baseline đối chiếu: `outputs/baselines/evaluations/qwen25_coder_7b_instruct_baseline_benchmark_v2_all_tests/qwen2.5-coder_7b-instruct/`.

## Độ phủ và lỗi còn lại

Lượt retry bổ sung 9 candidate: `0164`, `3249`, `3298`, `3715`, `3780`, `3828`, `3906`, `3964`, `4078`. Rejudge đã skip 286 report cũ và chấm 9 bài này. Không bài nào trong 9 pass toàn bộ test; `3780` trước đó search timeout nhưng nay có candidate, final judge 0/51 (runtime error).

Hiện có **295/300** APPS report, 295 ID duy nhất. Mọi `total_tests` đều khớp số input gốc; không có `executor_error`. Phân loại final judge: 57 `passed`, 191 `wrong_answer`, 27 `runtime_error`, 20 `timeout`.

Năm bài chưa có candidate:

| ID | Search status sau retry | Xử lý trong bảng |
|---|---|---|
| `1033` | timeout 900 giây | 0; chưa có code để chấm |
| `1634` | timeout 900 giây | 0; chưa có code để chấm |
| `3698` | timeout 900 giây | 0; chưa có code để chấm |
| `1684` | failed: `SyntaxError` khi trace code LLM | 0 tạm thời; lỗi kỹ thuật |
| `3702` | failed: `IndentationError` khi trace code LLM | 0 tạm thời; lỗi kỹ thuật |

Ba timeout được tính không pass theo quyết định trước đó. Hai lỗi kỹ thuật được đưa vào mẫu số 300 với đóng góp 0 để bảng không tự loại bài khó, **không phải kết luận rằng lời giải sai**. Không gán số lượng test hoặc kết quả test giả cho 5 bài thiếu candidate.

## Bảng so sánh

APPS Pass Rate là macro mean của `passed_tests/total_tests` theo problem; ID thiếu candidate đóng góp 0. Pass@1 là số bài pass toàn bộ test chia cho 100 hoặc 300 ID. HumanEval chỉ báo Pass@1.

| Phương pháp | Intro. Pass Rate | Intro. Pass@1 | Inter. Pass Rate | Inter. Pass@1 | Comp. Pass Rate | Comp. Pass@1 | Overall Pass Rate | Overall Pass@1 | HumanEval Pass@1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Direct baseline | 45.84 | 31.00 | 26.18 | 7.00 | 19.52 | 4.00 | 30.51 | 14.00 | 80.49 |
| RethinkMCTS APPS native_v2 (tạm thời) + HumanEval run cũ | 56.70 | 38.00 | 42.36 | 14.00 | 30.07 | 5.00 | 43.04 | 19.00 | 91.46 |

Độ phủ candidate APPS: Intro. 100/100, Inter. 97/100, Comp. 98/100. APPS có 57/300 bài pass toàn bộ test, so với baseline 42/300. Pass Rate tăng 0,80 điểm sau retry; Pass@1 không đổi. HumanEval MCTS vẫn là 150/164 từ run `native_v1` cũ, chưa chạy lại bằng source `native_v2`; không diễn giải hàng MCTS như một run đồng nhất phiên bản trên cả hai dataset.
