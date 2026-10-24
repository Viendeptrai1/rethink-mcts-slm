# Direct-generation baseline

## Benchmark v1 da khoa

Baseline v1 dung `qwen2.5-coder:7b-instruct` qua Ollama. Generation chay full
dataset; judge **da chay** 100 bai moi dataset trong
`data/samples/evaluation_v1/`. Cohort cho cac run moi la
`data/samples/benchmark_v2/` (300 APPS + 164 HumanEval). Sample
`baseline_v1` la tap tham chieu rieng va khong thay the hai cohort tren.

Run name: `qwen25_coder_7b_instruct_baseline_v1`. Artifact luon co model namespace
de khong tron ket qua giua cac model.

## Phạm vi

Baseline hiện tại thực hiện đúng một việc:

```text
đọc một bài toán -> gửi prompt tới LLM trên Modal -> nhận code -> lưu artifact
```

Mặc định package chỉ sinh code và **không sử dụng MCTS/Rethink**. Khi người dùng
chọn `--evaluate`, CLI gọi tầng `Executors` độc lập sau khi đã lưu candidate; xem
`docs/executors.md`.

## Thành phần

| File | Trách nhiệm |
|---|---|
| `baselines/generate_apps.py` | Entry point APPS, tự cố định dataset |
| `baselines/generate_humaneval.py` | Entry point HumanEval, tự cố định dataset |
| `baselines/run_apps_benchmark.py` | Batch APPS có range, resume và manifest |
| `baselines/run_humaneval_benchmark.py` | Batch HumanEval có range, resume và manifest |
| `baselines/batch_generation.py` | Điều phối batch dùng chung, gọi entry point từng bài |
| `baselines/direct_generation/cli.py` | CLI và điều phối một lần sinh |
| `baselines/direct_generation/pipeline.py` | Config, prompt, bóc code và lưu artifact |
| `baselines/direct_generation/configs/*.json` | Các cấu hình benchmark có tên/version |
| `DataProcess/problem_loader.py` | Đọc đề APPS/HumanEval mà không đọc solution/test |
| `ChatModels/modal_client.py` | Gọi endpoint OpenAI-compatible trên Modal |
| `tests/test_baseline.py` | Unit test offline cho loader, prompt và code extraction |

Hai entry point khuyến nghị cho người dùng:

```powershell
.\venv\Scripts\python.exe -m baselines.generate_apps --help
.\venv\Scripts\python.exe -m baselines.generate_humaneval --help
```

CLI chung `python -m baselines.direct_generation --dataset ...` vẫn được giữ để
script benchmark có thể chọn dataset động. Hai file riêng chỉ là wrapper mỏng,
không sao chép code gọi Modal.

## Chống data leakage

- APPS loader chỉ đọc `question.txt` và `starter_code.py` nếu có.
- APPS loader không đọc `solutions.json` hoặc `input_output.json`.
- HumanEval loader chỉ lấy `prompt`, `task_id` và `entry_point`.
- HumanEval loader không đưa `canonical_solution` hoặc `test` vào `Problem`.

## Dry-run không gọi API

APPS:

```powershell
.\venv\Scripts\python.exe -m baselines.generate_apps `
  --split test `
  --problem-id 0 `
  --dry-run
```

HumanEval:

```powershell
.\venv\Scripts\python.exe -m baselines.generate_humaneval `
  --problem-id 0 `
  --dry-run
```

## Sinh code thật

Mỗi lệnh chỉ gửi đúng một request:

```powershell
.\venv\Scripts\python.exe -m baselines.generate_humaneval `
  --problem-id 0
```

Các tham số chính:

| Tham số | Mặc định | Ý nghĩa |
|---|---:|---|
| `--config` | `configs/default.json` | File cấu hình run/prompt/generation |
| `--run-name` | từ config | Nhãn nhóm thí nghiệm trong output |
| `--model` | config hoặc provider env | Override model cho một lần chạy |
| `--split` | `test` | Split APPS; HumanEval luôn dùng test |
| `--max-tokens` | không gửi | Giới hạn output token nếu muốn đặt thủ công |
| `--temperature` | `0.2` | Sampling temperature |
| `--top-p` | `0.95` | Nucleus sampling |
| `--reasoning-effort` | không gửi | Chỉ gửi khi endpoint Modal cần |
| `--output-dir` | `outputs/baselines` | Root của artifact baseline |
| `--evaluate` | tắt | Chấm ngay và lưu `evaluation.json` cạnh code |
| `--evaluation-timeout` | APPS: 2s; HumanEval: 5s | Timeout khi dùng `--evaluate` |
| `--max-tests` | tất cả | Chỉ chấm N test đầu của APPS |

Mỗi config có thể lưu trường `model`; nếu để `null` thì dùng `LLM_MODEL` khi
`LLM_PROVIDER=ollama`, hoặc `KIMI_MODEL` khi dùng Modal. Tham số CLI ghi đè giá trị
tương ứng trong config. Endpoint và token không được đưa vào config
benchmark mà vẫn chỉ lấy từ `.env`.

Ví dụ chạy cùng config với model khác:

```powershell
.\venv\Scripts\python.exe -m baselines.generate_humaneval `
  --problem-id 0 `
  --config baselines/direct_generation/configs/default.json `
  --model organization/model-name
```

## Artifact

Mỗi lần gọi thành công tạo một thư mục:

```text
outputs/baselines/direct_generation/<run-name>/<model>/<dataset>/<problem-id>_<UTC timestamp>/
├── problem.txt       # prompt user đã gửi
├── response.txt      # response gốc từ model
├── solution.py       # code đã bóc khỏi Markdown fence nếu có
├── metadata.json     # model, tham số, usage, finish reason
└── evaluation.json   # chỉ có khi dùng --evaluate hoặc chấm lại vào cùng thư mục
```

`metadata.json` của bước sinh vẫn có `"evaluation": null`; báo cáo chấm được tạo
riêng bằng CLI executor. Khi thêm `--evaluate`, thư mục có thêm `evaluation.json`
và trường `evaluation` trong metadata được cập nhật bằng kết quả tóm tắt. Thư mục
`outputs/` được Git ignore.

Ví dụ sinh và chấm ngay tối đa 10 test APPS:

```powershell
.\venv\Scripts\python.exe -m baselines.generate_apps `
  --problem-id 0 `
  --evaluate `
  --max-tests 10
```

Không có `--evaluate`, CLI in sẵn lệnh PowerShell để chấm `solution.py` sau.

Config mặc định đặt `max_tokens: null`; client không gửi trường `max_tokens` tới
Modal. Đây không phải output vô hạn tuyệt đối: model/endpoint vẫn bị giới hạn bởi
context window và cấu hình server. Có thể đặt lại giới hạn bằng `--max-tokens N`.

Artifact chỉ được xem là hoàn chỉnh khi `response.txt` và `solution.py` có nội dung,
cùng `finish_reason` là `stop` (hoặc provider không trả finish reason). Response rỗng,
`finish_reason=length` hay trạng thái không hoàn chỉnh khác vẫn được lưu để audit
nhưng command trả lỗi và resume sẽ tự sinh lại problem đó.

## Chạy hàng loạt

Luôn xem kế hoạch trước; `--plan` không gọi Modal:

```powershell
.\venv\Scripts\python.exe -m baselines.run_apps_benchmark --plan
.\venv\Scripts\python.exe -m baselines.run_humaneval_benchmark --plan
```

Smoke test hai bài cho mỗi dataset:

```powershell
.\venv\Scripts\python.exe -m baselines.run_apps_benchmark `
  --limit 2 `
  --run-name smoke_apps_v1

.\venv\Scripts\python.exe -m baselines.run_humaneval_benchmark `
  --limit 2 `
  --run-name smoke_humaneval_v1
```

Chạy toàn bộ APPS test (5.000 bài) và HumanEval (164 bài):

```powershell
.\venv\Scripts\python.exe -m baselines.run_apps_benchmark `
  --run-name full_apps_test_v1 `
  --delay 1 `
  --confirm-full-run

.\venv\Scripts\python.exe -m baselines.run_humaneval_benchmark `
  --run-name full_humaneval_v1 `
  --delay 1 `
  --confirm-full-run
```

Batch chạy tuần tự. Resume được bật mặc định: chạy lại đúng `run-name`, model và
dataset sẽ bỏ qua bài đã có `solution.py`; nếu dùng `--evaluate`, chỉ bỏ qua khi có
thêm `evaluation.json`. Dùng `--no-resume` nếu chủ ý sinh candidate mới. Nên dùng
`run-name` khác khi thay prompt hoặc generation parameters.

Các tùy chọn hữu ích:

| Tham số | Ý nghĩa |
|---|---|
| `--start`, `--end` | Khoảng ID bao đóng cần chạy |
| `--limit N` | Chỉ lấy N ID đầu trong khoảng |
| `--delay SECONDS` | Nghỉ giữa hai request |
| `--generation-workers N` | Số request Modal chạy đồng thời; mặc định 2 |
| `--retries N` | Retry request lỗi; mặc định 0 để tránh phát sinh chi phí ngoài ý muốn |
| `--fail-fast` | Dừng batch ngay khi một bài lỗi |
| `--evaluate` | Chấm code ngay sau mỗi lần sinh |
| `--confirm-full-run` | Bắt buộc khi chọn hơn 20 bài |

Mỗi kết quả vẫn nằm trong cây artifact ở trên. Batch ghi thêm nhật ký append-only:

```text
outputs/baselines/batch_manifests/<run-name>/<model>/apps.jsonl
outputs/baselines/batch_manifests/<run-name>/<model>/humaneval.jsonl
outputs/baselines/batch_manifests/<run-name>/<model>/apps.log
outputs/baselines/batch_manifests/<run-name>/<model>/humaneval.log
```

Hai full batch tạo tổng cộng 5.164 request LLM trước retry. Kiểm tra quota và chi phí
Modal trước khi dùng `--confirm-full-run`.

## Trạng thái xác minh

Đã xác minh offline ngày 2026-09-26:

- 13 unit tests riêng của baseline đều pass.
- APPS test/0000 load và dựng prompt được.
- HumanEval/0 load và dựng prompt được.
- Hai entry point riêng đều dry-run thành công.
- Hai batch entry point `--plan --limit 2` thành công và không gọi Modal.
- Dry-run không tạo artifact.
- Config mặc định load và validate được.
- Đã gọi Modal thật trong run `direct_full_v1`; adapter nhận được response và lưu
  artifact. Giới hạn 2.048 token cũ gây nhiều `finish_reason=length`, nay đã bỏ khỏi
  config mặc định và các artifact chưa hoàn chỉnh sẽ được sinh lại.
