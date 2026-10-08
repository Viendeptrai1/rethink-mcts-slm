# RethinkMCTS benchmark v2: APPS private-half (đã bị thay thế)

> Kết quả này chỉ chấm nửa sau APPS tests. Không dùng làm bảng benchmark cuối.
> Bảng đúng chấm toàn bộ tests nằm tại `docs/results/benchmark-v2-all-tests.md`.

Trạng thái: **adjudicated**, không phải một run có đủ 464 candidate thực thi.
Kiểm tra artifact ngày 2026-10-04. Kết quả này không phải direct-generation
baseline và không được đổi nhãn thành kết quả chạy sạch 300/300 APPS.

## Bảng chính

| Nhóm | Pass Rate (%) | Pass@1 (%) |
|---|---:|---:|
| APPS Intro. | 27.93 | 20.00 |
| APPS Inter. | 16.23 | 7.00 |
| APPS Comp. | 8.28 | 4.00 |
| APPS Overall | 17.48 | 10.33 |
| HumanEval | N/A | 91.46 |

APPS có 100 bài mỗi độ khó. `Pass Rate` là trung bình tỷ lệ test pass theo
từng bài trên **300 bài**; `Pass@1` là số bài pass toàn bộ private tests trên
300 bài. Có 31/300 APPS pass toàn bộ; HumanEval 150/164 pass official harness.

## Ba bài được tính không pass

| APPS ID | Difficulty | Trạng thái cuối | Bằng chứng |
|---|---|---|---|
| `0796` | interview | Windows file lock | 2 failed attempts, `.executor-stderr` bị giữ bởi process khác |
| `1033` | interview | Search timeout | 2 attempts vượt giới hạn 900 giây trước khi có candidate hoàn chỉnh |
| `1581` | interview | Windows file lock | 2 failed attempts, `.executor-stderr` bị giữ bởi process khác |

Ba bài trên **không có `final_solution.py` và không có private test report**.
Theo quyết định của người dùng, chúng được gán 0 cho macro Pass Rate và Pass@1.
Không được tuyên bố `0/n` private tests đã thực thi. Vì vậy micro Pass Rate
quan sát là `436/3026 = 14.41%`, chỉ tính test thật của 297 APPS có candidate;
micro không phải metric chính trong bảng.

## Provenance

- APPS: `rethinkmcts_qwen25_modal_l40s_parallel_v1`, 297/300 candidate hoàn chỉnh,
  Modal L40S tối đa 4 replica, batch 4 worker, judge trên Windows laptop.
- HumanEval: `rethinkmcts_qwen25_modal_v1`, 164/164 candidate hoàn chỉnh,
  Modal L4, batch 1 worker, judge trên cùng máy.
- Cả hai dùng `qwen2.5-coder:7b-instruct`, digest
  `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`,
  cùng search settings và cohort `data/samples/benchmark_v2/`.
- Search: 2 rollouts, width 3, `max_rethink_times=2`, temperature 0.2,
  top-p 0.95, public APPS nửa đầu tests, private APPS nửa sau; HumanEval
  official harness chỉ chấm final candidate.
- Mỗi ID adjudicated có attempt count, latest status, error và SHA-256
  của attempt log trong `run.json`. Source config, cohort/data và toàn bộ
  candidate thật đều được kiểm tra/hash lúc tạo báo cáo.

## Artifact

`outputs/benchmarks/rethinkmcts_qwen25_modal_l40s_parallel_v1/qwen2.5-coder_7b-instruct/adjudicated_v1/`:

- `benchmark_table.md/.csv`: bảng chính.
- `benchmark_summary.json`: metric từng nhóm và manifest.
- `run.json`: provenance, coverage, chính sách adjudication, log hashes.
- `apps/results.csv/.jsonl`, `humaneval/results.csv/.jsonl`: 464 hàng để audit.
- `candidates.csv`: chỉ mục candidate thật và ba hàng failure không có artifact.

Core finalizer `rethinkmcts.benchmark` vẫn từ chối cohort thiếu candidate theo
thiết kế. Báo cáo này được tạo riêng bằng `tools.modal_mcts.adjudicate`, không
ghi file giả vào run MCTS và không sửa source code do model sinh.
