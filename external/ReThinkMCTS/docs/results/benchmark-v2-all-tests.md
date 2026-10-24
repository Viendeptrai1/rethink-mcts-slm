# Benchmark v2 - final evaluation trên toàn bộ test

Trạng thái: **kết quả đã kiểm chứng của hai run lịch sử**, kiểm tra ngày
2026-10-04. MCTS APPS run này dùng prompt `native_v1`, trước khi sửa thông
tin giao diện stdin/stdout và feedback stdout rỗng. Các con số không phải
đánh giá của `native_v2` hoặc `half_min2`.

## Protocol

- Cohort: 300 APPS (100 bài mỗi difficulty) và toàn bộ 164 HumanEval.
- Trong MCTS search, nửa đầu APPS tests là public tests để  tính reward và tạo
  feedback. Chúng không bị loại khỏi final evaluation.
- Final evaluation chạy **toàn bộ** `input_output.json` của APPS cho cả direct
  baseline và final solution MCTS, timeout 5 giây/test.
- HumanEval chạy toàn bộ official harness. `given_tests` chỉ phục vụ MCTS search.
- Ba APPS ID `0796`, `1033`, `1581` không có final MCTS candidate và được tính
  0 trong mẫu số 300 theo adjudication đã chốt.

## Kết quả

| Phương pháp | APPS Intro. Pass Rate | APPS Intro. Pass@1 | APPS Inter. Pass Rate | APPS Inter. Pass@1 | APPS Comp. Pass Rate | APPS Comp. Pass@1 | APPS Overall Pass Rate | APPS Overall Pass@1 | HumanEval Pass@1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Direct Evaluation | 45.84 | 31.00 | 26.18 | 7.00 | 19.52 | 4.00 | 30.51 | 14.00 | 80.49 |
| RethinkMCTS (adjudicated) | 31.40 | 20.00 | 17.69 | 6.00 | 10.80 | 3.00 | 19.96 | 9.67 | 91.46 |

Direct baseline có 42/300 APPS pass toàn bộ test và 132/164 HumanEval pass
official harness. RethinkMCTS có 29/300 APPS pass toàn bộ test (29/297 final
candidate thật, ba technical failure tính 0) và 150/164 HumanEval pass.

Audit best candidate của run APPS cũ: 106/295 bài stdin/stdout cho output
rỗng ở mọi public test; 181/297 bài có best reward bằng 0. Upstream APPS
loader ghi rõ `Use Standard Input format` trong prompt, còn prompt native v1
thiếu thông tin này. Xem `docs/implementation-audit.md` về native v2; bảng
này chưa được chạy lại sau sửa đổi.
Một pilot riêng cho APPS `0395` với prompt v2 đạt 53/53; kết quả đó không
được cộng vào bảng cohort lịch sử. Xem
`docs/results/rethinkmcts-apps-0395-native-v2-smoke.md`.

## Kiểm tra tính toàn vẹn

- Direct baseline: 300 APPS report, không thiếu ID, không `executor_error`.
- RethinkMCTS: 297 APPS report thật và ba ID adjudicated; không
  `executor_error` trong 297 report.
- Với mọi APPS report đã chạy, `total_tests == available_tests`; evaluator
  không dùng `max_tests` hay `private_half`.
- HumanEval có 164 report ở mỗi phương pháp.

## Artifact

- Baseline: `outputs/baselines/evaluations/qwen25_coder_7b_instruct_baseline_benchmark_v2_all_tests/qwen2.5-coder_7b-instruct/`.
- MCTS: `outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_qwen25_modal_benchmark_v2_all_tests/qwen2.5-coder_7b-instruct/`.

Hai bảng private-half trước đây được giữ để audit nhưng đã bị thay thế cho mục
đích báo cáo benchmark cuối. Chúng chỉ đo phần test không dùng trong search.
