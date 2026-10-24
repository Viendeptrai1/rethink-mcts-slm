# RethinkMCTS trên GPU thuê: APPS 300 + HumanEval 164

**Trạng thái:** gói và code đã kiểm thử offline; chưa smoke trên CKEY mới.
Đây là pipeline MCTS thật (gọi LLM để expand/sinh code/rethink và chấm code
ngay trong search), **khác** `tools/gpu/run_generation.py` của baseline direct.
Không chạy full trước khi kiểm tra Docker, smoke và chi phí.

## Chuẩn bị máy thuê

- Chọn template **Open WebUI + Ollama** cho RTX 3090 24 GB; không cần tải
  model trên laptop rồi chuyển lên.
- Mở SSH `22` (và `7681` nếu cần terminal web); không cần public port `11434`.
  CKEY có thể đổi hostname/port ánh xạ sau mỗi lần thuê.
- Trên máy thuê, xác minh `docker info`, `curl http://127.0.0.1:11434/api/tags`
  và dung lượng `df -h`. Nếu Docker không chạy được thì **dừng**, không chấm
  code sinh ra trực tiếp trên host. Bundle tự pull `qwen2.5-coder:7b-instruct`
  khi bắt đầu smoke/full, nhưng không pull ở bước plan. Kiểm tra đủ dung lượng
  cho Docker image, model và output trước khi chạy.

## Đóng gói trên Windows (không gọi LLM)

```powershell
cd D:\ReThinkMCTS
.\venv\Scripts\python.exe -m unittest discover -s tests -q
.\venv\Scripts\python.exe -m rethinkmcts.batch `
  --run-name rethinkmcts_qwen25_v1 --model qwen2.5-coder:7b-instruct --plan
.\venv\Scripts\python.exe -m tools.remote_mcts.prepare_bundle `
  --run-name rethinkmcts_qwen25_v1 --model qwen2.5-coder:7b-instruct `
  --archive outputs/remote_mcts/rethinkmcts_qwen25_v1.zip
```

ZIP chỉ chứa đúng 300 đề APPS cùng test/starter, HumanEval Arrow 164 bài,
public `given_tests`, manifest và source cần thiết; không chứa `.env`, APPS
`solutions.json`, baseline `solution.py` hoặc output cũ. HumanEval Arrow có
`canonical_solution` và official harness vì executor cần chấm cuối; prompt
LLM chỉ lấy đề bài, không đưa các cột này vào prompt.

## Chuyển và chạy trên GPU

Thay `<HOST>` và `<SSH_PORT>` bằng SSH endpoint **mới** từ trang CKEY.
Lệnh PowerShell trên laptop:

```powershell
scp -P <SSH_PORT> outputs/remote_mcts/rethinkmcts_qwen25_v1.zip root@<HOST>:/root/
ssh root@<HOST> -p <SSH_PORT>
```

Lệnh trong SSH terminal trên máy thuê:

```bash
mkdir -p /root/rethinkmcts_qwen25_v1
python3 -m zipfile -e /root/rethinkmcts_qwen25_v1.zip /root/rethinkmcts_qwen25_v1
cd /root/rethinkmcts_qwen25_v1
docker info
curl -fsS http://127.0.0.1:11434/api/tags
bash tools/remote_mcts/run.sh --plan
bash tools/remote_mcts/run.sh --smoke --rollouts 2 --width 3
```

Smoke chạy APPS `2408` và HumanEval/0 (một bài mỗi tập). Script chỉ auto-pull
model nếu thiếu. Nó ghi `run_config.json`, `progress.jsonl`, `attempt.log`,
`search_summary.json`, `final_solution.py`, `events.jsonl` và candidate logs.
Xem `outputs/remote_mcts/worker.log` và
`outputs/rethinkmcts/rethinkmcts_qwen25_v1/qwen2.5-coder_7b-instruct/`.
Kiểm tra lỗi, thời gian, token/request, public/private score và model digest
trước khi quyết định full. `--smoke` tốn request thật; `--plan` thì không.

Sau khi chấp nhận smoke, **mới** chạy full với đúng tham số trên:

```bash
bash tools/remote_mcts/run.sh --confirm-full-run --rollouts 2 --width 3
```

Batch chạy **1 bài tại một thời điểm** (không có worker CPU song song); LLM
cũng chỉ có một search đang hoạt động. APPS có 5.959 test gốc trong cohort;
`--timeout-seconds 5` tính cho **mỗi test**, `--problem-timeout-seconds 900`
cho cả một search subprocess. Rollout/rethink có thể làm số lần chấm và request
tăng nhiều; 464 bài có thể vượt thời gian/số dư thuê. Ba failure liên tiếp sẽ
dừng. Full chỉ chạy khi đã chủ động cấp đủ thời gian/chi phí.
Với mặc định 2 rollout và 2 lần Rethink, plan 464 bài ước lượng khoảng
**2.784 request** nếu mọi public test pass ngay hoặc **8.816 request** nếu
mọi lần đều fail; đây không phải dự báo thời gian/token, nhưng cho thấy full
MCTS đắt hơn nhiều so với direct generation một request/bài.

Khi mất kết nối hoặc hết hạn GPU, **không tự động đồng bộ về laptop**. Khi máy
thuê còn chạy, tạo checkpoint rồi kéo về:

```bash
python3 -m tools.remote_mcts.collect_results \
  --run-name rethinkmcts_qwen25_v1 --model qwen2.5-coder:7b-instruct --partial
```

Trên laptop, dùng `scp -P <SSH_PORT> root@<HOST>:/root/rethinkmcts_qwen25_v1/outputs/remote_mcts/*_checkpoint.zip outputs/remote_mcts/`.
Muốn resume trên instance khác phải chuyển lại **cả** `outputs/rethinkmcts/`
và `outputs/rethinkmcts_attempts/` từ checkpoint, giữ cùng ZIP, model digest,
tham số và Docker image. Batch bỏ qua bài có `search_summary.json` cùng
`final_solution.py` hợp lệ; bài đang chạy dở sẽ làm lại từ đầu và attempt cũ
vẫn được giữ. LangGraph chưa checkpoint giữa một bài.

Khi đủ 300+164, script tự tạo `outputs/benchmarks/<run>/<model>/` với
`run.json`, `candidates.csv`, `benchmark_table.csv/.md`, per-dataset
`results.csv/.jsonl` và `benchmark_metrics.json`, rồi đóng ZIP kết quả.
Nếu run chưa đủ cohort, finalizer từ chối tạo bảng. APPS dùng nửa đầu test cho
search feedback, còn final evaluation chạy toàn bộ test giống baseline direct.

**Giới hạn an toàn:** Docker hiện cô lập **toàn batch**, không cô lập từng
candidate. Container dùng host networking để gọi Ollama và được ghi output;
code sinh ra có thể truy cập mạng, input/test khác trong bundle và output của
run. Đây chưa phải sandbox đủ mạnh cho code không tin cậy; chỉ chạy trên
instance thuê riêng, không đặt secret trong bundle/container và không dùng
máy cá nhân để chấm. Cần sandbox từng candidate trước thí nghiệm mức tin cậy cao.
