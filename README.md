# RethinkMCTS cho mô hình ngôn ngữ nhỏ

Tiểu luận chuyên ngành (TLCN): cài đặt lại **RethinkMCTS** ([arXiv:2409.09584](Rethink.pdf)), một phương pháp tìm kiếm cây Monte Carlo trên mức "suy nghĩ" (thought) có dùng phản hồi thực thi để sinh mã nguồn, rồi kiểm chứng trên nhiều model mở 7–9B. Tên đề tài theo [Proposal.md](Proposal.md).

## Trạng thái

- **Protocol hiện hành: v3.1**. Thiết lập theo bài báo: 16 rollout, 1 rethink mỗi node, critic trong [-1, 1], không dừng sớm. Chi tiết ở [docs/research/PROTOCOL.md](docs/research/PROTOCOL.md) mục 8 và [configs/v3_7b/README.md](configs/v3_7b/README.md).
- **Model:** Qwen2.5-Coder-7B-Instruct, Seed-Coder-8B-Instruct, Qwen3.5-9B (tắt thinking). Chạy vLLM 0.31.0, bf16, trên A100-SXM4-40GB.
- **Baseline:** Direct (temperature 0) và Best-of-16 (temperature 0,8, chọn theo public test).
- **Dữ liệu:** APPS-300 (cohort cố định [data/cohorts/apps_benchmark_300.json](data/cohorts/apps_benchmark_300.json), public test là một nửa số test) và HumanEval-164.
- **Nguồn số liệu duy nhất:** [docs/results/BENCHMARK_LEDGER.md](docs/results/BENCHMARK_LEDGER.md) và [docs/results/v3/](docs/results/v3/). Mọi kết quả trước v3 đã được gỡ khỏi nhánh, lưu ở tag `archive/pre-v3-2026-11-13`, và không dùng cho kết luận.
- Quyết định nghiên cứu: [docs/research/DECISION_LOG.md](docs/research/DECISION_LOG.md). Khung báo cáo: [docs/report/KHUNG_BAO_CAO_v2.md](docs/report/KHUNG_BAO_CAO_v2.md). Rà soát gần nhất: [docs/RA_SOAT_2026-11-13.md](docs/RA_SOAT_2026-11-13.md).

## Cài đặt

```bash
python3.11 -m venv .venv && source .venv/bin/activate   # solver cần Python 3.11 (3.13 làm sót sự kiện trace)
pip install -e ".[dev]"
python3 -m pytest -q        # 2 test cần Docker image rethink-worker:py311 (docker build -t rethink-worker:py311 deploy/sandbox)
```

## Dùng nhanh

```bash
rethink doctor  --config configs/smoke_mock.yaml
rethink solve   --config configs/smoke_mock.yaml --problem tests/fixtures/watermelon_public.json --output-dir runs/smoke_demo
rethink judge   --run runs/smoke_demo --hidden tests/fixtures/watermelon_hidden.json
rethink prepare --dataset apps --raw-path data/apps/apps_300.jsonl --output prepared/apps_half --public-split half
python3 scripts/run_benchmark_batch.py --config configs/v3_7b/apps_mcts.yaml --output-dir runs/x --dry-run
```

Chạy benchmark thật cần một endpoint vLLM và tốn credit. Xem [configs/v3_7b/README.md](configs/v3_7b/README.md), [deploy/colab/v31_campaign/README.md](deploy/colab/v31_campaign/README.md) (Colab) và [deploy/modal_v31_runner.py](deploy/modal_v31_runner.py) (Modal).

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `src/rethink_mcts/` | Code chính, kiến trúc ports and adapters: `domain/`, `policies/` (P-UCB, Max backup, reward dual), `application/` (search, feedback, baseline, judge, benchmark), `adapters/` (LLM, thực thi, dữ liệu) |
| `prompts/native_v3/` | Prompt của protocol v3 |
| `configs/v3_7b/` | Config của protocol v3.1 |
| `prepared/` | Dữ liệu đã chuẩn hóa (`apps_half`, `apps_pilot_half`, `humaneval`), gồm public test và suite hidden riêng |
| `runs/v3_*` | Artifact của từng run (manifest, kết quả từng bài, chương trình được chọn). File nặng được nén trong `runs/v3_raw_archives/` |
| `scripts/` | `run_benchmark_batch.py`, `analyze_v3.py`, `pilot_report.py`, `pilot_gate.py`, `modal_spending_guard.py` |
| `deploy/` | Colab (`colab/`), Modal (`modal_v31_runner.py`), sandbox Docker (`sandbox/`) |
| `docs/` | `research/` (quyết định, protocol), `results/` (ledger, phân tích v3), `report/` (khung báo cáo), `architecture.md` |
