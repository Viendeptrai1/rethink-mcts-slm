# Executor và chấm test

## Phạm vi

`Executors/` là tầng độc lập nhận Python source code, chạy test của dataset và trả
về báo cáo có cấu trúc. Tầng này không gọi LLM, không đọc lời giải chuẩn và chưa
tham gia MCTS.

## Giao diện chung

Hai executor trả về `ExecutionReport` với các trường chính:

| Trường | Ý nghĩa |
|---|---|
| `dataset`, `problem_id` | Bài được chấm |
| `mode` | Kiểu chạy test |
| `status` | `passed` khi mọi test đã chạy đều pass, ngược lại là `failed` |
| `passed_tests` | Số test pass |
| `total_tests` | Số test thực sự đã chạy |
| `available_tests` | Tổng số test có trong dữ liệu |
| `pass_rate` | `passed_tests / total_tests` |
| `duration_seconds` | Tổng thời gian các subprocess |
| `tests` | Kết quả từng test, gồm status, output, lỗi và thời gian |

Status từng test gồm `passed`, `wrong_answer`, `runtime_error` hoặc `timeout`.

Chấm trên máy thuê: [runbook remote evaluation](runbooks/remote-evaluation.md)
đóng gói đúng cohort và chạy evaluator này trong Docker. Container giới hạn
tài nguyên ở cấp batch, chưa cô lập từng test; giới hạn hiện tại vẫn là timeout
từng test APPS hoặc cả harness HumanEval, không phải timeout tổng cho một bài.
Output/error dài được cắt bớt trong báo cáo để tránh artifact tăng không giới hạn.
Batch evaluator dùng danh sách test này để ghi `failed_test_indices`; expected,
actual và traceback chi tiết vẫn được giữ trong `evaluation.json` từng bài.

## APPS

`AppsExecutor` đọc `input_output.json` tại
`data/apps/raw/<split>/<problem-id>/` và tự nhận diện hai chế độ:

- `stdin_stdout`: mỗi cặp `inputs[i]`/`outputs[i]` chạy trong một subprocess riêng.
  So sánh output sau khi chuẩn hóa khoảng trắng, nhưng không đổi thứ tự token.
- `call_based`: khi có `fn_name`, executor tìm hàm ở cấp module hoặc method cùng
  tên trên `Solution`, gọi bằng dữ liệu input và so sánh cấu trúc đệ quy. Số thực
  dùng tolerance `1e-7`.

`--max-tests` chỉ chạy N test đầu để smoke test; khi đó `total_tests` là N còn
`available_tests` vẫn phản ánh toàn bộ test của bài.

## HumanEval

`HumanevalExecutor` ghép candidate code với trường `test` chính thức và gọi
`check(entry_point)`. HumanEval lưu toàn bộ assertion trong một harness, không lưu
từng test case thành các hàng riêng. Vì vậy báo cáo có quy ước:

- harness hoàn tất: `1/1` pass;
- assertion thất bại: `0/1`, `wrong_answer`;
- exception khác: `0/1`, `runtime_error`;
- vượt timeout: `0/1`, `timeout`.

Không tách source bằng cách đếm hoặc parse các câu `assert`, vì thao tác đó có thể
làm thay đổi ngữ nghĩa harness.

## Metric judge

Per-problem `ExecutionReport.pass_rate` la so test pass chia so test da chay.
`evaluation.benchmark_judge` dung report nay de tinh macro Pass Rate, micro Pass
Rate va Pass@1 cho sample evaluation co dinh. APPS duoc tach theo difficulty;
HumanEval chi bao Pass@1 vi official harness khong phai hidden-test Pass Rate.

## CLI

Chấm một file code APPS:

```powershell
.\venv\Scripts\python.exe -m Executors `
  --dataset apps `
  --split test `
  --problem-id 0 `
  --code-file path\to\solution.py `
  --timeout 2 `
  --report-file path\to\evaluation.json
```

Chấm HumanEval:

```powershell
.\venv\Scripts\python.exe -m Executors `
  --dataset humaneval `
  --problem-id 0 `
  --code-file path\to\solution.py `
  --timeout 5
```

CLI in JSON ra stdout, trả exit code `0` khi toàn bộ test pass và `1` nếu không.

## Giới hạn an toàn

Mỗi test chạy bằng Python isolated mode (`-I`) trong thư mục tạm, có timeout và
dọn cây tiến trình theo best effort. Đây là cô lập tiến trình để benchmark, **không
phải security sandbox**: code do model sinh vẫn có thể đọc file, truy cập mạng hoặc
tạo tiến trình. Benchmark quy mô lớn hoặc code không tin cậy phải chạy executor
bên trong container/VM riêng, tắt mạng và đặt giới hạn CPU/RAM ở tầng hệ điều hành.

## Trạng thái xác minh

Đã kiểm chứng offline ngày 2026-09-26:

- APPS `stdin_stdout` báo đúng partial pass.
- APPS `call_based` gọi được method của `Solution`.
- Solution có sẵn của APPS `test/0000` pass `3/3` test đầu; bài có tổng cộng 565 test.
- Timeout được ghi nhận và tiến trình kết thúc.
- `HumanEval/0` pass với implementation đúng và fail với implementation sai.
- Không có request nào được gửi tới Modal trong quá trình test.
## Đánh giá lại run lịch sử với timeout rộng hơn

Mặc định APPS dùng timeout `2` giây cho từng test case. Để kiểm tra lại các
candidate mà không dừng quá sớm, chạy:

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

`--evaluation-timeout 300` áp dụng tối đa 300 giây cho **mỗi test case**, không
phải toàn bộ bài. Bài có nhiều test có thể mất hơn 5 phút. `--no-resume` chỉ
chạy lại evaluator và ghi đè báo cáo evaluation; không sửa `solution.py`.
