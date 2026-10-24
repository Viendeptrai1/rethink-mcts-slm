# Pipeline direct baseline

## Cau hinh benchmark hien tai

Benchmark moi dung hai manifest `data/samples/benchmark_v2/` (APPS 300 +
HumanEval 164) va dung cung `--sample-file` cho moi model/MCTS. Doan lenh
ben duoi la vi du tai lap **run cu 100+100**, khong phai cohort moi:

Cap nhat van hanh: direct baseline da hoan thanh generation va evaluation sample;
lenh chinh thuc va quy tac resume nam tai
[`docs/runbooks/baseline-full.md`](runbooks/baseline-full.md). Sample 100 o
duoi chi duoc giu de truy vet ket qua cu.

Phan sample `baseline_v1` ben duoi duoc giu de tham chieu lich su; full generation
hien tai khong truyen `--sample-file`.

```powershell
$run = "qwen25_coder_7b_instruct_baseline_v1"
$config = "baselines/direct_generation/configs/qwen25_coder_7b_instruct.json"

.\venv\Scripts\python.exe -m pipelines `
  --stage generate --dataset apps --run-name $run --config $config `
  --generation-workers 1 --delay 1 --confirm-full-run

.\venv\Scripts\python.exe -m pipelines `
  --stage evaluate --dataset apps --run-name $run `
  --sample-file data/samples/evaluation_v1/apps_test_100.json `
  --workers 8 --test-workers 4 --evaluation-timeout 300 --confirm-full-run
```

Lap lai hai lenh tren cho `humaneval` voi file
`data/samples/evaluation_v1/humaneval_test_100.json`. Khong dung mot sample file cho
ca hai dataset: pipeline se kiem tra va tu choi neu dataset khong khop manifest.

Model va output luon duoc tach theo model:
`outputs/baselines/<stage>/<run>/<model>/<dataset>/`.

## Luồng chính thức

Pipeline direct baseline gồm hai checkpoint tách biệt:

```text
Stage 1 - generate
  gọi Modal -> lưu toàn bộ candidate -> generation manifest hoàn chỉnh

Stage 2 - evaluate
  quét candidate đã lưu -> chấm song song -> báo cáo từng bài + tổng hợp
```

Không cần gọi lại LLM trong stage evaluation. Khi chạy `--stage all`, pipeline vẫn
hoàn thành generation cho tất cả dataset đã chọn trước khi bắt đầu candidate đầu
tiên của evaluation. Nếu generation có bài lỗi, pipeline dừng và không tự chấm.

## Xem kế hoạch

Lệnh sau không gọi Modal và không chạy code candidate:

```powershell
Set-Location D:\ReThinkMCTS

.\venv\Scripts\python.exe -m pipelines `
  --stage all `
  --dataset all `
  --run-name direct_full_v1 `
  --plan
```

Trong `--plan`, phần evaluation chỉ thấy artifact đã tồn tại; candidate dự kiến sinh
trong plan chưa được tạo nên chưa xuất hiện ở số lượng evaluation.

## Smoke test

Sinh hai bài mỗi dataset, sau đó chấm song song:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage all `
  --dataset all `
  --run-name direct_smoke_v1 `
  --limit 2 `
  --workers 2
```

Lệnh này tạo tối đa bốn request LLM: hai APPS và hai HumanEval.

## Chạy full theo hai lệnh

Checkpoint 1, chỉ sinh code cho 5.000 APPS test và 164 HumanEval:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage generate `
  --dataset all `
  --run-name direct_full_v1 `
  --generation-workers 2 `
  --delay 1 `
  --confirm-full-run
```

Sau khi kiểm tra generation manifest và số artifact, chạy checkpoint 2:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage evaluate `
  --dataset all `
  --run-name direct_full_v1 `
  --workers 4 `
  --confirm-full-run
```

Có thể dùng `--stage all` để tự chuyển stage, nhưng hai lệnh riêng dễ kiểm tra chi
phí, số candidate và lỗi generation trước khi thực thi code do model sinh.

## Song song hóa

Generation dùng `ThreadPoolExecutor` để giữ tối đa N request Modal đồng thời. Mỗi
worker gọi entry point một bài trong subprocess riêng; manifest và log chỉ được ghi
ở scheduler chính. Vì vậy artifact không ghi chồng, còn dòng `saved` có thể xuất
hiện khác thứ tự ID:

```text
[1/100] 0000: generating
[2/100] 0001: generating
[2/100] 0001: saved ...
[3/100] 0002: generating
[1/100] 0000: saved ...
```

`--generation-workers` mặc định là 2 để giới hạn tải trên provider. Chỉ tăng lên 4
sau khi xác nhận Modal deployment có đủ concurrency và không trả rate limit.
`--delay` giãn thời điểm scheduler cấp request thay thế, còn số request đang
chạy không vượt quá worker count.

Evaluation dùng process pool riêng và tham số `--workers`; hai tham số không dùng
chung vì generation chủ yếu chờ mạng, còn evaluation tiêu thụ CPU/subprocess.

Evaluation dùng `ProcessPoolExecutor` và phân phối **candidate/bài toán** cho worker:

```text
worker 1 -> candidate A -> các test của A
worker 2 -> candidate B -> các test của B
worker 3 -> candidate C -> các test của C
worker 4 -> candidate D -> các test của D
```

Các test bên trong một candidate không tạo thêm process pool lồng nhau. Executor
vẫn chạy candidate trong subprocess có timeout. Mặc định tối đa 4 worker; nên bắt
đầu với `--workers 4`, theo dõi CPU/RAM rồi mới tăng.

## Resume

Resume bật mặc định ở cả hai stage:

- Generate chỉ bỏ qua bài có `response.txt` và `solution.py` không rỗng, cùng finish
  reason hoàn chỉnh đúng run/model/dataset; bài rỗng hoặc bị cắt bởi token vẫn được
  sinh lại.
- Evaluate bỏ qua candidate đã có `evaluation.json` hợp lệ.
- Nếu cùng problem có nhiều artifact, evaluator chọn artifact có `created_at` mới nhất.
- Dùng `--no-resume` khi chủ ý chạy lại.
- Đổi `run-name` khi đổi prompt, model hoặc generation parameters.

## Artifact

Candidate và kết quả từng bài:

```text
outputs/baselines/direct_generation/<run>/<model>/<dataset>/<problem_timestamp>/
├── problem.txt
├── response.txt
├── solution.py
├── metadata.json
└── evaluation.json
```

Generation manifest append-only:

```text
outputs/baselines/batch_manifests/<run>/<model>/<dataset>.jsonl
outputs/baselines/batch_manifests/<run>/<model>/<dataset>.log
```

JSONL dùng cho xử lý bằng chương trình; file `.log` cho biết thời điểm bắt đầu/kết
thúc, từng `problem_id`, trạng thái generation, artifact hoặc lỗi request.

Kết quả tổng hợp evaluation:

```text
outputs/baselines/evaluations/<run>/<model>/<dataset>/
├── results.jsonl
├── results.csv
├── failures.jsonl
├── failures.csv
├── passed.jsonl
├── evaluation.log
└── summary.json
```

`summary.json` gồm `total_candidates`, `fully_passed`, `pass_at_1`,
`partially_passed`, `zero_tests_passed`, `mean_test_pass_rate`,
`micro_test_pass_rate`, tổng test pass/tổng test, `failed_problem_ids` và số lượng
theo `passed`, `wrong_answer`, `runtime_error`, `timeout`, `executor_error`.

Mỗi dòng `failures.jsonl/csv` chỉ rõ bài sai, số test pass, tổng test,
`failed_test_indices`, thống kê status và đường dẫn artifact. `evaluation.log` là bản
text đọc nhanh. Expected/actual/traceback đầy đủ vẫn nằm trong `evaluation.json` của
từng candidate để tránh file tổng hợp quá lớn.

Pipeline còn ghi chuyển stage tại:

```text
outputs/baselines/pipeline_logs/<run>/pipeline.log
```

Voi benchmark moi, log pipeline duoc tach tiep theo model:
`outputs/baselines/pipeline_logs/<run>/<model>/pipeline.log`. Log o cap
`<run>/pipeline.log` cua run cu la artifact lich su va khong dung cho benchmark moi.

## Lưu ý an toàn và chi phí

- Full APPS test + HumanEval tạo 5.164 request trước retry.
- Chọn hơn 20 bài bắt buộc có `--confirm-full-run`.
- Retry mặc định là 0; chỉ bật sau khi hiểu chi phí request lặp.
- Generation song song làm tăng số request/token đồng thời, không làm giảm tổng chi phí.
- Config mặc định không gửi `max_tokens`; giới hạn cuối vẫn do context/model/provider.
- Worker process và timeout không phải security sandbox. Trước full evaluation code
  không tin cậy, nên chạy toàn pipeline trong container/VM, tắt mạng và giới hạn
  CPU/RAM ở tầng hệ điều hành.

## Trạng thái xác minh

Đã kiểm chứng offline ngày 2026-09-26:

- Pipeline `--stage all --dataset all --limit 2 --plan` không gọi Modal.
- Candidate discovery chọn artifact mới nhất cho mỗi problem/model.
- HumanEval candidate được chấm qua process pool và pass `1/1`.
- APPS candidate được chấm qua process pool và pass `3/3` test đầu.
- `evaluation.json`, `results.jsonl`, `results.csv`, `summary.json` được tạo đúng.
- Candidate sai xuất hiện đúng trong `failures.jsonl/csv` và `evaluation.log`, kèm
  số test pass/tổng test và index test fail.
## Song song hai tầng khi evaluation

Evaluation hỗ trợ hai mức song song:

- `--workers`: số bài chạy đồng thời.
- `--test-workers`: số test APPS chạy đồng thời bên trong mỗi bài.

Mỗi test vẫn chạy trong subprocess riêng, có timeout riêng và kết quả được trả về
đúng thứ tự index. HumanEval không có nhiều test độc lập nên `--test-workers`
không ảnh hưởng đến HumanEval.

Với máy 32 logical CPU, cấu hình cân bằng cho sample APPS là:

```powershell
--workers 8 --test-workers 4
```

Tổng tối đa khoảng 32 candidate subprocess. Không nên chạy thêm một evaluator
khác trên cùng run vì các tiến trình sẽ ghi chung `evaluation.json`.
