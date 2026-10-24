# LLM provider

## Provider benchmark hien tai

RethinkMCTS run `rethinkmcts_qwen25_modal_v1` dung `LLM_PROVIDER=modal_gpu`:
private Modal Function chay Ollama Qwen2.5-Coder 7B tren L4, local judge tren
Windows. HumanEval 164 da hoan tat; APPS dang tam dung. Xem
[Modal MCTS runbook](runbooks/modal-mcts.md). Khong dung `MODAL_PROXY_*` lich su.

Direct-generation baseline lich su dung `LLM_PROVIDER=ollama` tren GPU CKEY.

## Quyết định hiện tại

Dự án có adapter `ModalClient` cho endpoint OpenAI-compatible lịch sử và
`ModalGpuClient` gọi private Modal Function của run MCTS hiện tại. Modal account
token nằm trong profile do `modal setup` tạo, không nằm trong `.env`; cấu hình
Ollama/CKEY lịch sử vẫn do `.env` quản lý.

Thông tin instance GPU và checklist vận hành nằm tại [GPU runtime](gpu/README.md).

## Biến môi trường

| Biến | Bắt buộc | Ý nghĩa |
|---|---:|---|
| `MODAL_PROXY_TOKEN_ID` | Có | ID dùng để xác thực Modal proxy |
| `MODAL_PROXY_TOKEN_SECRET` | Có | Secret dùng để xác thực Modal proxy |
| `MODAL_BASE_URL` | Có | Base URL OpenAI-compatible, gồm version path nếu endpoint yêu cầu |
| `KIMI_MODEL` | Modal | Model identifier gửi trong request Modal |
| `LLM_PROVIDER` | Ollama | Provider đang chọn cho benchmark GPU mới |
| `LLM_BASE_URL` | Ollama | Base URL OpenAI-compatible của Ollama |
| `LLM_MODEL` | Ollama | Model identifier, dự kiến `qwen2.5-coder:7b-instruct` |
| `LLM_API_KEY` | Ollama | Giá trị local, thường là `ollama`; không phải secret |

Mẫu không chứa secret được lưu tại `.env.example`. File `.env` thật phải được Git
ignore và không được chép vào log, Markdown, notebook hoặc artifact thử nghiệm.

## Cách khởi tạo client

```python
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.environ["MODAL_BASE_URL"],
    api_key=(
        f"{os.environ['MODAL_PROXY_TOKEN_ID']}."
        f"{os.environ['MODAL_PROXY_TOKEN_SECRET']}"
    ),
)
model = os.environ["KIMI_MODEL"]
```

## Quy tắc thử nghiệm

- Không in token hoặc toàn bộ environment ra terminal/log.
- Không commit `.env`; chỉ commit `.env.example` với giá trị rỗng.
- Smoke test đầu tiên chỉ gửi một request ngắn.
- Khi chạy RethinkMCTS, bắt đầu với 1 bài và rollout thấp.
- Ghi model identifier, tham số sampling, số request và token usage nếu API trả về.
- Không ghi giá trị token vào tài liệu tái lập; chỉ ghi tên biến môi trường.
- Không gọi API chỉ để kiểm tra cấu hình nếu có thể kiểm tra offline.

## Trạng thái xác minh

Đã kiểm tra offline ngày 2026-09-26:

- `.env` tồn tại.
- Bốn biến bắt buộc đều có mặt và không rỗng.
- `MODAL_BASE_URL` có dạng URL HTTP(S).
- `tools/smoke_modal.py` là smoke script lịch sử cho Modal; pipeline benchmark hiện
  tại dùng `pipelines` với provider Ollama.

Đã gửi request thật qua endpoint Modal và nhận được response/usage. Một lần cấu hình
route sai trả `404 route not found`; sau khi sửa `.env`, plan resolve đúng model và
generation tạo được artifact. Không ghi endpoint hoặc token vào tài liệu/log.
