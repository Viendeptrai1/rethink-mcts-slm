# Full Direct Baseline

## Muc tieu

Run hien tai dung model Ollama `qwen2.5-coder:7b-instruct` tren GPU CKEY va chay:

- APPS test: 5.000 bai.
- HumanEval test: 164 bai.
- Tong: 5.164 request LLM truoc retry.

Run name lich su: `qwen25_coder_7b_instruct_baseline_v1`.

Runbook nay tai lap benchmark **lich su 100+100**, khong phai cohort moi.
Hai manifest `baseline_v1` duoc giu rieng de truy vet. Cohort cho cac run moi
va MCTS la `data/samples/benchmark_v2/` (APPS 300 + HumanEval 164); xem
[`docs/datasets.md`](../datasets.md). Khong ghi de evaluation run cu khi doi cohort.
Full generation không truyền `--sample-file`.

Judge cua full run dung hai manifest rieng:

```text
data/samples/evaluation_v1/apps_test_100.json
data/samples/evaluation_v1/humaneval_test_100.json
```

## Kiem tra provider

Tren GPU CKEY:

```bash
ollama list
ollama show qwen2.5-coder:7b-instruct
```

Tren may Windows, `.env` can co:

```env
LLM_PROVIDER=ollama
LLM_BASE_URL=http://n2.ckey.vn:2800/v1
LLM_MODEL=qwen2.5-coder:7b-instruct
LLM_API_KEY=ollama
```

## Xem plan

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage generate --dataset apps `
  --run-name qwen25_coder_7b_instruct_baseline_v1 `
  --config baselines/direct_generation/configs/qwen25_coder_7b_instruct.json `
  --plan

.\venv\Scripts\python.exe -m pipelines `
  --stage generate --dataset humaneval `
  --run-name qwen25_coder_7b_instruct_baseline_v1 `
  --config baselines/direct_generation/configs/qwen25_coder_7b_instruct.json `
  --plan
```

## Stage 1: Generate

APPS:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage generate --dataset apps `
  --run-name qwen25_coder_7b_instruct_baseline_v1 `
  --config baselines/direct_generation/configs/qwen25_coder_7b_instruct.json `
  --generation-workers 1 --delay 1 --confirm-full-run
```

HumanEval:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage generate --dataset humaneval `
  --run-name qwen25_coder_7b_instruct_baseline_v1 `
  --config baselines/direct_generation/configs/qwen25_coder_7b_instruct.json `
  --generation-workers 1 --delay 1 --confirm-full-run
```

Resume bat mac dinh. Artifact co `response.txt`, `solution.py` khong rong va finish
reason hoan tat se duoc skip. Khong dung `--no-resume`.

## Theo doi generation

```powershell
Get-Content outputs\baselines\batch_manifests\qwen25_coder_7b_instruct_baseline_v1\qwen2.5-coder_7b-instruct\apps.log -Wait
Get-Content outputs\baselines\batch_manifests\qwen25_coder_7b_instruct_baseline_v1\qwen2.5-coder_7b-instruct\humaneval.log -Wait
```

Neu bi dung, chay lai dung lenh generate. Pipeline se tinh lai completed/pending.

## Stage 2: Evaluate

APPS:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage evaluate --dataset apps `
  --run-name qwen25_coder_7b_instruct_baseline_v1 `
  --model qwen2.5-coder:7b-instruct `
  --sample-file data/samples/evaluation_v1/apps_test_100.json `
  --workers 8 --test-workers 4 --evaluation-timeout 300 --confirm-full-run
```

HumanEval:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage evaluate --dataset humaneval `
  --run-name qwen25_coder_7b_instruct_baseline_v1 `
  --model qwen2.5-coder:7b-instruct `
  --sample-file data/samples/evaluation_v1/humaneval_test_100.json `
  --workers 8 --evaluation-timeout 300 --confirm-full-run
```

Evaluation cung resume: candidate da co `evaluation.json` se duoc skip.

## Stage 3: Judge metrics

Judge khong chay code va khong goi LLM; no doc `results.jsonl` cua hai evaluation,
bo sung candidate missing vao denominator, roi tao metric va bang ket qua:

```powershell
.\venv\Scripts\python.exe -m evaluation.benchmark_judge `
  --run-name qwen25_coder_7b_instruct_baseline_v1 `
  --model qwen2.5-coder:7b-instruct `
  --apps-sample-file data/samples/evaluation_v1/apps_test_100.json `
  --humaneval-sample-file data/samples/evaluation_v1/humaneval_test_100.json
```

APPS co macro Pass Rate, micro Pass Rate va Pass@1 theo Intro/Inter/Comp/Overall.
HumanEval chi co Pass@1; Pass Rate duoc ghi `N/A`.

## Output

```text
outputs/baselines/
├── direct_generation/<run>/<model>/<dataset>/<problem_timestamp>/
├── batch_manifests/<run>/<model>/<dataset>.jsonl
├── evaluations/<run>/<model>/<dataset>/summary.json
├── evaluations/<run>/<model>/<dataset>/benchmark_metrics.json
├── evaluations/<run>/<model>/benchmark_table.csv
├── evaluations/<run>/<model>/benchmark_table.md
├── evaluations/<run>/<model>/benchmark_summary.json
└── pipeline_logs/<run>/<model>/pipeline.log
```

Model co dau `:` duoc sanitize trong ten folder Windows:
`qwen2.5-coder:7b-instruct` -> `qwen2.5-coder_7b-instruct`.

## Xem ket qua

```powershell
Get-Content outputs\baselines\evaluations\qwen25_coder_7b_instruct_baseline_v1\qwen2.5-coder_7b-instruct\apps\summary.json
Get-Content outputs\baselines\evaluations\qwen25_coder_7b_instruct_baseline_v1\qwen2.5-coder_7b-instruct\humaneval\summary.json
```

Failure chi tiet nam trong `failures.csv`, `failures.jsonl`, `evaluation.log` va
`evaluation.json` cua tung candidate.
## Đánh giá lại APPS với timeout 5 phút

Nếu lần đánh giá trước dùng timeout 2 giây và cần kiểm tra lại candidate mà
không sinh lại code:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage evaluate `
  --dataset apps `
  --run-name qwen25_coder_7b_instruct_baseline_v1 `
  --model qwen2.5-coder:7b-instruct `
  --sample-file data/samples/evaluation_v1/apps_test_100.json `
  --workers 2 `
  --evaluation-timeout 300 `
  --no-resume `
  --confirm-full-run
```

Timeout hiện tại là theo từng test case. `--no-resume` ghi đè các file
`evaluation.json` và aggregate evaluation, nhưng không ghi đè artifact
generation hay code đã sinh.
