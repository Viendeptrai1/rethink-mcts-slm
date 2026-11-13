# Nhật ký bằng chứng

## E-001 — Rà soát nền cũ (23/09/2026)

Nguồn: repository review 23/09/2026 (đã lưu trữ ở tag `archive/pre-v3-2026-11-13`), code/artifacts trước `88aa774`. Các bảng cũ là exploratory, không đo controller adaptive hiện tại. Review cũ được giữ nguyên để truy vết; thông tin đã bị phát hiện thiếu hoặc thay đổi được ghi ở các entry sau.

## E-002 — Public/hidden overlap APPS

Phương pháp: so nội dung test case sau khi bỏ `case_id`, thay vì so toàn object chứa ID khác nhau giữa hai tập. Trong 300 APPS local có 13 hidden cases trùng public thuộc 8 bài; subset introductory cũng có bài bị ảnh hưởng, gồm `apps_4073`. Điều này bổ sung/sửa kết luận overlap từ lần kiểm tra nông hơn trong review cũ.

Adapter v2 bỏ các bản trùng public khỏi hidden; runner v2 từ chối dữ liệu prepared còn exact overlap. Chuẩn bị lại vào TemporaryDirectory rồi validate toàn cohort được 300 bài, 600 public tests và 19.542 hidden tests. Không ghi đè prepared/apps hay kết quả cũ. Thư mục tạm đã được dọn; tái tạo bằng lệnh trong PROTOCOL.

Giới hạn: so trùng chính xác không phát hiện mọi biến thể tương đương ngữ nghĩa hoặc contamination từ pretraining. First-two-public là adaptation được khai báo, không khẳng định giống split của tác giả.

## E-003 — Kiểm chứng chức năng offline

Lệnh: `python -m pytest -q`. Kết quả cuối phiên: **64 passed**, gồm 36 tests cũ và 28 integration/regression tests cho nền mới. Dùng mock/spy gateway, monkeypatch HTTP và fixture code; không gửi request LLM.

Các ràng buộc chính được kiểm tra: accounting cả block analysis; sampling/seed đến gateway; missing usage không thành 0; HTTP retries được đếm; cap khiến feedback downgrade; expansion nhận feedback; mean backup/test-only thật sự thay hành vi; tracing function/assertion và kill timeout; không giả fail các test sau TLE; hidden sentinel không vào request/feedback; manifest/resume từ chối config hoặc selected-code bị đổi; các baseline và adaptive policy hoạt động trên fixture.

Dry-run đã validate toàn 164 HumanEval hiện có và 300 APPS được prepare v2 trong thư mục tạm; không tạo output run hay gọi mạng LLM. Dữ liệu này chưa phải development mới.

Kiểm tra CLI end-to-end với `configs/research_smoke.yaml` trong TemporaryDirectory: hoàn tất 1 fixture, ghi 5 logical model calls và tokens=null đúng với mock. Chạy lại cùng lệnh resume cho summary giống hệt (kể cả thời gian đã lưu); không sinh lại bài đã hoàn tất. Thư mục tạm đã được dọn.

Giới hạn: đây là bằng chứng code/protocol, không chứng minh hiệu quả phương pháp, tính đầy đủ của CFG, isolation thực của Docker hoặc chất lượng serving. Không tính tỷ lệ pass mock thành kết quả nghiên cứu.

## E-004 — Docker chưa sẵn sàng

Có binary Docker nhưng probe image/daemon trả lỗi kết nối socket. Không build image hay chạy container; tests hiện kiểm tra dựng command và dùng chung harness. Cần kiểm chứng container thực trước benchmark generated code. Không fallback sang host khi cấu hình Docker lỗi.

## E-005 — Đối chiếu prior work có mục tiêu

Đã ghi nguồn và mức độ đọc vào [LITERATURE_NOTES](LITERATURE_NOTES.md). Kết luận dùng để thiết kế: runtime/basic-block feedback, chọn blocks và adaptive allocation đều có tiền lệ; chỉ đổi backbone sang SLM không đủ để nhận thuật toán mới. Chưa xác nhận novelty toàn diện. Controller v0 và ba câu hỏi nghiên cứu vẫn ở trạng thái cần thử nghiệm.
