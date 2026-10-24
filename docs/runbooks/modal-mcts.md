# RethinkMCTS: Modal GPU inference, local judge

**Trạng thái 2026-10-04:** HumanEval 164/164 hoàn tất trên run L4 cũ.
Run APPS L40S `rethinkmcts_qwen25_modal_l40s_parallel_v1` đã chạy thật,
297/300 hoàn chỉnh. `0796` và `1581` lặp lỗi Windows file lock; `1033`
lặp timeout 900 giây. Không chạy finalizer trước khi xử lý ba bài này.
Xem
[báo cáo HumanEval](../results/rethinkmcts-modal-humaneval-v1.md).

**Cập nhật 2026-10-05:** Run APPS `native_v2` 4 worker
`rethinkmcts_apps_interface_v2_half_w4` có 295/300 candidate sau retry;
rejudge all-tests đã xong cho 295 bài. Ba search còn timeout, hai search
lỗi kỹ thuật AST vẫn thiếu candidate. Xem
[báo cáo sau retry](../results/rethinkmcts-apps-native-v2-w4-retry.md);
đừng dùng lệnh finalizer cohort đầy đủ cho run này.

Hai lỗi AST ở `1684` và `3702` đã được sửa trong code mới. Không resume
run gốc sau khi source hash đổi. Dùng `--problem-ids` để chọn đúng ID thuộc
cohort trong run riêng; `--apps-test-workers` chỉ song song test của một
candidate, khác với `--workers` song song problem. `3702` đã cần 2 test
worker và timeout tổng 1.800 giây để có final candidate. Kết quả/cấu hình
và provenance ở [báo cáo repair](../results/rethinkmcts-apps-ast-repair.md).

## Audit APPS và run kế tiếp

Run APPS L40S ở trên dùng prompt `native_v1`; bảng all-tests của run đó
đã được chấm đúng nhưng chưa phản ánh sửa giao diện APPS. Prompt `native_v2`
đã đưa `stdin/stdout` hoặc `fn_name` vào search, code, feedback và Rethink.
Không resume run lịch sử với source mới: batch so hash source và sẽ từ chối.

Trước khi gọi Modal, kiểm tra policy và cohort offline:

```powershell
.\venv\Scripts\python.exe -m tools.modal_mcts.run --plan --dataset apps `
  --run-name rethinkmcts_apps_interface_v2_half `
  --public-cases-type half --workers 2
```

`half` giữ đúng cách chia nửa đầu của repo tác giả. 85/300 bài chỉ có 3
test, nên search nhìn thấy 1 public test ở những bài đó. Nếu nghiên cứu
coverage cao hơn, dùng **một run name khác** và thêm
`--public-cases-type half_min2`; policy này dùng 2 public test cho 85 bài
trên và để lại 1 private test. Final evaluation vẫn chấm toàn bộ APPS tests.
Pilot một bài `0395` đã đạt 53/53 với prompt v2; xem
`docs/results/rethinkmcts-apps-0395-native-v2-smoke.md`. Run
`rethinkmcts_apps_interface_v2_half_w4` nay da co ket qua tam thoi 295/300
candidate sau retry; bang day du 300/300 van chua co.

Sau plan, dùng cùng `--run-name`, `--public-cases-type`, `--workers` và
model digest cho `--smoke`, rồi `--limit 10 --confirm-full-run`, rồi mới
chạy đủ cohort. Xem phần lệnh triển khai Modal bên dưới để lấy digest từ
run đã pin. Các bài hoàn thành trong **run mới** được resume; candidate cũ
không được coi là kết quả của prompt v2. So lieu tam thoi nam trong bao cao
duoc lien ket o dau runbook.

Nếu ghép APPS run v2 với HumanEval run cũ, hồ sơ phải nêu rõ hai source
run và prompt version khác nhau. Để có một benchmark thống nhất cùng
implementation, chạy HumanEval dưới cùng source/run v2 trước khi tổng hợp.

**Topology mới:** Ollama `qwen2.5-coder:7b-instruct` runs in a private Modal GPU
Function on up to four L40S containers. The MCTS coordinator, dataset loader, Python executor,
AST trace and artifacts run on the Windows laptop. Generated code is therefore
executed on the laptop. This is not the remote-judge workflow.

The Modal app uses the account token from `modal setup`, not the historical
`MODAL_PROXY_*` values in `.env`. It binds Ollama only to container loopback;
there is no public model endpoint. The image is pinned to Ollama 0.35.1 and
the model digest is saved in the run config. The first request downloads the
model into the persistent `rethinkmcts-ollama-models` Volume. The Function
scales down after 120 idle seconds; keeping it warm costs GPU time.

## Preparation

Check Modal billing method and Workspace budget in the dashboard. Keep the
machine awake and the local terminal connected while a batch is running.
Do not run two copies of the same run name concurrently.

```powershell
cd D:\ReThinkMCTS
.\venv\Scripts\python.exe -m modal token info
.\venv\Scripts\python.exe -m unittest discover -s tests -q
.\venv\Scripts\python.exe -m tools.modal_mcts.run --plan --dataset apps --workers 4
```

`--plan` does not deploy, download a model, or call GPU. With `--dataset apps`
it must report 300 APPS and 4 workers for the pinned `benchmark_v2` cohort.

## APPS L40S parallel run (new)

Run these commands in PowerShell from `D:\ReThinkMCTS`. The model digest is
the one recorded in the completed HumanEval L4 run. The wrapper verifies the
new deployment is L40S and refuses a different model digest before searching.

```powershell
$env:PYTHONIOENCODING = 'utf-8'
.\venv\Scripts\python.exe -m modal deploy tools/modal_mcts/inference.py
.\venv\Scripts\python.exe -m tools.modal_mcts.run --dataset apps --workers 4 --smoke `
  --expected-model-digest dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364
.\venv\Scripts\python.exe -m tools.modal_mcts.run --dataset apps --workers 4 --limit 4 `
  --expected-model-digest dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364 --confirm-full-run
.\venv\Scripts\python.exe -m tools.modal_mcts.run --dataset apps --workers 4 `
  --expected-model-digest dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364 --confirm-full-run
```

Inspect the smoke and four-problem pilot before the full command. Repeating
the full command resumes completed problems in this new run; interrupted
problems restart. Never run two batch processes against the same run at once.
The old run's APPS smoke is retained but is not copied to the new namespace.
The judge still executes generated code on the laptop, now up to four problems
at once. If that load is unacceptable, stop before the full step; changing
worker count requires another run name because `run_config.json` is immutable.

Once all 300 APPS are complete, combine them with the existing 164 HumanEval
artifacts without copying candidate files:

```powershell
.\venv\Scripts\python.exe -m rethinkmcts.benchmark `
  --run-name rethinkmcts_qwen25_modal_l40s_parallel_v1 `
  --humaneval-run-name rethinkmcts_qwen25_modal_v1 `
  --model qwen2.5-coder:7b-instruct
```

The finalizer checks matching search settings, model digest and cohort. It
records source run names and source/inference hashes per dataset in
`outputs/benchmarks/rethinkmcts_qwen25_modal_l40s_parallel_v1/qwen2.5-coder_7b-instruct/`.

Với run hiện tại chỉ có 297/300 APPS candidate, lệnh core finalizer bên trên
**phải từ chối**. Người dùng đã quyết định tính `0796`, `1033`, `1581` là
không pass. Lệnh báo cáo riêng (không gọi GPU, không tạo solution giả):

```powershell
.\venv\Scripts\python.exe -m tools.modal_mcts.adjudicate `
  --run-name rethinkmcts_qwen25_modal_l40s_parallel_v1 `
  --humaneval-run-name rethinkmcts_qwen25_modal_v1 `
  --model qwen2.5-coder:7b-instruct `
  --failed-apps 0796 1033 1581
```

Bang private-half lich su nam trong `adjudicated_v1/`. Bang final evaluation
toan bo APPS tests hien tai nam tai
`outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_qwen25_modal_benchmark_v2_all_tests/qwen2.5-coder_7b-instruct/benchmark_table.md`.
Chỉ 297 bài có private test report; ba bài adjudicated được tính 0 trong
macro Pass Rate/Pass@1, không thêm private tests giả vào micro denominator.

**Safety:** `Executors` use local subprocesses and timeouts, not a security
sandbox. Do not use this topology if generated code must be isolated from the
laptop. The alternative remote executor requires separate integration.
