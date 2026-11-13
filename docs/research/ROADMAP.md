# Lộ trình khoảng 8 tuần

> **Ghi chú 13/11/2026:** các mục viết trước protocol v3 (kế hoạch 3B/7B chính, 14B đối chiếu) là lịch sử. Kế hoạch hiện hành: [KHUNG_BAO_CAO_v2.md](../report/KHUNG_BAO_CAO_v2.md) và [PROTOCOL.md](PROTOCOL.md) mục 8; model là Qwen2.5-Coder-7B, Seed-Coder-8B, Qwen3.5-9B (D-006).

Đây là kế hoạch kể từ phiên dựng nền 23/09/2026; deadline chính xác chưa được khóa. Trạng thái và bằng chứng hiện tại nằm trong CURRENT_STATE/RESEARCH_LOG, không suy từ checkbox kế hoạch.

## Tuần 1 — Khóa câu hỏi và điều kiện đo

- Đọc toàn văn/code của các prior work gần nhất, đặc biệt conditional search và selective feedback. Lập bảng thuật toán, tín hiệu đầu vào, model scale, baseline và budget; điều chỉnh claim nếu trùng.
- Dùng RQ1/RQ2 làm trọng tâm; RQ3 là phân tích bổ sung. Định nghĩa đóng góp là cơ chế cụ thể và kết quả kiểm chứng, không phải việc “dùng SLM” riêng lẻ.
- Chọn APPS train development cohort, phân tầng difficulty, lưu danh sách ID/seed và kiểm tra trùng nội dung với final cohort. Chốt lượng bài sau kiểm tra độ dài/test coverage, trước khi xem kết quả phương pháp.
- Build/pin Docker image; kiểm tra container stdin/function/assertion/trace và resource limits. Kiểm tra serving seed, tokenizer/context, token usage và pin revision. Chưa tự động chạy LLM trong phiên dựng nền.
- Chọn quy tắc matched-budget khả thi: cùng code/call cap kèm realized-token curves, hoặc bổ sung reservation nếu muốn strict token cap. Không gọi soft cap hiện tại là strict matched-token.

Điều kiện hoàn tất: protocol/cohort/serving checklist có artifact và không còn lỗi infrastructure làm lẫn với model failure.

## Tuần 2–3 — Pilot development và cơ chế chọn feedback

- So facts/trace/block cố định, adaptive v0 và iterative repair trên cùng cohort/checkpoint/budget. Direct và Best-of-N cung cấp mốc cơ sở.
- Phân tầng theo lỗi ban đầu; đo tỷ lệ sửa đúng, regression, lặp lại cùng code, phân bố feedback level và token theo role. Lưu cả kết quả âm và analyzer feedback sai.
- Tune ngưỡng tăng mức chỉ trên development. Ablation bỏ adaptation, bỏ block analysis, và test-only reward nếu cần để tách ảnh hưởng critic.
- Nếu adaptive không hơn baseline mạnh nhất, kiểm tra cơ chế và chất lượng feedback; cho phép đổi đóng góp thành nghiên cứu thực nghiệm có kết quả âm thay vì ép claim thắng.

Điều kiện hoàn tất: chọn/freeze controller, prompts, hyperparameters và tiêu chí báo cáo trước final test.

## Tuần 4–5 — Benchmark đã khóa

- 3B/7B là hai mốc chính, 14B đối chiếu dự kiến; cùng họ model để giảm yếu tố nhiễu. Ba seed, budget grid dự kiến 4/8/16; điều chỉnh grid trên development trước khi khóa.
- APPS holdout và benchmark ngoài phù hợp; ghi rõ phần test đã quan sát từ run cũ. Với HumanEval cần thảo luận ceiling/contamination và hạn chế public examples.
- Dùng output directory riêng theo model/data/method/seed/budget; audit provenance, unknown usage, failure denominator và selection chỉ dựa public.

## Tuần 6 — Phân tích

- Mean/std qua seed, paired bootstrap CI theo bài, correctness theo realized compute; định nghĩa resampling unit và aggregation trước khi tính.
- Phân tích sensitivity theo error type/model size, feedback không hữu ích, public overfit, hạ mức do budget và trường hợp method thua repair.
- Kiểm tra đối chiếu từng số trong bảng với artifacts; không gộp kết quả protocol cũ và mới.

## Tuần 7–8 — Viết và hoàn thiện tiểu luận

- Viết attribution rõ: phần kế thừa RethinkMCTS/LDB, phần adapter/engineering, phần cơ chế đề xuất và phần được thực nghiệm chứng minh.
- Hoàn thiện related work, method/pseudocode, protocol, kết quả, giới hạn, reproducibility appendix và slide bảo vệ.
- Để khoảng đệm sửa lỗi, chạy kiểm tra cần thiết và phản biện claim; không thêm nhánh thuật toán lớn cuối kỳ.
