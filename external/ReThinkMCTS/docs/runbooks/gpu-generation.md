# Generation qua GPU thuê, tự kéo model

Script `tools.gpu.run_generation` chạy pipeline trên Windows bằng
`D:\ReThinkMCTS\venv`, dùng SSH tunnel riêng để chuyển request Ollama tới GPU
thuê. Dataset và output vẫn ở Windows; chỉ phần inference dùng GPU. Không cần
chép 5.000 bài APPS hay `.env` lên máy thuê, và không cần mở cổng Ollama public.

Instance phải có Ollama đang chạy ở `127.0.0.1:11434` và SSH truy cập được.
Template **Open WebUI + Ollama** trước đây đáp ứng điều này, nhưng phải kiểm tra
trên instance mới. Script không tự cài Ollama hay khởi động Docker. Thay `<HOST>`
và `<SSH_PORT>` bằng thông tin SSH **mới** của CKEY; không dùng host/port cũ.
OpenSSH có thể hỏi xác nhận host key và mật khẩu một lần để mở tunnel. Không
phải SSH vào shell hoặc tự gõ `ollama pull`.

## 1. Kiểm tra plan, không kết nối GPU

```powershell
cd D:\ReThinkMCTS
.\venv\Scripts\python.exe -m tools.gpu.run_generation `
  --ssh-host <HOST> --ssh-port <SSH_PORT> `
  --dataset all --run-name qwen25_coder_7b_instruct_next_v1 `
  --plan
```

## 2. Smoke mỗi tập một bài

```powershell
.\venv\Scripts\python.exe -m tools.gpu.run_generation `
  --ssh-host <HOST> --ssh-port <SSH_PORT> `
  --dataset all --run-name qwen25_coder_7b_instruct_next_v1 `
  --limit 1
```

Script mở SSH tunnel, hỏi Ollama `/api/tags`, chỉ tải
`qwen2.5-coder:7b-instruct` qua `/api/pull` khi thiếu, rồi chạy generation với
`--generation-workers 1 --delay 1`. Nếu pull hoặc API lỗi, generation **không
được chạy**. Lần tiếp theo cùng instance, model đã có thì bỏ qua tải. Model
được tải **trên ổ đĩa GPU thuê**, không phải máy Windows.

## 3. Generation full nếu thật sự cần

```powershell
.\venv\Scripts\python.exe -m tools.gpu.run_generation `
  --ssh-host <HOST> --ssh-port <SSH_PORT> `
  --dataset all --run-name qwen25_coder_7b_instruct_next_v1 `
  --confirm-full-run
```

Resume mặc định bỏ qua bài đã sinh thành công cùng run/model. Không dùng
`--confirm-full-run` cho smoke. Lệnh full có thể tạo đến 5.164 request LLM
trước retry; chỉ chạy khi đã xem plan và chi phí. Nếu chỉ cần một tập, thay
`--dataset all` bằng `apps` hoặc `humaneval`.

Để dùng model khác, truyền `--model` và config tương ứng. Không tăng
`--generation-workers` quá 1 trước khi xác nhận Ollama ổn định. Script chỉ
quản lý **direct generation**, không chấm code hay chạy MCTS.

**Benchmark v2 hiện tại không cần lệnh này:** toàn bộ code baseline đã sinh
xong. [Remote evaluation](remote-evaluation.md) chỉ chấm candidate có sẵn
bằng CPU/Docker, không tải hoặc gọi model.
