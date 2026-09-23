# Prior work và ranh giới đóng góp

Ngày kiểm tra nguồn: 23/09/2026. Đây là targeted review phục vụ thiết kế, chưa là systematic review hoặc chứng nhận không có phương pháp trùng.

| Nguồn gốc | Đã đối chiếu | Liên quan và ranh giới |
|---|---|---|
| [RethinkMCTS, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.410/) | Metadata chính thức và phần method/experiments trong bản trích xuất local | Kế thừa thought-level MCTS, leaf rethink và dual feedback; phải phục hồi feedback cho expansion trước so sánh. Không nhận các cơ chế này là đóng góp riêng. |
| [LDB](https://arxiv.org/html/2402.16906v2) | Method: profiling, debugging, selective debugging | Runtime state/basic-block feedback đã có; LDB còn chọn một số blocks khi trace dài. Điểm cần kiểm định ở đề tài là chọn **loại/mức feedback giữa facts, trace, analysis theo lịch sử public**, không đơn thuần cắt bớt trace. |
| [Feedback Over Form, preprint 2026](https://arxiv.org/html/2604.21950v1) | Method, kết quả tổng quan, §5.6 limitations | Pipeline 1–3B cho thấy feedback/loại lỗi quan trọng; paper tự giới hạn kết luận trong model pool và search space được thử. Thí nghiệm chính của họ không tương đương sweep cùng họ code model 3B/7B/14B. Cần baseline iterative repair và phân tầng error type; không mặc định tree phức tạp sẽ thắng. |
| [Reason-Code, ACL Industry 2026](https://aclanthology.org/2026.acl-industry.30/) | Abstract và metadata chính thức; chưa thẩm định toàn văn/code | Conditional search sau greedy failure đã có; mô tả abstract còn nêu khác biệt hạn chế giữa UCB và repair ở budget thấp. Không nhận early activation MCTS là mới; cần đọc protocol đầy đủ trước tái hiện baseline mang tên Reason-Code. |
| [Learning How Hard to Think](https://arxiv.org/abs/2410.04707) | Abstract chính thức; chưa thẩm định toàn văn/code | Adaptive allocation/routing đã được nghiên cứu trên nhiều task. Controller v0 ở repo là heuristic về mức feedback, không phải tái hiện bộ dự đoán phân phối reward của công trình này. |

Đóng góp đang hướng tới: khảo sát tương tác kích thước model × loại lỗi × mức feedback; một chính sách chọn mức public-only được mô tả tường minh; đánh giá matched-budget và regression có provenance. Cả hiệu quả và mức độ mới đều còn cần kiểm chứng.

Việc còn thiếu trước khẳng định novelty: đọc toàn văn Reason-Code và các bài chọn/thu gọn feedback, so sánh thuật toán/prompt/benchmark chính xác, theo dõi các nghiên cứu mới sát đề tài. Iterative repair trong repo được gọi đúng là baseline tự hiện thực; không gắn tên LDB, Reflexion hay Self-Refine nếu chưa tái hiện đúng protocol của họ.
