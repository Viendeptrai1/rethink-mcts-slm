# Chấm benchmark trên máy GPU thuê (CPU worker)

## Trạng thái và điều kiện

Workflow này đã được chuẩn bị **offline**; chưa triển khai lên CKEY vì instance
cũ đã hết hạn. Chỉ cần điền host/SSH port của instance mới sau khi bạn gửi.
Máy thuê chạy evaluator bằng CPU, không cần GPU cho bước chấm. Cấu hình ban
đầu dành cho máy cũ 4/8 vCPU, 64 GB RAM: 2 candidate workers, 1 APPS test
worker, giới hạn container 4 CPU/12 GB RAM. Không chạy generation Ollama nặng
cùng lúc nếu muốn kết quả thời gian ổn định.

Yêu cầu trên máy thuê: Docker daemon hoạt động, quyền dùng Docker, Python 3
hoặc `unzip`, và mạng để build image/lấy package. Một số template CKEY chạy
trong container **có thể không cho chạy Docker bên trong**; kiểm tra trước.
Không có Docker thì `run.sh` sẽ dừng. **Không chạy candidate trực tiếp bằng
Python trên host GPU** để né bước này.

## 1. Đóng gói tại Windows

Không gọi LLM, không chuyển `.env`, dataset train, hay toàn bộ 5.000 bài APPS.
Script chọn candidate hoàn chỉnh mới nhất thuộc đúng manifest `benchmark_v2`
từ run generation cũ, chép 300 file test APPS cần chấm và HumanEval Arrow. Các
artifact/chấm cũ không được copy, run name mới tránh ghi đè.

```powershell
cd D:\ReThinkMCTS
.\venv\Scripts\python.exe -m tools.remote_evaluation.prepare_bundle `
  --source-run qwen25_coder_7b_instruct_baseline_v1 `
  --remote-run qwen25_coder_7b_instruct_benchmark_v2 `
  --model qwen2.5-coder:7b-instruct `
  --provider ollama `
  --archive outputs/remote_evaluation/qwen25_coder_7b_instruct_benchmark_v2.zip
```

Script báo số candidate và từ chối nếu thiếu. `--allow-missing` chỉ dành cho
audit từng phần, không dùng cho báo cáo benchmark đầy đủ.
Nếu có digest trọng số model đã xác minh từ lúc sinh code, thêm
`--model-revision <digest>`; nếu không, hồ sơ ghi `null`, không tự đoán từ
model đang được cài trên GPU thuê mới.

## 2. Chuyển sang instance mới

Thay `<HOST>` và `<SSH_PORT>` bằng thông tin instance mới. **Không dùng lại
`n2.ckey.vn:2797` nếu instance đó đã hết hạn.**

```powershell
scp -P <SSH_PORT> `
  outputs/remote_evaluation/qwen25_coder_7b_instruct_benchmark_v2.zip `
  root@<HOST>:/root/
ssh root@<HOST> -p <SSH_PORT>
```

Trên terminal Linux của máy thuê:

```bash
docker info
mkdir -p /root/rethink_eval_v2
python3 -m zipfile -e /root/qwen25_coder_7b_instruct_benchmark_v2.zip /root/rethink_eval_v2
cd /root/rethink_eval_v2
bash tools/remote_evaluation/run.sh --plan
```

`--plan` build Docker image và chỉ đếm candidate, **không chấm code**. Xác
nhận `apps=300` và `humaneval=164` trong `bundle.json` và plan trước khi chạy:

```bash
bash tools/remote_evaluation/run.sh --workers 2 --apps-timeout 2 --humaneval-timeout 5
```

Runner chấm APPS rồi HumanEval, sau đó gọi judge tổng hợp và đóng băng hồ sơ
`outputs/benchmarks/<run>/<model>/`; xem [schema báo cáo](../benchmark-results.md).
Resume mặc định bỏ
qua `evaluation.json` đã hoàn tất; nếu SSH đứt, kết nối lại và chạy đúng lệnh
trên với **cùng timeout và cấu hình**. Nếu đổi timeout sau khi đã chấm một
phần, hồ sơ benchmark sẽ từ chối kết quả trộn cấu hình; cần chấm lại thống nhất
trong run mới. Giới hạn thời gian là **mỗi test APPS** hoặc **cả harness HumanEval**,
chưa phải timeout tổng cho một bài APPS. Log tiến trình được nối vào
`outputs/remote_evaluation/worker.log`; artifact lưu dưới
`outputs/baselines/evaluations/` và cạnh candidate.

Container chạy UID không đặc quyền, mạng tắt, root filesystem chỉ đọc, giới
hạn CPU/RAM/process và chỉ cho ghi vào `outputs/`. Đây là cô lập **cả batch**,
chưa phải sandbox riêng cho từng test: code do LLM sinh vẫn có thể đọc dữ liệu
test và thay đổi các artifact trong `outputs/` của cùng container. Không xem
nó là hệ thống judge chống gian lận hay bảo đảm bảo mật tuyệt đối. Tuyệt đối
không đưa `.env`, SSH key hoặc token vào bundle.

## 3. Thu hồi kết quả

Sau khi chạy xong, runner tạo:

```text
/root/rethink_eval_v2/outputs/remote_evaluation/
  qwen25_coder_7b_instruct_benchmark_v2_qwen2.5-coder_7b-instruct_results.zip
```

Trên Windows, tải về vào thư mục tách biệt với benchmark lịch sử:

```powershell
scp -P <SSH_PORT> `
  root@<HOST>:/root/rethink_eval_v2/outputs/remote_evaluation/qwen25_coder_7b_instruct_benchmark_v2_qwen2.5-coder_7b-instruct_results.zip `
  outputs/remote_evaluation/
Expand-Archive `
  outputs/remote_evaluation/qwen25_coder_7b_instruct_benchmark_v2_qwen2.5-coder_7b-instruct_results.zip `
  outputs/remote_evaluation/inspected_benchmark_v2
```

Trong archive có cả `outputs/benchmarks/<run>/<model>/run.json`, bảng
`benchmark_table.md`, `candidates.csv`, các `results.jsonl`, log và
`evaluation.json` từng candidate; không có code gốc.
Trước khi báo cáo, kiểm tra đủ 300/164 bài và số `missing_candidates` bằng 0.
Nếu cần nhập kết quả vào output namespace cục bộ để xử lý tiếp, làm riêng
sau khi đã kiểm tra archive; không giải nén chồng lên run lịch sử.
