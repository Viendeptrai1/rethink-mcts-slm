# RethinkMCTS Trace Viewer

Viewer local, read-only để xem cây thought và event trace đã lưu cho từng bài.
Nó không chạy search, gọi LLM, đánh giá candidate hay sửa benchmark artifact.

## Chạy

Từ PowerShell tại `D:\ReThinkMCTS`:

```powershell
.\venv\Scripts\python.exe -m tools.trace_viewer.server
```

Mở <http://127.0.0.1:8765>; dừng server bằng `Ctrl+C`.

Chọn run, model, dataset và problem. Bấm node trong cây để xem thought, prior,
Q-value, visit count, feedback và candidate nếu artifact có lưu. Bấm event trong
trace để xem chi tiết event, LLM request metadata, expansion proposals hoặc code
candidate liên quan.

## Giới hạn hiện tại

- Viewer đọc `outputs/rethinkmcts/<run>/<model>/<dataset>/<problem>/`.
- Chỉ hiển thị thông tin thực sự được ghi trong `tree.json`, `events.jsonl`,
  `search_summary.json` và `candidates/`; không nội suy bước bị thiếu.
- Đây là playback artifact đã lưu, chưa phải live view của search đang chạy.
- Thought trong artifact là reasoning text được Agent phát ra cho thuật toán.
  Viewer không thể khôi phục chain-of-thought nội bộ không được ghi lại.
- Server chỉ bind `127.0.0.1`; không expose ra mạng.
