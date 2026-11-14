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

## D-008: Vận hành đợt chạy v3.1 trên Colab khi runtime bị thu hồi (13/11/2026)

Bối cảnh: từ khoảng 01:45 đến 10:10 ngày 13/11, runtime A100 trên Colab thường biến mất sau khoảng 22–25 phút. Nguyên nhân phía Colab chưa rõ. Chi tiết và số liệu ở [BENCHMARK_LEDGER.md](../results/BENCHMARK_LEDGER.md), mục 12.

Quyết định:
1. **Resume từ bản lưu.** Bản lưu `runs/` được tải về mỗi 5 phút, và run được tiếp tục trên VM mới với cùng code đóng băng `d9666c4`. Chấp nhận vì resume chỉ diễn ra ở ranh giới hoàn thành một bài, manifest được kiểm tra khớp, và bài đang chạy dở được giải lại từ đầu (D-004).
2. **Bài vướng lỗi CRLF khi resume thì giải lại.** 3 bài Best-of-16 của qwen25c7b được giải lại; kết quả lần đầu được lưu riêng. Không sửa code giữa đợt, vì sửa sẽ làm đổi `source_hash` và chặn resume mọi run. Sửa sau đợt: đọc `selected.py` dưới dạng bytes trong `_load_completed`, thêm test hồi quy, rồi bump protocol nếu cần.
3. **Đổi thứ tự hàng đợi** của seedcoder8b và qwen35_9b: các run ngắn trước, MCTS APPS sau cùng. Việc này không ảnh hưởng kết quả.
4. **Tạm dừng qwen35_9b** (người dùng đồng ý sau khi thử lại lúc 10:35–11:03): với tuổi thọ runtime khoảng 23 phút và thời gian khởi động 9 phút, MCTS không tiến được. Chưa quyết định chạy lại vào lúc khác hay chỉ báo cáo 2 model.
5. **Lưu trữ artifact.** Các file nặng của từng bài được nén theo run trong `runs/v3_raw_archives/`, phần còn lại commit trực tiếp.
6. **Phân tích** dùng [analyze_v3.py](../../scripts/analyze_v3.py): McNemar exact với Holm, bootstrap ghép cặp, chọn lại offline (bỏ critic, dừng sớm) và Best-of-k từ k mẫu đầu, chấm lại hidden trên máy local. Kết quả cho 2 model: [docs/results/v3/analysis_qwen25c7b_seedcoder8b.json](../results/v3/analysis_qwen25c7b_seedcoder8b.json). Đây là quan sát, chưa phải kết luận của đề tài.

## D-009: Gỡ kết quả trước v3, bỏ 14B (13/11/2026)

Người dùng thấy các kết quả cũ không chính xác và gây nhầm lẫn, nên đã quyết định:
1. **Gỡ toàn bộ tài liệu trước v3 khỏi nhánh:** run 14B v1, tuning, demo, nhánh 7B cũ (`external/ReThinkMCTS`), các chương báo cáo 01–06, config, script, prompt `native_v2`, dữ liệu `prepared/apps`. Tất cả vẫn lấy lại được ở tag `archive/pre-v3-2026-11-13` và trong `~/TLCN_archive_pre_v3/`. Nguồn số liệu duy nhất là [BENCHMARK_LEDGER.md](../results/BENCHMARK_LEDGER.md) cùng `docs/results/v3/`.
2. **RQ5 chỉ còn ở dạng mô tả:** các lỗi của cài đặt cũ và cách v3 sửa. Không dùng số liệu v1. Bỏ phụ lục A và mục tham khảo 14B/7B trong khung báo cáo.
3. **Bỏ E7 (14B theo v3).** Ba model 7–9B là phạm vi duy nhất.
4. **MCTS APPS của Qwen3.5-9B chạy tiếp trên Colab** từ bản lưu 116/300 khi Colab ổn định, thay vì chạy lại từ đầu trên Modal. Các run Qwen3.5 khác chạy trên Modal (D-008, ledger mục 12).

## D-010: Giữ kết quả Qwen3.5-9B APPS dù output bị cắt (14/11/2026)

Bối cảnh: trên APPS, `qwen35_9b` (tắt thinking) có khoảng 26–29% lời gọi `code` bị cắt ở giới hạn 4.096 token ở cả ba phương pháp. Riêng MCTS có 17 bài không có candidate vì expansion ở gốc bị cắt ở 1.024 token ([BENCHMARK_LEDGER.md](../results/BENCHMARK_LEDGER.md), mục 6.1).

Quyết định (người dùng, 14/11/2026): **giữ nguyên protocol v3.1 và kết quả hiện có, không chạy lại.** Lý do: kết quả nhìn chung hợp lý, và cả ba phương pháp dùng cùng giới hạn token nên so sánh ghép cặp trong model vẫn cùng cấu hình. Việc output bị cắt (và việc chỉ MCTS mất trắng bài khi expansion bị cắt) được ghi vào threats to validity của báo cáo, cùng với việc ô APPS chạy trên hai nền tảng (Modal và Colab).
