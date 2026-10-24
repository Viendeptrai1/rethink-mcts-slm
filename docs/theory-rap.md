# RAP - ghi chú đối chiếu

Nguồn tham khảo: **Reasoning with Language Model is Planning with World Model**,
arXiv `2305.14992`.

## Vai trò trong dự án

RAP là related work để hiểu cách kết hợp LLM với MCTS. Đây không phải baseline chính
và chưa phải thành phần cần implement ở giai đoạn hiện tại.

## Ý tưởng cốt lõi

RAP nhìn reasoning như một bài toán planning:

- LLM đóng vai trò policy để đề xuất action/reasoning step.
- LLM cũng đóng vai trò world model để dự đoán state tiếp theo.
- MCTS tìm đường reasoning có triển vọng dựa trên reward và self-evaluation.

Khác biệt quan trọng với RethinkMCTS:

| Khía cạnh | RAP | RethinkMCTS |
|---|---|---|
| Không gian search | Reasoning state/action | Thought dùng để sinh code |
| Chuyển trạng thái | World model dự đoán | Nối thought vào state |
| Tín hiệu môi trường | Chủ yếu do model ước lượng | Chạy code trên public tests |
| Sửa lỗi | Search nhánh khác | Rethink thought hiện tại bằng verbal feedback |
| Domain chính | Reasoning/planning tổng quát | Code generation |

## Giới hạn của ghi chú này

File này chỉ giữ đối chiếu khái niệm cần cho đề tài. Chưa có bản PDF RAP trong
`RelativeWork/`, vì vậy không dùng file này làm nguồn cho công thức hoặc chi tiết
implementation. Trước khi triển khai hoặc báo cáo định lượng về RAP, cần thêm paper
gốc, đọc lại và cập nhật tài liệu với trích dẫn theo section/table.

