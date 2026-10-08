# Direct baseline benchmark v2: APPS private-half (đã bị thay thế)

> Kết quả này chỉ chấm nửa sau APPS tests. Không dùng làm bảng benchmark cuối.
> Bảng đúng chấm toàn bộ tests nằm tại `docs/results/benchmark-v2-all-tests.md`.

Trạng thái: **đã chấm đủ 464/464 candidate**, không có `missing_candidate`
hoặc `executor_error`. Kiểm tra ngày 2026-10-04.

## Bảng chính

| Nhóm | Pass Rate (%) | Pass@1 (%) |
|---|---:|---:|
| APPS Intro. | 45.55 | 32.00 |
| APPS Inter. | 26.54 | 9.00 |
| APPS Comp. | 17.85 | 5.00 |
| APPS Overall | 29.98 | 15.33 |
| HumanEval | N/A | 80.49 |

APPS có 100 bài mỗi độ khó; tổng cộng 46/300 bài pass toàn bộ private
tests. HumanEval có 132/164 bài pass official harness. APPS Pass Rate là
macro mean của tỷ lệ pass từng bài; Pass@1 dùng mẫu số đủ 300/164 bài.

## Phương pháp và provenance

- Model yêu cầu: `qwen2.5-coder:7b-instruct`. Solution được tái sử dụng từ
  direct-generation run `qwen25_coder_7b_instruct_baseline_v1` qua Ollama
  trên CKEY; lượt này **không gọi LLM**, không sửa solution.
- Cohort cố định: `data/samples/benchmark_v2/apps_test_300.json` và
  `humaneval_test_164.json`.
- APPS judge dùng nửa sau test cases (private half) và timeout 5 giây/test.
  HumanEval judge dùng official harness, timeout 5 giây.
- Chấm trên CPU máy Windows cục bộ. APPS chạy tối đa 4 candidate worker,
  riêng bài `3886` retry với 1 worker sau lỗi Windows khóa file tạm.
  Lần retry có 2/16 private tests pass và timeout; không tính là lỗi hạ tầng.
- Evaluation run: `qwen25_coder_7b_instruct_baseline_benchmark_v2`, tách
  khỏi evaluation lịch sử 100+100.
- MCTS paired cohort dùng Modal và APPS có 3 bài được adjudicate 0 do thiếu
  candidate. Cùng ID/policy chấm không có nghĩa là cùng hạ tầng sinh code;
  không suy diễn chênh lệch là hiệu ứng MCTS thuần túy.

## Artifact

`outputs/baselines/evaluations/qwen25_coder_7b_instruct_baseline_benchmark_v2/qwen2.5-coder_7b-instruct/`:

- `benchmark_table.md/.csv`, `benchmark_summary.json`: bảng và metric tổng hợp.
- `apps/`, `humaneval/`: `results.jsonl`, `summary.json`, `evaluation.log`,
  `evaluation_config.json` và báo cáo từng candidate trong `candidates/`.
- File `evaluation_config.json` khóa source run, timeout, test policy và
  SHA-256 của manifest để resume không trộn chính sách chấm.

Bảng lịch sử 100+100 ở run `qwen25_coder_7b_instruct_baseline_v1` vẫn giữ nguyên.
