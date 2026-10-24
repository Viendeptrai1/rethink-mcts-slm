# Tools

Các script trong thư mục này hỗ trợ kiểm tra và vận hành quanh pipeline chính;
logic generation/judge vẫn nằm ở `baselines/` và `evaluation/`.

## `gpu/run_generation.py`

Entry point direct generation qua SSH tunnel tới Ollama trên GPU thuê. Tự pull
model nếu thiếu rồi gọi `pipelines --stage generate` tại máy Windows; dataset
và artifact ở workspace cục bộ. Xem
[runbook GPU generation](../docs/runbooks/gpu-generation.md). Không dùng khi
chỉ chấm benchmark v2.

## `remote_evaluation/`

Đóng gói candidate cohort và chạy evaluator bằng CPU/Docker trên máy thuê.
Không gọi Ollama; xem [runbook](../docs/runbooks/remote-evaluation.md).

## `remote_mcts/`

Đóng gói source + cohort 300 APPS/164 HumanEval, chạy native search trong
Docker trên máy thuê, tự kiểm tra/pull Ollama model, lưu checkpoint cấp bài và
đóng bảng benchmark khi đủ cohort. Có gọi LLM và chấm code trong search.
Xem [runbook](../docs/runbooks/remote-mcts.md).

## `smoke_modal.py`

Gọi thử một request Modal theo biến môi trường cũ. Benchmark hiện tại dùng Ollama
trên GPU CKEY và chạy qua `pipelines`, vì vậy script này chỉ giữ cho việc kiểm tra
provider Modal lịch sử.

Không ghi secret vào file hoặc commit `.env`.
