# Ablation: bo LLM self-evaluation khoi reward

Run nay dung `reward_mode=test_only`: voi moi candidate, `reward =
passed_public_tests / total_public_tests`, ke ca khi pass het (`reward=1`).
Khong goi request `self_evaluation`; feedback va Rethink khi fail public
tests van giu nguyen. Day la thuc nghiem moi, khong sua artifact run `dual`.

## Protocol co dinh

- APPS cohort: `data/samples/benchmark_v2/apps_test_300.json` (100 ID/muc kho).
- HumanEval cohort: `data/samples/benchmark_v2/humaneval_test_164.json`;
  search dung given tests, final judge dung official harness.
- Model: `qwen2.5-coder:7b-instruct`; pin digest da kiem chung cua run doi chieu.
- Prompt `native_v2`; 2 rollouts, width 3, seed 0, public policy `half`,
  2 rethink toi da, 5 giay/public test, 900 giay/problem, 4 problem worker.
- Final judge: tat ca APPS tests trong `input_output.json`, 5 giay/test,
  2 CPU worker; ket qua final khong tham gia search/reward.
- Run name rieng: `rethinkmcts_apps_test_only_v1`; rejudge name:
  `rethinkmcts_apps_test_only_v1_all_tests`.
- HumanEval run rieng: `rethinkmcts_humaneval_test_only_v1`; rejudge name:
  `rethinkmcts_humaneval_test_only_v1_official`.

Chay trong PowerShell tai `D:\ReThinkMCTS`. `--plan` khong goi Modal.

```powershell
$run = 'rethinkmcts_apps_test_only_v1'
$digest = 'dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364'
.\venv\Scripts\python.exe -m unittest discover -s tests -q
.\venv\Scripts\python.exe -m tools.modal_mcts.run --plan --dataset apps `
  --run-name $run --reward-mode test_only --workers 4
```

Kiem tra Modal account/billing va deploy inference neu account/deployment
da thay doi. `--smoke` tao artifact trong chinh run name nay; kiem tra no
truoc khi goi ca cohort. Khong chay hai batch cung run name dong thoi.

```powershell
.\venv\Scripts\python.exe -m modal token info
.\venv\Scripts\python.exe -m modal deploy tools/modal_mcts/inference.py
.\venv\Scripts\python.exe -m tools.modal_mcts.run --smoke --dataset apps `
  --run-name $run --reward-mode test_only --workers 4 `
  --expected-model-digest $digest
.\venv\Scripts\python.exe -m tools.modal_mcts.run --dataset apps --limit 4 `
  --run-name $run --reward-mode test_only --workers 4 `
  --expected-model-digest $digest --confirm-full-run
.\venv\Scripts\python.exe -m tools.modal_mcts.run --dataset apps `
  --run-name $run --reward-mode test_only --workers 4 `
  --expected-model-digest $digest --confirm-full-run
```

Lenh full tren resume bai da hoan thanh voi dung config. Bai failed/timeout
chua co artifact hoan chinh se duoc thu lai; can kiem tra `progress.jsonl`
va `outputs/rethinkmcts_attempts/` neu loi lap lai. Khong tu dong coi
technical failure la loi logic cua candidate.

Neu run full dung sau 3 timeout/loss lien tiep, dung bo dieu phoi hang doi
lien tuc ben duoi. No giu toi da 4 problem worker; bai nao xong hoac loi thi
giao ngay bai tiep theo, khong cho bai cham nhat cua mot nhom. Moi candidate
van dung 1 APPS test worker. Config/source hash cua run duoc giu nguyen;
loi duoc ghi `progress.jsonl` va `attempt.log`. Khong chay song song voi lenh
full o tren. Exit code 1 sau cung nghia la van con bai thieu artifact, khong
phai cac bai phia sau bi bo qua.

```powershell
.\venv\Scripts\python.exe -m tools.modal_mcts.continue_run `
  --dataset apps --run-name rethinkmcts_apps_test_only_v1 `
  --reward-mode test_only --workers 4 `
  --expected-model-digest dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364
```

Sau generation, chay final judge va xem metric. Rejudge resume report da co;
`benchmark_metrics.json` tinh bai thieu candidate la 0 theo denominator 300,
nhung `summary.json` van ghi ro ID thieu. `--plan` hien coverage truoc khi chay.

```powershell
$judge = 'rethinkmcts_apps_test_only_v1_all_tests'
.\venv\Scripts\python.exe -m evaluation.rejudge_mcts --dataset apps `
  --source-run-name $run --run-name $judge `
  --model qwen2.5-coder:7b-instruct --timeout 5 --workers 2 --plan
.\venv\Scripts\python.exe -m evaluation.rejudge_mcts --dataset apps `
  --source-run-name $run --run-name $judge `
  --model qwen2.5-coder:7b-instruct --timeout 5 --workers 2 --confirm-full-run
$result = 'outputs/rethinkmcts_evaluations/evaluations/' + $judge + '/qwen2.5-coder_7b-instruct/apps'
Get-Content "$result/benchmark_metrics.json"
Get-Content "$result/summary.json"
```

Chay HumanEval cung reward mode va tham so search, nhung run name rieng de
theo doi tien do/doc lap. Khong dung lai HumanEval `dual` cu cho hang ablation.

```powershell
$heRun = 'rethinkmcts_humaneval_test_only_v1'
$heJudge = 'rethinkmcts_humaneval_test_only_v1_official'
.\venv\Scripts\python.exe -m tools.modal_mcts.run --plan --dataset humaneval `
  --run-name $heRun --reward-mode test_only --workers 4
.\venv\Scripts\python.exe -m tools.modal_mcts.run --smoke --dataset humaneval `
  --run-name $heRun --reward-mode test_only --workers 4 `
  --expected-model-digest $digest
.\venv\Scripts\python.exe -m tools.modal_mcts.run --dataset humaneval --limit 4 `
  --run-name $heRun --reward-mode test_only --workers 4 `
  --expected-model-digest $digest --confirm-full-run
.\venv\Scripts\python.exe -m tools.modal_mcts.run --dataset humaneval `
  --run-name $heRun --reward-mode test_only --workers 4 `
  --expected-model-digest $digest --confirm-full-run
.\venv\Scripts\python.exe -m evaluation.rejudge_mcts --dataset humaneval `
  --source-run-name $heRun --run-name $heJudge `
  --model qwen2.5-coder:7b-instruct --timeout 5 --workers 2 --plan
.\venv\Scripts\python.exe -m evaluation.rejudge_mcts --dataset humaneval `
  --source-run-name $heRun --run-name $heJudge `
  --model qwen2.5-coder:7b-instruct --timeout 5 --workers 2 --confirm-full-run
$heResult = 'outputs/rethinkmcts_evaluations/evaluations/' + $heJudge + '/qwen2.5-coder_7b-instruct/humaneval'
Get-Content "$heResult/benchmark_metrics.json"
```

So voi run `dual` tai `docs/results/rethinkmcts-apps-native-v2-w4-retry.md`:
APPS Overall Pass Rate 43.04%, Pass@1 19.00% (295/300 candidate). Ghi
coverage, timeout, request/token va source/model digest cung voi metric moi;
khong ket luan MCTS tot/xau chi tu mot lan run. `test_only` bo mot request
self-evaluation tren moi candidate pass public tests, nen chi phi va duong
search co the khac nhau du giu nguyen rollout/width.
