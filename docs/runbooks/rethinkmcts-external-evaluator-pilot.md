# Dual với evaluator model riêng: APPS 30 + HumanEval 164

Thử nghiệm này giữ generator `qwen2.5-coder:7b-instruct`, nhưng dùng
`qwen2.5-coder:14b-instruct` chỉ cho `self_evaluation` ([0m`v_llm`[0m).
Expansion, code generation, verbal feedback và rethink vẫn chạy trên generator.
Reward Dual là `v_test` khi `v_test < 1`; khi pass toàn bộ public tests thì
`0.8 * v_test + 0.2 * v_llm`. Modal chạy inference; executor và final judge
vẫn chạy cục bộ trên máy dự án.

APPS dùng manifest cố định 30 ID, 10 bài mỗi độ khó. HumanEval dùng đủ 164 ID.
Kết quả APPS là pilot `n=30`, không được gán nhãn hoặc ngoại suy thành `n=300`.
Không resume run cũ; artifacts được ghi vào run name mới.

## 1. Kiểm tra và lập kế hoạch

PowerShell từ `D:\ReThinkMCTS`:

```powershell
$run = 'rethinkmcts_dual_external_qwen25_14b_pilot_v1'
$appsSample = 'data/samples/benchmark_v2/apps_test_30_external_evaluator_pilot.json'
$generator = 'qwen2.5-coder:7b-instruct'
$evaluator = 'qwen2.5-coder:14b-instruct'

.\venv\Scripts\python.exe -m unittest discover -s tests -q
.\venv\Scripts\python.exe -m tools.modal_mcts.run --plan --dataset apps `
  --run-name $run --reward-mode dual --evaluator-model $evaluator `
  --apps-sample-file $appsSample --workers 4
.\venv\Scripts\python.exe -m tools.modal_mcts.run --plan --dataset humaneval `
  --run-name $run --reward-mode dual --evaluator-model $evaluator `
  --apps-sample-file $appsSample --workers 4
```

APPS plan phải báo 30 bài. HumanEval plan phải báo 164. `--plan` không gọi
Modal. Tham số search được giữ như Dual hiện tại: 2 rollouts, width 3, seed 0,
2 lần rethink tối đa, APPS public policy `half`, timeout 5 giây/public test,
900 giây/problem, 4 problem workers.

## 2. Deploy và pin hai model

Xác nhận Modal account/budget trước. Deploy cập nhật app hiện có; preflight sẽ
khởi tạo GPU L40S và tải evaluator vào persistent Ollama Volume nếu chưa có,
nên bước này có thể phát sinh GPU và network/storage usage.

```powershell
.\venv\Scripts\python.exe -m modal token info
.\venv\Scripts\python.exe -m modal deploy tools/modal_mcts/inference.py
.\venv\Scripts\python.exe -m tools.modal_mcts.run --preflight --dataset apps `
  --run-name $run --reward-mode dual --evaluator-model $evaluator `
  --apps-sample-file $appsSample --workers 4
```

Preflight phải in digest cho cả hai model và báo GPU L40S. Gán digest đúng như
đầu ra của lần preflight hiện tại; không dùng digest cũ hoặc tự đoán:

```powershell
$generatorDigest = '<digest của qwen2.5-coder:7b-instruct>'
$evaluatorDigest = '<digest của qwen2.5-coder:14b-instruct>'
```

## 3. Smoke rồi chạy search

Smoke chạy một bài APPS trong manifest và ghi vào namespace của run mới. Kiểm
tra request log để xác nhận `self_evaluation` dùng model 14B, các operation
còn lại dùng 7B; nếu smoke ổn mới chạy cohort.

```powershell
.\venv\Scripts\python.exe -m tools.modal_mcts.run --smoke --dataset apps `
  --run-name $run --reward-mode dual --evaluator-model $evaluator `
  --apps-sample-file $appsSample --workers 4 `
  --expected-model-digest $generatorDigest `
  --expected-evaluator-model-digest $evaluatorDigest

.\venv\Scripts\python.exe -m tools.modal_mcts.run --dataset apps `
  --run-name $run --reward-mode dual --evaluator-model $evaluator `
  --apps-sample-file $appsSample --workers 4 `
  --expected-model-digest $generatorDigest `
  --expected-evaluator-model-digest $evaluatorDigest --confirm-full-run

.\venv\Scripts\python.exe -m tools.modal_mcts.run --dataset humaneval `
  --run-name $run --reward-mode dual --evaluator-model $evaluator `
  --apps-sample-file $appsSample --workers 4 `
  --expected-model-digest $generatorDigest `
  --expected-evaluator-model-digest $evaluatorDigest --confirm-full-run
```

Chạy APPS và HumanEval tuần tự với cùng run name/cấu hình để resume identity
nhất quán; mỗi bài hoàn tất được skip khi chạy lại. Không chạy hai batch cùng
run name đồng thời. Final evaluation trong summary dùng toàn bộ APPS tests và
HumanEval official harness. Có thể chạy rejudge độc lập:

```powershell
.\venv\Scripts\python.exe -m evaluation.rejudge_mcts --dataset apps `
  --source-run-name $run --run-name "${run}_apps_all_tests" `
  --model $generator --sample-file $appsSample --workers 2 --timeout 5 --confirm-full-run
.\venv\Scripts\python.exe -m evaluation.rejudge_mcts --dataset humaneval `
  --source-run-name $run --run-name "${run}_humaneval_official" `
  --model $generator --sample-file data/samples/benchmark_v2/humaneval_test_164.json `
  --workers 2 --timeout 5 --confirm-full-run
```

## 4. Tạo bảng pilot có denominator thật

Reporter đọc final all-tests evaluation trong search summaries. Có thể thêm
paired direct baseline và `test_only` trên cùng 30 APPS + 164 HumanEval; thêm
Dual cũ chỉ cho APPS vì HumanEval Dual trước đây dùng `native_v1`.

```powershell
.\venv\Scripts\python.exe -m rethinkmcts.pilot_benchmark `
  --run-name $run --model $generator `
  --comparison "Direct Evaluation=outputs/baselines/evaluations/qwen25_coder_7b_instruct_baseline_benchmark_v2_all_tests/qwen2.5-coder_7b-instruct/apps/results.jsonl|outputs/baselines/evaluations/qwen25_coder_7b_instruct_baseline_benchmark_v2_all_tests/qwen2.5-coder_7b-instruct/humaneval/results.jsonl" `
  --comparison "RethinkMCTS test_only=outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_apps_test_only_v1_all_tests/qwen2.5-coder_7b-instruct/apps/results.jsonl|outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_humaneval_test_only_v1_official/qwen2.5-coder_7b-instruct/humaneval/results.jsonl" `
  --comparison "RethinkMCTS dual (self evaluator)=outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_apps_interface_v2_half_w4_all_tests/qwen2.5-coder_7b-instruct/apps/results.jsonl|-"
```

Bảng và provenance được tạo tại
`outputs/benchmarks/<run>/<generator>/apps30_pilot/`. Mỗi nhóm APPS phải có
denominator 10, APPS overall 30, HumanEval 164. Mục HumanEval của comparator
Dual cũ hiện `N/A`, không giả lập số. Không dùng
`python -m rethinkmcts.benchmark`: finalizer đó chỉ chấp nhận cohort benchmark
đầy đủ 300 APPS + 164 HumanEval.

## Artifact và an toàn

- Generator giữ namespace `outputs/rethinkmcts/<run>/qwen2.5-coder_7b-instruct/`;
  `run_config.json` ghi evaluator model và cả hai digest.
- Mỗi `llm_request` event/summary ghi model thực tế, operation và token usage.
- Báo cáo pilot không sửa bảng `dual`, `test_only`, baseline hoặc manifest
  benchmark_v2 hiện có.
- LLM inference chạy trên Modal; code do LLM sinh vẫn được execute trên máy
  local trong `Executors`. Chỉ chạy khi chấp nhận chạy untrusted code tại đó.
