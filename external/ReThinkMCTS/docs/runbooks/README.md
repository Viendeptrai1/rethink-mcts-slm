# Runbook scope (2026-09-27)

Direct baseline đã hoàn tất với model `qwen2.5-coder:7b-instruct` qua Ollama.
Native RethinkMCTS đã có batch cohort `benchmark_v2/` và artifact riêng dưới
`outputs/rethinkmcts/`; đã hoàn tất HumanEval 164 trên Modal L4, APPS tạm dừng.

# Runbooks

Runbook là các lệnh thao tác có thể copy/chạy trực tiếp. Root
[README.md](../../README.md) là điểm vào chính; file này chỉ lập bản đồ thao tác.

## Runbook hiện tại

- [Full direct baseline](baseline-full.md): generation full, evaluation sample cố
  định 100+100 lịch sử và benchmark judge.
- [Benchmark v2](benchmark-v2.md): cohort cố định APPS 300 + HumanEval 164;
  gồm lệnh paired direct baseline dùng lại solution cũ, không gọi LLM.
- [Remote evaluation](remote-evaluation.md): đóng gói cohort, chạy worker trong
  Docker trên máy thuê và tải báo cáo về; chưa triển khai lên instance mới.
- [GPU generation](gpu-generation.md): một lệnh từ Windows mở SSH tunnel, tự
  tải Ollama model nếu thiếu rồi chạy direct generation; không dùng cho judge.
- [RethinkMCTS smoke](rethinkmcts-smoke.md): test native offline và smoke một bài
  HumanEval/APPS sau khi duyệt output.
- [Remote MCTS](remote-mcts.md): đóng gói đúng 300+164, Docker/Ollama trên GPU
  thuê, smoke hai bài, resume và thu bảng. Chưa chạy thật.
- [Modal MCTS](modal-mcts.md): APPS run mới dùng tối đa 4 Modal L40S replica
  và 4 problem worker; HumanEval L4 lịch sử được giữ riêng. Plan, deploy,
  smoke, pilot rồi mới full/resume; judge vẫn trên laptop.

## Thứ tự vận hành

1. Đọc `docs/project-status.md` và kiểm tra `.env`/provider trong
   [llm-provider.md](../llm-provider.md).
2. Với direct baseline, chạy `--plan` trước batch lớn.
3. Với native RethinkMCTS, chạy unit test offline và `--plan` trước provider smoke.
4. Generation full không truyền `--sample-file`.
5. Run lịch sử dùng `data/samples/evaluation_v1/`; run mới dùng
   `data/samples/benchmark_v2/` (APPS 300 + HumanEval 164).
6. Judge chỉ chạy sau khi cả APPS và HumanEval có `results.jsonl`.

## Quy tắc resume

- Generation mặc định skip artifact hoàn chỉnh.
- Evaluation mặc định skip candidate đã có `evaluation.json`.
- Không dùng `--no-resume` nếu chỉ muốn chạy tiếp.
- Không chạy hai evaluator cùng lúc trên cùng run/model.
- MCTS batch skip bài đã hoàn tất; bài dở làm lại, attempt cũ được giữ.
- `outputs/` là artifact tự động; không sửa `solution.py` để làm thay đổi metric.
