# Quyết định

## D-001 — Mốc lịch sử trước khi sửa nền (23/09/2026)

Theo yêu cầu người dùng, commit `88aa774` lưu code, dữ liệu, cấu hình, tài liệu và báo cáo exploratory hiện tại. `runs/` vẫn nằm cục bộ theo ignore policy. Phát triển tiếp trên nhánh `research/feedback-foundation`; không ghi đè bảng kết quả cũ.

## D-002 — Phạm vi làm việc

Người dùng muốn hoàn thiện nền, đối chiếu prior work và xây dựng cơ chế chọn feedback; chưa cần gọi LLM. Quyết định kỹ thuật: dùng mock/spy gateway, fixtures và dry-run toàn bộ prepared data trong giai đoạn này. Giới hạn thời gian khoảng 2 tháng; ngân sách GPU không phải trở ngại. Chưa huấn luyện/fine-tune hoặc mở rộng graph thành phương pháp chính vì sẽ tăng số yếu tố cần kiểm chứng.

## D-003 — Câu hỏi nghiên cứu làm việc

Chọn **mức phản hồi thực thi thích ứng theo loại lỗi và tình trạng không tiến triển** làm trục v0. So sánh trên code models 3B/7B, 14B làm mốc đối chiếu dự kiến; danh sách model không khóa trong code. Câu hỏi cụ thể và giả thuyết ở HYPOTHESIS_LAB; tính mới chưa được chứng nhận toàn diện. Có thể điều chỉnh sau literature review sâu và pilot development.

Lý do: tận dụng execution/trace/rethink sẵn có, tạo phép so sánh một yếu tố, hoàn thành được trong 8 tuần. Chỉ đổi backbone hoặc thêm early stop không đủ khác biệt với prior work. Đề tài không nhận MCTS, runtime feedback hoặc adaptive compute nói chung là phát minh mới.

## D-004 — Protocol v2 và tính tái lập

Mọi run mới có manifest theo effective config, source, prompt, dữ liệu, cohort và runtime. Resume chỉ ở ranh giới hoàn thành một bài; không nhập dữ liệu từ run cũ thiếu manifest. Chọn chương trình chỉ từ public evaluation. Hidden judging tách khỏi solver và controller; trong kiểm tra dry-run, coordinator được đọc suite để xác thực cấu trúc/hash nhưng không cấp cho model.

APPS v2 vẫn dùng first-two-public như một adaptation công khai, loại hidden cases trùng public về nội dung. Đây chưa phải exact author split. Không sửa prepared/apps hoặc các kết quả cũ; tạo output mới khi chuẩn bị lại dữ liệu.

## D-005 — Cách hiểu chi phí

Model call là logical request; transport retries được báo riêng. Token usage thiếu được ghi null; không giả lập 0. Token cap và wall cap được kiểm tra ở ranh giới thao tác; chưa phải bảo đảm cứng không vượt trong một request/evaluation đang chạy. Main protocol để transport retries=0, đòi token usage thật và báo realized compute. Không suy chi phí GPU hoặc USD từ số calls.
