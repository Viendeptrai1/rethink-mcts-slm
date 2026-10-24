# Baselines

Thư mục này chứa direct-generation baseline và các config generation. Hướng dẫn
đầy đủ bắt đầu từ [../README.md](../README.md); runbook copy/chạy trực tiếp nằm ở
`../docs/runbooks/baseline-full.md`.

## Trách nhiệm của package

```text
baselines/
├── direct_generation/
│   ├── configs/              # Prompt/model/sampling config
│   ├── cli.py                # Sinh một candidate
│   └── pipeline.py           # Prompt, extraction và artifact schema
├── batch_generation.py       # Batch generation + resume + manifest/log
├── generate_apps.py          # Entry point một bài APPS
├── generate_humaneval.py     # Entry point một bài HumanEval
├── run_apps_benchmark.py     # Wrapper batch APPS cũ/tương thích
├── run_humaneval_benchmark.py# Wrapper batch HumanEval cũ/tương thích
└── sample_selection.py       # Đọc manifest sample cố định
```

Generation không đọc solution hoặc test chuẩn. Candidate được lưu tại:

```text
outputs/baselines/direct_generation/<run>/<model>/<dataset>/<problem_timestamp>/
├── problem.txt
├── response.txt
├── solution.py
└── metadata.json
```

## Run hiện tại

```text
model: qwen2.5-coder:7b-instruct
provider: Ollama trên GPU CKEY
run: qwen25_coder_7b_instruct_baseline_v1
```

Generation full không truyền `--sample-file`. Hai manifest dưới đây là của
**benchmark v1 đã chạy**, không phải cohort cho các run mới:

```text
data/samples/evaluation_v1/apps_test_100.json
data/samples/evaluation_v1/humaneval_test_100.json
```

Hai file `data/samples/baseline_v1/` chỉ là sample lịch sử được giữ để truy vết.
Không dùng chúng cho benchmark v2.

Benchmark từ nay về sau dùng `data/samples/benchmark_v2/apps_test_300.json`
và `data/samples/benchmark_v2/humaneval_test_164.json`; xem
[`docs/runbooks/benchmark-v2.md`](../docs/runbooks/benchmark-v2.md). Dùng run
name mới khi đổi cohort để không ghi đè kết quả 100+100 cũ.

## Lệnh chính

Xem plan, không gọi LLM:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage generate `
  --dataset all `
  --run-name <run_name> `
  --config baselines/direct_generation/configs/qwen25_coder_7b_instruct.json `
  --plan
```

Sinh full, resume artifact đã có:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage generate `
  --dataset all `
  --run-name <run_name> `
  --config baselines/direct_generation/configs/qwen25_coder_7b_instruct.json `
  --generation-workers 1 `
  --delay 1 `
  --confirm-full-run
```

Đánh giá APPS sample:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage evaluate `
  --dataset apps `
  --run-name <run_name> `
  --model <model> `
  --sample-file data/samples/evaluation_v1/apps_test_100.json `
  --workers 8 `
  --test-workers 4 `
  --evaluation-timeout 300 `
  --confirm-full-run
```

Đánh giá HumanEval sample:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage evaluate `
  --dataset humaneval `
  --run-name <run_name> `
  --model <model> `
  --sample-file data/samples/evaluation_v1/humaneval_test_100.json `
  --workers 8 `
  --evaluation-timeout 300 `
  --confirm-full-run
```

Sau khi cả hai evaluation có `results.jsonl`, tạo bảng:

```powershell
.\venv\Scripts\python.exe -m evaluation.benchmark_judge `
  --run-name <run_name> `
  --model <model>
```

## Quy tắc vận hành

- Luôn chạy `--plan` trước batch lớn.
- Không dùng `--no-resume` nếu chỉ muốn chạy tiếp.
- Không chạy hai evaluator cùng lúc trên cùng run/model.
- `--workers` là số bài song song; `--test-workers` là số test APPS song song trong mỗi bài.
- `--evaluation-timeout` là timeout cho từng test APPS hoặc toàn bộ harness HumanEval.
- Không sửa `solution.py` sau generation nếu muốn giữ baseline tái lập.
- Không commit `.env`, token hoặc output generated vào Git.
