# Giả thuyết — chưa được chứng minh

> **Ghi chú 13/11/2026:** các giả thuyết dưới đây được viết trước protocol v3 (khi còn dự định 3B/7B/14B). Câu hỏi và giả thuyết hiện hành ở [KHUNG_BAO_CAO_v2.md](../report/KHUNG_BAO_CAO_v2.md) mục RQ1–RQ5.

## H-001 — Mức feedback và loại lỗi

**RQ1:** Ở mô hình sinh mã 3B/7B/14B, facts, runtime trace và trace kèm phân tích LLM khác nhau thế nào về tỷ lệ sửa đúng, regression và chi phí, khi giữ nguyên pipeline và ngân sách?

Giả thuyết: trace/analysis có thể hữu ích cho wrong answer hơn một số lỗi cú pháp/runtime đã có tín hiệu rõ. Không giả định LLM analyzer luôn đúng. Bằng chứng cần: cùng lỗi đầu vào hoặc phân tầng theo lỗi ban đầu, nhiều seed, giữ generator/refiner checkpoint cố định trong mỗi so sánh.

## H-002 — Chọn mức thích ứng

**RQ2:** Controller chỉ dựa vào thông tin public có cải thiện đường cong selected-solution correctness theo realized tokens so với mọi mức cố định và iterative repair không?

Giả thuyết: tránh phân tích đắt khi không cần, tăng mức khi không tiến triển có thể cải thiện trade-off. Controller v0 trong PROTOCOL là heuristic kiểm chứng được, không phải thuật toán đã chứng minh tối ưu. Kiểm định ưu thế với baseline mạnh nhất dưới cùng budget, không chỉ Direct.

## H-003 — Vai trò của kích thước mô hình

**RQ3:** Lợi ích của mức feedback thay đổi ra sao theo kích thước checkpoint? Có vùng mà thêm phân tích làm tốn token hoặc gây regression?

Một họ model giảm một số yếu tố nhiễu nhưng không biến số tham số thành biến nhân quả độc lập. 14B là mốc so sánh; không dựa vào ngưỡng SLM phổ quát. Kết quả âm vẫn phải báo.

Chưa có kết quả LLM mới cho cả ba giả thuyết. Test mock chỉ xác nhận hành vi chương trình.
