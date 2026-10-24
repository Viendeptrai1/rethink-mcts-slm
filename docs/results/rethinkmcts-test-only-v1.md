# RethinkMCTS test-only: ket qua va provenance

Kiem tra ngay 2026-10-06. Day la ablation bo LLM self-evaluation khoi
reward; khong thay doi code candidate sau khi sinh.

## Cau hinh

- Cohort: `data/samples/benchmark_v2/`, APPS 300 (100 moi muc do kho),
  HumanEval 164.
- Model: `qwen2.5-coder:7b-instruct`, digest
  `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`;
  Modal L40S, prompt `native_v2`.
- Search: 2 rollouts, width 3, seed 0, toi da 2 rethink, 4 problem worker,
  1 APPS test worker/candidate, gioi han 900 giay/problem.
- Reward: `passed_public_tests / total_public_tests`; khong goi LLM
  self-evaluation. APPS public policy `half`; HumanEval search dung given tests.
- Rejudge: APPS chay tat ca test trong `input_output.json`, 5 giay/test;
  HumanEval dung official harness, 5 giay/bai; 2 CPU problem worker.

## Ket qua

| Nhom | Pass Rate (%) | Pass@1 (%) | Candidate | Pass het |
|---|---:|---:|---:|---:|
| APPS Introductory | 61.14 | 41.00 | 100/100 | 41 |
| APPS Interview | 45.46 | 18.00 | 98/100 | 18 |
| APPS Competition | 29.42 | 9.00 | 99/100 | 9 |
| APPS Overall | 45.34 | 22.67 | 297/300 | 68 |
| HumanEval | N/A | 89.63 | 164/164 | 147 |

APPS Pass Rate la macro mean theo 300 problem; ID khong co candidate
dong gop 0. `summary.json` cua executor tinh tren 297 candidate da cham,
nen khong dung truc tiep `mean_test_pass_rate` cua file do de dien vao
bang cohort 300. HumanEval khong bao Pass Rate.

## Bai chua hoan tat

Ba APPS `0841`, `1033`, `3702` search timeout sau 900 giay, khong co
`final_solution.py` va khong duoc rejudge. Chung duoc tinh 0 trong mau so
theo quy tac adjudication, khong tao test report gia va khong phai bang
chung code sai. Trong 297 candidate APPS da cham, 19 candidate co ket qua
final `timeout`; day la loai timeout khac voi ba search timeout tren.

Outcome APPS: 68 passed, 188 wrong_answer, 22 runtime_error, 19 timeout.
Outcome HumanEval: 147 passed, 14 wrong_answer, 2 runtime_error, 1 timeout.

## Artifact

- Search APPS: `outputs/rethinkmcts/rethinkmcts_apps_test_only_v1/qwen2.5-coder_7b-instruct/apps/`.
- Search HumanEval: `outputs/rethinkmcts/rethinkmcts_humaneval_test_only_v1/qwen2.5-coder_7b-instruct/humaneval/`.
- APPS metrics: `outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_apps_test_only_v1_all_tests/qwen2.5-coder_7b-instruct/apps/benchmark_metrics.json`.
- HumanEval metrics: `outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_humaneval_test_only_v1_official/qwen2.5-coder_7b-instruct/humaneval/benchmark_metrics.json`.
- Moi search run co `run_config.json`; moi rejudge co `evaluation_config.json`,
  `summary.json`, `results.jsonl` va `evaluation.log`.

So sanh voi `dual` chi la doi chieu tham khao: APPS `dual` co 295/300
candidate; HumanEval `dual` dung `native_v1` lich su. Khong quy chenhlech
ket qua rieng cho viec bo `v_llm`.
