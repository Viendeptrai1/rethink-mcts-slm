# APPS native_v2, 4 worker: ket qua tam thoi

**Snapshot trước retry (286/300).** Kết quả mới nhất ở
[báo cáo sau retry](rethinkmcts-apps-native-v2-w4-retry.md); các số dưới đây
được giữ nguyên để truy vết và không còn là bảng hiện hành.

Kiem tra ngay 2026-10-05. Day la ket qua rejudge cac candidate da hoan tat,
khong goi lai LLM, khong sua `final_solution.py` va khong tuy tien gan pass
cho search bi timeout.

## Nguon va protocol

- Cohort: `data/samples/benchmark_v2/apps_test_300.json`, 300 APPS ID,
  100 ID cho moi difficulty.
- Search: `rethinkmcts_apps_interface_v2_half_w4`, model
  `qwen2.5-coder:7b-instruct`, digest
  `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`,
  Modal L40S, 4 problem worker, public policy `half`, 2 rollouts,
  width 3, 900 giay/problem.
- Rejudge: `rethinkmcts_apps_interface_v2_half_w4_all_tests`,
  `evaluation.rejudge_mcts`, `--timeout 5 --workers 2`.
  Chay toan bo `input_output.json` cho moi candidate, khong chi private half.
- APPS report: `outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_apps_interface_v2_half_w4_all_tests/qwen2.5-coder_7b-instruct/apps/`.
- Paired direct baseline: `outputs/baselines/evaluations/qwen25_coder_7b_instruct_baseline_benchmark_v2_all_tests/qwen2.5-coder_7b-instruct/`.
- HumanEval MCTS 91,46% la 150/164 tu run cu
  `rethinkmcts_qwen25_modal_v1`, khong phai native_v2. Baseline la
  132/164 = 80,49%.

## Kiem tra do phu

- 286/300 APPS candidate co `final_solution.py` va `search_summary.json`.
- Rejudge co 286 report, 286 ID duy nhat; moi `total_tests` khop so input
  goc; khong co `executor_error`.
- Trong 286 report: 57 `passed`, 186 `wrong_answer`, 25 `runtime_error`,
  18 `timeout` o final test. 57/300 = 19,00% Pass@1.
- Nam search timeout 900 giay khong co candidate:
  `1033`, `1634`, `3698`, `3702`, `3780`. Theo quyet dinh cua nguoi dung,
  tinh la khong pass; khong gia tao ket qua test cho chung.
- Chin search loi ky thuat khac khong co candidate:
  `0164`, `1684`, `3249`, `3298`, `3715`, `3828`, `3906`, `3964`, `4078`.
  Chung gop 0 vao mau so 300 trong bang tam thoi, nhung khong duoc goi la
  wrong answer. Nguyen nhan gom syntax error trong AST trace, JSON/duplicate
  thought, loi ket noi Modal va Windows page-file.

## Bang ket qua

Pass Rate APPS = mean(per-problem passed_tests/total_tests) tren 100 ID/muc
do kho, hoac 300 ID/overall; ID khong co candidate dong gop 0.
Pass@1 = so bai pass tat ca tests / so ID cua nhom. Khong gan `total_tests`
gia cho 14 ID thieu candidate.

| Phuong phap | APPS Intro. Pass Rate | APPS Intro. Pass@1 | APPS Inter. Pass Rate | APPS Inter. Pass@1 | APPS Comp. Pass Rate | APPS Comp. Pass@1 | APPS Overall Pass Rate | APPS Overall Pass@1 | HumanEval Pass@1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Direct baseline | 45.84 | 31.00 | 26.18 | 7.00 | 19.52 | 4.00 | 30.51 | 14.00 | 80.49 |
| RethinkMCTS APPS native_v2 (tam thoi) + HumanEval run cu | 56.45 | 38.00 | 41.94 | 14.00 | 28.33 | 5.00 | 42.24 | 19.00 | 91.46 |

APPS candidate coverage theo nhom: Intro. 99/100, Inter. 96/100,
Comp. 91/100. Bang MCTS la lower-bound bao gom 14 candidate thieu, khong
phai bao cao search hoan chinh. HumanEval trong cung hang la ket qua
implementation/Modal workspace lich su; khong duoc suy dien nhu da chay
lai HumanEval `native_v2`.
