# Trạng thái hiện tại — 23/09/2026

## Stable facts

- Mốc trước sửa nền: `88aa774`. Nhánh phát triển: `research/feedback-foundation`. Repo kế thừa RethinkMCTS và có các adaptation; không phải phương pháp độc lập đã được chứng minh mới.
- Có runner benchmark chung cho model endpoint và prepared dataset, kiểm tra cohort, manifest/hash và resume theo bài. Có direct, Best-of-N, iterative repair và MCTS; feedback facts/trace/block/adaptive được nối vào luồng thực thi thật.
- Đã sửa sampling theo role, đo model calls/token usage, feedback cho expansion, tracing function/assertion, timeout không giả verdict cho test chưa chạy, và wiring mean backup/test-only reward. Thiếu token usage được báo null.
- Kiểm chứng hiện có: 64 tests qua, chuẩn bị và validate offline 300 APPS, không gọi LLM. Chi tiết và giới hạn bằng chứng ở [RESEARCH_LOG](RESEARCH_LOG.md).
- Chưa có bằng chứng adaptive feedback tăng chất lượng SLM. Chưa chạy pilot development mới. Docker integration thực chưa chạy vì daemon không hoạt động. Token/wall cap hiện là giới hạn tại biên thao tác, không phải hard cap trong request/evaluation.

Revisit khi source/protocol/dataset thay đổi hoặc có kết quả serving/container thực; không dùng test mock để suy ra chất lượng sinh code.

## Active operating decisions

Theo [DECISION_LOG](DECISION_LOG.md): dùng public execution signals để chọn mức feedback; so sánh fixed feedback và iterative repair; giữ bảng exploratory cũ riêng. Câu hỏi và giả thuyết ở [HYPOTHESIS_LAB](HYPOTHESIS_LAB.md), prior work và mức độ đọc ở [LITERATURE_NOTES](LITERATURE_NOTES.md).

Model/data thay bằng config trong phạm vi endpoint và prepared schema đã hỗ trợ. Dataset raw mới có thể cần adapter; chưa hỗ trợ đa ngôn ngữ lập trình. Revision trọng số/serving cần pin bên ngoài runner. Protocol, lệnh sử dụng và giới hạn đầy đủ ở [PROTOCOL](PROTOCOL.md).

Revisit trước khóa final protocol; không sử dụng dữ liệu test đã quan sát làm development độc lập.

## Current context

Mục tiêu người dùng: hoàn thành tiểu luận trong khoảng 2 tháng, có đóng góp riêng và attribution rõ. GPU không là ràng buộc chính. Phiên dựng nền chỉ chạy offline theo yêu cầu. Bước tiếp theo: thẩm định novelty sâu hơn, khóa development cohort, kiểm tra Docker/serving rồi mới pilot LLM theo [ROADMAP](ROADMAP.md).
