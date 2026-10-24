# RethinkMCTS Smoke Run

## Trước khi chạy

Đã kiểm tra offline bằng:

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

Giai đoạn implement không tự gọi API. Khi bắt đầu smoke thật, chỉ chạy một problem với
rollout thấp và kiểm tra provider trong `.env` trước.

## Xem plan

```powershell
.\venv\Scripts\python.exe -m rethinkmcts `
  --dataset humaneval `
  --problem-id 0 `
  --run-name rethinkmcts_v1 `
  --model qwen2.5-coder:7b-instruct `
  --rollouts 2 `
  --width 3 `
  --plan
```

APPS dùng ID trong folder raw, ví dụ:

```powershell
.\venv\Scripts\python.exe -m rethinkmcts `
  --dataset apps `
  --problem-id 0002 `
  --run-name rethinkmcts_v1 `
  --model qwen2.5-coder:7b-instruct `
  --rollouts 2 `
  --width 3 `
  --plan
```

## Chạy thật sau khi smoke được duyệt

Bỏ `--plan`. Không chạy full dataset ở bước đầu. Output nằm dưới:

```text
outputs/rethinkmcts/<run>/<model>/<dataset>/<problem_id>/
```

Đọc `events.jsonl` để đối chiếu Selection, Expansion, Evaluation, Feedback, Backpropagation
và Rethink; đọc `search_summary.json` để xem reward và private evaluation.
