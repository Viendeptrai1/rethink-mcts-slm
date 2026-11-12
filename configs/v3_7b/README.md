# Cấu hình v3: RethinkMCTS đúng thiết lập bài báo, nhiều model 7–9B

Bộ config này dùng cho đợt thực nghiệm mới (từ 11/2026), thay cho cấu hình 14B v1 (xem [../README.md](../README.md)). Mọi model dùng **cùng một file config**; chỉ đổi `model.model`, `model.base_url` và, với model có thinking, `model.extra_body`.

| File | Dùng cho |
|---|---|
| `apps_mcts.yaml` | RethinkMCTS trên APPS-300 (`prepared/apps_half`) |
| `apps_baseline.yaml` | Direct (`--solver direct`) và Best-of-16 (`--solver best_of_n --samples-n 16`, temperature 0,8) |
| `humaneval_mcts.yaml`, `humaneval_baseline.yaml` | Tương tự trên HumanEval-164 |
| `pilot_apps_mcts.yaml`, `pilot_apps_baseline.yaml` | Pilot trên 20 bài APPS **ngoài** cohort ([apps_pilot_20.json](../../data/cohorts/apps_pilot_20.json)) |

## Đối chiếu với bài báo

| Thiết lập | Bài báo / upstream | v3 | v1 (14B) |
|---|---|---|---|
| Ngân sách | 16 rollout | 16 rollout (`budget.max_rollouts`), rethink không tính vào | 16 lần sinh code, tính cả rethink, tối đa 16 vòng lặp |
| Rethink mỗi node | 1 (`max_think_times=2`) | 1 | 2 |
| Dừng sớm | Không | Không; phương án dừng sớm tính lại offline | Dừng khi pass public |
| Giới hạn token / lời gọi | Không | Chỉ là lưới an toàn (4 triệu token, 400 lời gọi) | 65.536 token, 64 lời gọi |
| Public test | Một nửa (`half`) | Một nửa số test **khác nhau** (`prepared/apps_half`) | 2 test đầu |
| Temperature | 0 | 0 (Best-of-16: 0,8) | 0,2–0,6 |
| Critic | Thang [-1, 1], có thought | Như bài báo | Prompt [-1, 1] nhưng không có tác dụng vì dừng sớm |
| Block analysis | Nhận xét từng block, đưa vào feedback | Như bài báo; nếu không parse được thì giữ nguyên văn | Bị bỏ hoàn toàn |
| Rethink thấy thought cần sửa | Có | Có | Không |

Điểm lệch còn lại (ghi trong `experiment.deviations`): model mở 7–9B chạy bf16 trên vLLM; trace trong prompt giới hạn 32 lượt block; giới hạn an toàn 3600 giây mỗi bài; sandbox là subprocess trên máy chạy.

## Model

| Tên ngắn | Hugging Face ID | Ghi chú triển khai (kiểm tra ở pilot) |
|---|---|---|
| `qwen25c7b` | `Qwen/Qwen2.5-Coder-7B-Instruct` | Không có thinking |
| `seedcoder8b` | `ByteDance-Seed/Seed-Coder-8B-Instruct` | Không có thinking, context 32K |
| `qwen35_9b` | `Qwen/Qwen3.5-9B` | Thinking bật mặc định: `--set 'model.extra_body={chat_template_kwargs: {enable_thinking: false}}'`. Có encoder ảnh. Cần vLLM đủ mới |
| `granite42_8b` (dự phòng) | `ibm-granite/granite-4.2-8b` | Thinking bật mặc định; cách tắt cần xác nhận trên model card |

## Lệnh chạy

Triển khai endpoint (**tốn credit**, chỉ chạy khi đã quyết định):

```bash
MODAL_APP_NAME=rethink-qwen25c7b VLLM_MODEL_ID=Qwen/Qwen2.5-Coder-7B-Instruct VLLM_GPU=L40S \
VLLM_PIP_SPEC=vllm==0.31.0 VLLM_ENFORCE_EAGER=0 MODAL_MAX_INPUTS=64 VLLM_MAX_MODEL_LEN=32768 \
modal deploy deploy/modal_vllm.py
# Song song: ngắt app khi chạm trần credit hoặc thời gian
MODAL_APP_NAME=rethink-qwen25c7b MODAL_MAX_CREDIT=25 MODAL_MAX_HOURS=2 python3 scripts/modal_spending_guard.py
```

Chạy benchmark (mỗi model × phương pháp × dataset một thư mục riêng):

```bash
M=Qwen/Qwen2.5-Coder-7B-Instruct; E=https://<workspace>--rethink-qwen25c7b-serve.modal.run/v1
python3 scripts/run_benchmark_batch.py --config configs/v3_7b/apps_mcts.yaml \
  --output-dir runs/v3_apps_qwen25c7b_mcts --workers 8 \
  --set model.base_url=$E --set model.model=$M
python3 scripts/run_benchmark_batch.py --config configs/v3_7b/apps_baseline.yaml --solver best_of_n --samples-n 16 \
  --output-dir runs/v3_apps_qwen25c7b_bon16 --workers 8 \
  --set sampling.code.temperature=0.8 --set sampling.code.top_p=0.95 --set model.base_url=$E --set model.model=$M
```

**Chạy trên Colab:** `deploy/colab/` (`orchestrate.sh` chạy trên máy cá nhân: xin phiên A100, upload code, giữ kernel bận, tải kết quả về rồi tắt phiên; `run_plan.sh` chạy trên VM; kế hoạch sinh bằng `make_plans.py`). Thông số chạy song song (16 worker, `test_workers=4`, `max_test_processes=8`) đã kiểm chứng ở pilot P2b, xem [BENCHMARK_LEDGER.md](../../docs/results/BENCHMARK_LEDGER.md) mục 11.

**Phiên bản Python:** solver, trace và sandbox phải chạy Python 3.11. Với Python 3.13, 3 test về trace fail: hàm đệ quy bị bỏ sót lượt chạy, làm block feedback thiếu dữ liệu mà không báo lỗi. vLLM là tiến trình riêng nên dùng Python nào cũng được. Trước mỗi đợt chạy, phải chạy `pytest` bằng đúng interpreter sẽ dùng.

`--workers` là số bài chạy đồng thời trong một process. Kết quả không phụ thuộc vào giá trị này, nhưng thời gian mỗi bài thì có, vì các bài dùng chung CPU để chạy test. Nên đặt thấp hơn số nhân CPU (máy hiện tại có 8 nhân) và ghi lại giá trị đã dùng.

## Kế hoạch pilot

Pilot chỉ dùng 20 bài APPS **ngoài** cohort (APPS test id 0–49, đều ở mức interview). Số liệu pilot **không bao giờ** được báo cáo như kết quả. HumanEval không có tập ngoài nên chỉ chạy 3 bài để kiểm tra định dạng, và không chỉnh gì dựa trên việc các bài đó pass hay fail.

| Bước | Nội dung | Mục đích |
|---|---|---|
| P1 | `qwen25c7b`, MCTS, `--limit 3 --workers 3` | Smoke test: artifact đầy đủ, không lỗi template |
| P2 | `qwen25c7b`, 20 bài × MCTS, Best-of-16, Direct, `--workers 8` | Đo token, thời gian, chi phí; chọn số worker |
| P3 | `seedcoder8b`, `qwen35_9b`: 5 bài × MCTS, Direct; HumanEval 3 bài | Định dạng JSON, tắt thinking, tốc độ |
| P4 (tùy chọn) | `qwen25c7b` trên L4: 5 bài × Direct, MCTS | So token/giây và $/bài giữa L4 và L40S |

Sau mỗi bước chạy `python3 scripts/pilot_report.py runs/<run> ...`. Lấy số giây GPU từ `modal billing report --show-resources` rồi truyền `--gpu-seconds` để ước tính chi phí 300 bài.

**Tiêu chí đạt** trước khi chạy thật:
1. Không có lỗi template (`strict_variables`) và tối đa 1/20 bài lỗi kỹ thuật.
2. `block_analysis_in_feedback_pct` ≥ 90%.
3. `mean_rollouts` = 16, trừ bài hết việc trên cây; `max_depth_distribution` có bài đạt độ sâu ≥ 3.
4. `finish_reasons.length` ≤ 5% số lời gọi; `think_leaks` = 0.
5. Không bài nào chạm giới hạn 3600 giây. Nếu có, giảm `--workers` hoặc xem lại GPU.
6. Ước tính chi phí cho model × dataset × phương pháp nằm trong credit còn lại.

Khi đạt cả 6 tiêu chí: đóng băng commit, prompt và config, ghi protocol vào [PROTOCOL.md](../../docs/research/PROTOCOL.md), rồi mới chạy cohort thật. Nếu phải sửa gì sau pilot thì chạy lại pilot.
