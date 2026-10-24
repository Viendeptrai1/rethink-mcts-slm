# GPU thuê CKEY

**Instance ghi trong tài liệu này đã hết hạn.** Host và port bên dưới chỉ là
lịch sử, không dùng làm lệnh kết nối mới. Khi thuê lại, điền endpoint mới theo
[runbook remote evaluation](../runbooks/remote-evaluation.md) và kiểm tra Docker
trước khi chạy code do LLM sinh.

Đối với **generation mới**, dùng [runbook tự kéo model](../runbooks/gpu-generation.md):
chạy một lệnh từ Windows, tự kiểm tra/tải Ollama qua SSH tunnel. Phần remote
evaluation của `benchmark_v2` chỉ cần CPU và **không tải model**.
RethinkMCTS cần **cả** Ollama trên GPU lẫn CPU executor trên cùng máy; xem
[runbook remote MCTS](../runbooks/remote-mcts.md), không dùng bundle evaluation
của baseline cho search.

## Benchmark đã hoàn thành

Sau khi instance CKEY hoat dong, benchmark duoc chot nhu sau:

- Model: `qwen2.5-coder:7b-instruct`.
- APPS: 100 bài test trong `data/samples/evaluation_v1/apps_test_100.json`.
- HumanEval: 100 bài test trong `data/samples/evaluation_v1/humaneval_test_100.json`.
- Run: `qwen25_coder_7b_instruct_baseline_v1`.
- Generation: bat dau `--generation-workers 1`; chi tang len 2 neu Ollama on dinh.
- MCTS về sau dùng hai manifest `benchmark_v2` (300 APPS + 164 HumanEval),
  không sample lại; hai dòng 100 bài ở trên là kết quả lịch sử.

Lenh generation/evaluation chinh thuc nam trong `baselines/README.md` va
`docs/pipeline-direct.md`.

Generation full đã hoàn thành. Các lệnh bên dưới là runbook tái lập hoặc kiểm tra
instance, không phải trạng thái đang chạy.

Tài liệu vận hành instance GPU thuê dùng cho direct-generation baseline. Đây là
thông tin của instance hiện tại, không phải cấu hình cố định cho mọi lần thuê GPU.

## Trạng thái hiện tại

- Nhà cung cấp: CKEY.VN, dịch vụ GPU3.
- Trạng thái lúc ghi nhận: hoạt động, khởi tạo xong; **hiện đã hết hạn**.
- Image: `chieustudio/openwebui-ollama-ubuntu:latest`.
- Khu vực: UA.
- GPU: `1x RTX 3090 - 24 GB`.
- CPU: `4/8 vCPU`.
- RAM: `64 GB`.
- Storage: khoảng `6923 GB`.
- Giá ghi nhận: khoảng `7.643 VND/giờ`.
- Model dự kiến: `qwen2.5-coder:7b-instruct` trên Ollama.

Không ghi username/password, token hoặc secret vào tài liệu này.

## Endpoint và port mapping của instance cũ (không dùng lại)

| Mục đích | Endpoint bên ngoài | Port trong GPU |
|---|---|---:|
| SSH | `ssh root@n2.ckey.vn -p 2797` | `22` |
| TTYD | `http://n2.ckey.vn:2798` | `7681` |
| Open WebUI | `http://n2.ckey.vn:2799` | `8080` |
| Ollama API | `http://n2.ckey.vn:2800` | `11434` |

Benchmark nên chạy trực tiếp trên GPU thuê và gọi Ollama qua
`http://127.0.0.1:11434`. Không cần expose thêm port Ollama public khi pipeline
chạy cùng máy. Nếu cần gọi từ Windows, ưu tiên SSH tunnel thay vì mở API không có
authentication.

## Kế hoạch runtime cũ (tham khảo)

1. Chờ instance chuyển sang `Hoạt động`.
2. SSH vào máy bằng port `2797`.
3. Kiểm tra GPU bằng `nvidia-smi`.
4. Kiểm tra Ollama bằng `ollama list`.
5. Tải model trên chính GPU thuê nếu chưa có:

   ```bash
   ollama pull qwen2.5-coder:7b-instruct
   ```

6. Smoke test một request trước khi chạy benchmark.
7. Chạy generation với `generation-workers=1`, sau đó mới tăng lên `2`.
8. Chạy evaluation sau khi generation hoàn tất.

Model đã có trên Ollama Windows không tự động xuất hiện trên instance CKEY. Không
cần copy blob trong thư mục `.ollama`; dùng `ollama pull` trên GPU thuê để Ollama
tự tải đúng model và metadata.

## Cấu hình project dự kiến

Provider Ollama sẽ dùng OpenAI-compatible API khi pipeline chạy trên GPU:

```env
LLM_PROVIDER=ollama
LLM_BASE_URL=http://127.0.0.1:11434/v1
LLM_MODEL=qwen2.5-coder:7b-instruct
LLM_API_KEY=ollama
```

Modal vẫn được giữ như provider cũ, nhưng không dùng cho benchmark GPU này. Các
biến môi trường thật không được commit hoặc ghi vào log.

Ở instance cũ, nếu chạy pipeline từ Windows, endpoint public từng được map
như sau; **không dùng endpoint này cho instance mới**:

```env
LLM_BASE_URL=http://n2.ckey.vn:2800/v1
```

Khuyến nghị vẫn là copy project và chạy benchmark trực tiếp trên GPU để tránh phụ
thuộc mạng public.

## Smoke test trên GPU

```bash
nvidia-smi
ollama list
ollama run qwen2.5-coder:7b-instruct
curl http://127.0.0.1:11434/api/tags
```

Provider Ollama đã được tích hợp vào native search. Smoke test sẽ chạy một bài APPS
và một bài HumanEval, kiểm tra `response.txt`, `solution.py`, `metadata.json` và
`events.jsonl` trước khi chạy batch lớn.

## Quy mô benchmark cho run mới

- Generation: chay full APPS 5.000 bai va HumanEval 164 bai.
- Judge evaluation: 300 APPS + 164 HumanEval theo hai manifest trong
  `data/samples/benchmark_v2/`. Chưa chạy trên cohort này.
- Generation: bắt đầu với 1 worker, tối đa 2 worker sau khi xác nhận GPU ổn định.
- `max_tokens`: đặt giới hạn hữu hạn, khuyến nghị ban đầu `8192` hoặc `16384` cho
  Qwen2.5:7B; không dùng `null` trong smoke test.

## Lệnh HumanEval

Sau khi project và dataset đã có trên GPU, từ root project:

```bash
source venv/bin/activate
python -m pipelines \
  --stage generate \
  --dataset humaneval \
  --run-name qwen25_7b_humaneval_v1 \
  --config baselines/direct_generation/configs/qwen25_7b_ollama.json \
  --generation-workers 1 \
  --delay 2 \
  --plan
```

Smoke test hai bài trước:

```bash
python -m pipelines \
  --stage generate \
  --dataset humaneval \
  --run-name qwen25_7b_humaneval_smoke \
  --config baselines/direct_generation/configs/qwen25_7b_ollama.json \
  --limit 2 \
  --generation-workers 1 \
  --delay 2
```

Full HumanEval sau khi smoke test thành công:

```bash
python -m pipelines \
  --stage generate \
  --dataset humaneval \
  --run-name qwen25_7b_humaneval_v1 \
  --config baselines/direct_generation/configs/qwen25_7b_ollama.json \
  --generation-workers 1 \
  --delay 2 \
  --confirm-full-run
```

Chấm candidate sau generation:

```bash
python -m pipelines \
  --stage evaluate \
  --dataset humaneval \
  --run-name qwen25_7b_humaneval_v1 \
  --workers 2 \
  --confirm-full-run
```

## Checklist trước khi tắt GPU

- Đã lưu candidate, manifest và evaluation output về workspace hoặc remote storage.
- Đã kiểm tra `summary.json` và log lỗi.
- Đã dừng Ollama/process benchmark.
- Đã xác nhận không còn dữ liệu cần giữ trên instance.
- Chỉ tắt instance sau khi hoàn tất copy dữ liệu vì GPU bị xóa có thể làm mất disk.
