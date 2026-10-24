# Môi trường phát triển

## Môi trường chuẩn

Từ ngày 2026-09-26, toàn bộ lệnh Python và pip của dự án phải dùng virtual
environment tại:

```text
D:\ReThinkMCTS\venv
```

Không dùng Python/pip global khi chạy script, cài dependency hoặc kiểm thử.

Riêng workflow [remote evaluation](runbooks/remote-evaluation.md) chạy trên
Linux trong Docker image Python 3.11 với dependency tối thiểu ở
`tools/remote_evaluation/requirements.txt`. `D:\ReThinkMCTS\venv` của Windows
chỉ dùng để chuẩn bị bundle tại máy cục bộ; không copy venv này sang máy thuê.

## Lệnh PowerShell

Kích hoạt môi trường:

```powershell
.\venv\Scripts\Activate.ps1
```

Hoặc gọi trực tiếp, phù hợp cho automation:

```powershell
.\venv\Scripts\python.exe --version
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Dependency manifest

`requirements.txt` được tổng hợp từ:

- Import của code hiện tại: `openai`, `python-dotenv`, `datasets`.
- Toàn bộ import bên thứ ba trong repo RethinkMCTS gốc tại commit
  `3908cacd94feed849f671f6de39f0baec00ed72c`.

Repo gốc không có `requirements.txt`, nên các dải phiên bản hiện tại là baseline để
resolve trên môi trường mới, chưa phải lockfile tái lập tuyệt đối. Sau khi clone repo
và chạy baseline thành công, cần tạo lockfile hoặc ghi lại `pip freeze` của môi trường
đã xác minh.

Đã chạy `pip install --dry-run --ignore-installed -r requirements.txt` thành công
trên Python 3.14.5 ngày 2026-09-26. Kiểm tra này xác nhận resolver tìm được bộ package
phù hợp nhưng **chưa cài đặt** chúng vào `venv`.

Đã cài nhóm tối thiểu cho direct baseline: `openai`, `python-dotenv`, `datasets` và
các dependency bắc cầu của chúng. Nhóm MCTS/PyTorch trong manifest chưa được cài.
Ngày 2026-10-04 đã cài `langgraph` và `pydantic` trong chính `venv` cho native
workflow; `pip check` không báo dependency lỗi. Đây không phải là việc cài
toàn bộ nhóm PyTorch của repo tác giả.
Modal SDK 1.6.1 da duoc cai trong `venv`; `modal setup` luu token tai profile
nguoi dung, khong luu trong `.env` cua project.

## Nhóm dependency

| Nhóm | Package chính |
|---|---|
| LLM | `openai`, `python-dotenv`, `tiktoken` |
| Native workflow | `langgraph`, `pydantic` |
| Dataset | `datasets`, `jsonlines`, `numpy` |
| Runtime | `torch`, `accelerate`, `transformers`, `torcheval`, `torchmetrics` |
| Phân tích code | `astor`, `astroid`, `astunparse`; local shim thay `pyext` |
| Phân tích kết quả | `matplotlib`, `scikit-learn`, `tqdm` |

## Trạng thái tương thích

`venv` hiện dùng Python 3.14.5. Đây là phiên bản mới hơn thời điểm code gốc được
viết, vì vậy cần xác minh đặc biệt:

- Wheel của PyTorch và các package native trên Windows.
- API thay đổi trong `transformers`, `openai`, `astroid` và `datasets`.
- Module `resource` mà executor gốc import là module dành cho Unix, không có sẵn
  trên Windows; đây là vấn đề portability của code, không phải dependency pip.
- `pyext==0.7` dùng `inspect.getargspec` và không build được trên Python 3.14.
  Repo gốc chỉ dùng `RuntimeModule.from_string` trong APPS executor, nên khi tích
  hợp cần thay bằng compatibility shim cục bộ thay vì cài package lỗi thời này.

Không đổi phiên bản Python hoặc tạo virtual environment khác mà chưa cập nhật file
này, `project-status.md` và `decisions.md`.
