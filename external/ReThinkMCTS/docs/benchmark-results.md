# Lưu trữ và so sánh kết quả benchmark

## Hai lớp artifact

1. `outputs/baselines/evaluations/<run>/<model>/`: kết quả chấm gốc do evaluator
   ghi, gồm `results.jsonl`, `results.csv`, `failures.csv`, `summary.json`,
   `evaluation.log` và bảng judge. Đây là dữ liệu làm việc, có thể được cập
   nhật khi resume hoặc chấm lại.
2. `outputs/benchmarks/<run>/<model>/`: **hồ sơ benchmark đã khóa** sau khi
   cả APPS và HumanEval hoàn tất, không có candidate thiếu hay `executor_error`.
   Không ghi đè hồ sơ nếu input, tham số hoặc kết quả thay đổi. Muốn thực nghiệm
   lại với timeout/model/seed khác, dùng run name mới.

Kết quả baseline **lịch sử 100+100** vẫn ở `outputs/baselines/evaluations/
qwen25_coder_7b_instruct_baseline_v1/`; không tự gán sang cohort `benchmark_v2`.
Direct baseline `benchmark_v2` đã chấm đủ 300+164 tại run hậu tố `_all_tests`;
xem `docs/results/benchmark-v2-all-tests.md`. Đây là bảng judge trong
working artifacts, chưa phải hồ sơ `outputs/benchmarks/` được đóng băng.
Hồ sơ chuẩn dưới đây chỉ áp dụng cho run mới 300 APPS + 164 HumanEval.
RethinkMCTS Modal có [báo cáo adjudicated](results/rethinkmcts-modal-benchmark-v2-adjudicated.md)
riêng cho 297 APPS candidate thật, 3 technical failure tính 0 và 164
HumanEval; không gọi đây là run sạch 300/300 candidate.

## Cây thư mục chuẩn

```text
outputs/benchmarks/
├── <run>/<model>/
│   ├── run.json                 # thông số, nguồn, hash, trạng thái, metrics
│   ├── candidates.csv           # 1 dòng/bài, hash solution + tham số generation
│   ├── benchmark_table.csv
│   ├── benchmark_table.md
│   ├── benchmark_summary.json
│   ├── apps/
│   │   ├── sample_manifest.json
│   │   ├── summary.json
│   │   ├── results.jsonl
│   │   ├── results.csv
│   │   ├── failures.csv
│   │   ├── evaluation.log
│   │   └── benchmark_metrics.json
│   └── humaneval/
│       └── ...
└── comparisons/<comparison_name>/
    ├── comparison.json
    ├── comparison.csv
    └── comparison.md
```

`run.json` có `schema_version`, `run_name`, `method`, `model`, `model_revision`
(nếu được xác minh khi đóng gói; nếu không là `null`), `provider`,
`source_generation_run`, ngày UTC và `status=complete`. Các nhóm chính:

| Nhóm | Nội dung |
|---|---|
| `cohorts` | Sample ID, seed, số bài, difficulty, SHA-256 của manifest và dữ liệu test |
| `generation_profiles` | Tập cấu hình thực tế của các candidate: prompt version, max tokens, temperature, top-p, reasoning effort, seed nếu có |
| `evaluation` | Split, workers, test-workers, timeout và phạm vi timeout, test policy, max-tests, thời lượng batch, hash manifest |
| `coverage` | Số bài kỳ vọng/đã chấm/thiếu/lỗi hạ tầng |
| `execution` | Site, backend, Docker image ID, CPU/RAM/process limit, Python version, OS, hash code evaluator |
| `metrics` | Bảng APPS theo mức khó/overall và HumanEval Pass@1 |
| `source_hashes` | Hash kết quả evaluator, bundle và candidate index; `source_fingerprint` khóa hồ sơ |

`candidates.csv` cho phép truy vết từng `problem_id`, mã SHA-256 của
`solution.py`, model trả lời, finish reason, số token, tham số generation và
trạng thái/pass count. Seed generation cũ không được ghi trong artifact sẽ là
`null`, không tự suy đoán lại. **Không lưu secret, prompt đầy đủ hay code candidate
trong hồ sơ benchmark.** Code và báo cáo execution gốc vẫn nằm ở artifact
generation/evaluation tương ứng.

Mỗi `evaluation.json` mới ghi `evaluation_provenance` (hash solution, timeout,
test-workers, max-tests). Bước đóng băng đối chiếu từng candidate với cấu hình
batch; resume từ timeout khác hoặc code đã bị sửa sẽ bị từ chối, tránh bảng
metric mang nhãn tham số sai. Khi đó cần chấm lại với cấu hình thống nhất rồi
mới tạo hồ sơ mới.

## Quy tắc hoàn tất và so sánh

Runner máy thuê tự tạo hồ sơ bằng `evaluation.benchmark_record` **sau** khi
evaluator và judge hoàn tất. Nếu thiếu ID, có `executor_error`, dùng manifest
khác hoặc `--max-tests`, bước đóng băng sẽ dừng; output thô vẫn giữ để sửa
và resume. Timeout do code brute-force là kết quả thất bại hợp lệ, không phải
lỗi hạ tầng. Cùng run name + fingerprint được đọc lại; input đổi thì bị từ
chối ghi đè.

Sau này khi có hai hồ sơ hoàn tất, so sánh:

```powershell
.\venv\Scripts\python.exe -m evaluation.compare_benchmarks `
  --name qwen_models_v1 `
  --records outputs/benchmarks/<run_1>/<model_1>/run.json `
            outputs/benchmarks/<run_2>/<model_2>/run.json
```

Lệnh từ chối so sánh nếu cohort, dữ liệu test, test policy, timeout hoặc
Python version khác nhau. Tham số generation và worker được hiển thị trong
bảng để giải thích chi phí/độ trễ nhưng không buộc giống nhau. Không dùng
bảng so sánh này để trộn kết quả 100+100 cũ với 300+164 mới.

## Chạy trên GPU thuê

[Runbook remote evaluation](runbooks/remote-evaluation.md) tạo bundle có code,
candidate và dữ liệu đúng cohort. Trên remote, `run.sh` giới hạn tài nguyên
Docker, lưu `worker.log`, tạo hồ sơ benchmark, rồi nén báo cáo để tải về.
Hồ sơ nằm **trên remote** trong lúc chạy; sau khi tải result archive về, xem
`outputs/benchmarks/<run>/<model>/benchmark_table.md` ở thư mục đã giải nén.

## Hồ sơ RethinkMCTS

Native MCTS dùng `outputs/rethinkmcts/<run>/<model>/<dataset>/<problem_id>/`
cho từng search (thought tree, candidate, public execution và private result).
`rethinkmcts.benchmark` chỉ đóng băng bảng khi đủ **300 APPS + 164 HumanEval**.
Hồ sơ cùng namespace `outputs/benchmarks/<run>/<model>/` gồm `run.json`,
`candidates.csv`, `benchmark_table.csv/.md`, `benchmark_summary.json` và mỗi
dataset có `sample_manifest.json`, `results.csv/.jsonl`, `benchmark_metrics.json`.
Các file `summary.json`, `failures.csv` và `evaluation.log` trong cây ví dụ
phía trên thuộc **baseline remote evaluator**, không thuộc hồ sơ MCTS.
MCTS `run.json` lưu config search, model digest, source/data/manifest hashes,
candidate solution hashes, policy public/private và metric. Xem
[runbook remote MCTS](runbooks/remote-mcts.md) để đóng gói, smoke và thu kết quả.

Run Modal L40S hiện có 297/300 APPS candidate thật. Theo adjudication đã chốt,
ba ID `0796`, `1033`, `1581` được tính 0 ở macro Pass Rate và Pass@1, nhưng
không tạo artifact giả và không được tính là đã chạy private tests. Báo cáo
riêng nằm dưới `outputs/benchmarks/<run>/<model>/adjudicated_v1/`, có trạng thái
`adjudicated_complete` và không thay thế bảng clean-complete của core finalizer.
Xem [báo cáo benchmark v2](results/rethinkmcts-modal-benchmark-v2-adjudicated.md).

APPS baseline và MCTS final solution đều chấm **toàn bộ** test. Nửa đầu chỉ
đóng vai trò public feedback trong MCTS search. HumanEval báo Pass@1 official
harness, không báo Pass Rate.
