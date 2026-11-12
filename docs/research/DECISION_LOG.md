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

## D-006 — Chuyển sang protocol v3 và nhiều model 7–9B (12/11/2026)

Lý do: review code 11–12/11/2026 cho thấy bản 14B v1 chưa chạy đúng hai cơ chế cốt lõi. Block analysis bị bỏ (0/1.203 lần vào feedback). Rethink không thấy thought cần sửa. Critic không có tác dụng vì dừng sớm. Ngân sách tính cả rethink nên cây chỉ sâu tối đa 2. Ngoài ra MCTS chưa được so với baseline cùng chi phí. Chi tiết: [prompts/README.md](../../prompts/README.md), [configs/v3_7b/README.md](../../configs/v3_7b/README.md).

Quyết định (người dùng đồng ý ngày 12/11/2026):
1. Giữ tên đề tài trong [Proposal.md](../../Proposal.md). Vấn đề cụ thể: tái hiện và kiểm chứng RethinkMCTS trên nhiều model mở 7–9B, so với baseline cùng ngân sách.
2. Model: Qwen2.5-Coder-7B-Instruct, Seed-Coder-8B-Instruct, Qwen3.5-9B (tắt thinking; dự phòng Granite-4.2-8B). Tắt thinking cho mọi phương pháp. Kết quả 14B v1 chỉ vào phụ lục; 14B v3 chỉ chạy nếu còn credit.
3. Thiết lập v3 theo bài báo: 16 rollout, 1 rethink/node, không dừng sớm (tính lại offline), temperature 0, critic [-1, 1], public = một nửa số test khác nhau. Token và lời gọi chỉ có giới hạn an toàn.
4. Baseline: Direct (temperature 0) và Best-of-16 (temperature 0,8, chọn theo public test). BO3 v1 không còn là baseline chính.
5. Phần cứng: Modal L40S, bf16, không nén trọng số. L4 chỉ để so tốc độ ở pilot (P4).
6. Pilot trên 20 bài APPS ngoài cohort; tiêu chí đạt ở [configs/v3_7b/README.md](../../configs/v3_7b/README.md). Sau pilot mới đóng băng protocol và chạy cohort thật.

Còn mở: temperature của Best-of-16 (0,8 là đề xuất); có chạy ablation trên 300 bài hay tập con; có chạy lại nhánh 7B của HuyinCP theo v3 hay không.

## D-007: Protocol v3.1, nâng giới hạn output (12/11/2026)

Lý do: gate của Qwen3.5-9B (chạy với v3.0) fail vì 15/255 output bị cắt (5,9%, ngưỡng 5%). Bị cắt gồm expansion 6/64 (giới hạn 512), block analysis 6/29 (1.536), rethink 2/22 (256), code 1/153 (2.048). Các output này đều là lập luận hợp lệ viết dở, không phải lặp. Expansion bị cắt làm node bị đóng, analysis bị cắt làm feedback tụt xuống mức trace, nên model bị thiệt vì cấu hình chứ không vì năng lực. Seed-Coder-8B qua gate v3.0 nhưng cũng có 11/90 block analysis bị cắt. Nguồn: `colab_results/qwen35/`, `colab_results/seed_v30/`.

Quyết định (người dùng đồng ý): nâng giới hạn **cho mọi model**: expansion 1.024, code 4.096, rethink 512, block analysis 3.072 (critic giữ 256); vLLM `max-model-len` 32.768 để prompt cộng output vẫn vừa ngữ cảnh. Với temperature 0, output nào trước đây không bị cắt thì giữ nguyên. `protocol_id` đổi thành `*_v3_1`. Chưa run cohort nào chạy xong với v3.0 (run MCTS của Seed-Coder bị dừng ngay khi vừa bắt đầu), nên mọi run báo cáo đều dùng v3.1. Pilot P1/P2 (v3.0) vẫn giữ làm bằng chứng về quy trình.
