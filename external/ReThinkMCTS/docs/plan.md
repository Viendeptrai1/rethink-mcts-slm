# Kế hoạch dự án

## Nguyên tắc phạm vi

Baseline phải chạy được và được quan sát trước khi phát triển biến thể. Mọi thử
nghiệm API bắt đầu bằng 1-2 bài và rollout thấp để kiểm soát chi phí.

## Kế hoạch 15 tuần

| Tuần | Trọng tâm | Kết quả cần có |
|---:|---|---|
| 1 | Chốt đề tài và câu hỏi nghiên cứu | Phạm vi, mục tiêu, tiêu chí đánh giá |
| 2 | Đọc RethinkMCTS và RAP | Ghi chú lý thuyết, câu hỏi mở |
| 3 | Chuẩn bị APPS và HumanEval | Dataset load được, schema được mô tả |
| 4 | Lấy và đọc repo RethinkMCTS gốc | Commit hash, sơ đồ module, dependency |
| 5 | Dựng môi trường chạy | Cài đặt tái lập được, loader chạy độc lập |
| 6 | Smoke test baseline | 1-2 bài, rollout thấp, log đầy đủ |
| 7 | Đối chiếu paper với code | Audit các khác biệt và điểm nhập nhằng |
| 8 | Thiết lập baseline đo lường | Protocol, seed, metric, lưu artifact |
| 9 | Thiết kế đóng góp | Đặc tả reward/feedback mới, chưa code vội |
| 10 | Prototype có kiểm thử | Thay đổi nhỏ, test executor và reward |
| 11 | Tích hợp vào search | Chạy end-to-end trên tập nhỏ |
| 12 | Thử nghiệm chính | Baseline và phương pháp đề xuất |
| 13 | Ablation và phân tích lỗi | Bảng kết quả, case study |
| 14 | Viết báo cáo | Phương pháp, thực nghiệm, thảo luận |
| 15 | Hoàn thiện | Rà soát tái lập, slide và phụ lục |

## Giai đoạn hiện tại

Đang ở **Modal RethinkMCTS benchmark - HumanEval hoàn tất, APPS tạm dừng**.
Direct baseline đã hoàn tất; native package có tree, P-UCB, expansion, code
evaluation, dual evaluation reward, feedback, rethink, backpropagation và
artifact writer. HumanEval 164/164 đã chạy thật với Ollama trên Modal L4 và
judge cục bộ; xem `docs/results/rethinkmcts-modal-humaneval-v1.md`. APPS mới
có 1/300 bài smoke. Bước kế tiếp là resume APPS khi người dùng yêu cầu, rồi
đóng băng bảng 300+164. Bundle Docker/CKEY là workflow khác, chưa chạy thật.

### Definition of Done cho direct-generation baseline

- Loader đọc được một bài APPS hoặc HumanEval mà không đọc đáp án/test.
- Prompt yêu cầu model chỉ trả complete Python code.
- Mỗi lệnh gửi tối đa một bài và một request.
- Raw response, code và metadata usage được lưu thành artifact.
- Có dry-run để xem prompt mà không gọi API.
- Bước sinh code không tự thực thi candidate; việc chấm thuộc package `Executors`.

### Definition of Done cho executor baseline

- APPS hỗ trợ cả `stdin_stdout` và `call_based`.
- HumanEval chạy nguyên official harness bằng đúng `entry_point`.
- Báo cáo có số test pass, tổng test, pass rate, lỗi và thời gian chạy.
- Mỗi test/harness có timeout và không làm treo tiến trình benchmark.
- Có unit test offline cho pass, wrong answer và timeout.
- Giới hạn bảo mật của subprocess runner được ghi rõ.

### Definition of Done cho pipeline direct baseline

- Generation và evaluation là hai checkpoint có thể chạy/resume độc lập.
- Stage `all` chỉ bắt đầu evaluation sau khi toàn bộ generation thành công.
- Evaluation song song theo candidate với số worker cấu hình được.
- Mỗi candidate có `evaluation.json`; mỗi dataset có JSONL, CSV và summary.
- Full run cần xác nhận rõ để tránh gọi API hoặc thực thi hàng loạt ngoài ý muốn.
- Pipeline plan và evaluation offline có unit test; smoke Ollama thật vẫn cần chạy.

## Definition of Done cho native RethinkMCTS smoke/baseline

Baseline chỉ được xem là chạy được khi đáp ứng đủ:

- Repo gốc và commit hash được ghi nhận.
- Dependency và lệnh chạy có thể tái lập trong `D:\ReThinkMCTS\venv`.
- Loader đọc đúng một mẫu APPS hoặc HumanEval.
- Executor chạy được public tests với timeout.
- Một lượt search tạo được thought, code, reward và kết quả test dưới namespace
  `outputs/rethinkmcts/`.
- Có bằng chứng rethink được kích hoạt trên ít nhất một trường hợp lỗi, hoặc ghi rõ
  đã thử nhưng chưa kích hoạt với cấu hình nào.
- Log đủ để đối chiếu với sáu pha trong paper.
- Chi phí API và số request được ghi lại, không ghi secret.

## Ngoài phạm vi hiện tại

- Reward phân biệt TLE/MLE.
- Root-cause identification cho thought.
- CodeContests.
- Chạy toàn bộ benchmark hoặc rollout lớn trước khi smoke được duyệt.

## Bối cảnh direct baseline

Direct baseline đã sinh full APPS test và HumanEval test với model
`qwen2.5-coder:7b-instruct` qua Ollama. Judge đã chạy sample lịch sử 100 bài mỗi
dataset trong `data/samples/evaluation_v1/`. Experiment runner mới dùng cohort
`data/samples/benchmark_v2/` (300 APPS + 164 HumanEval); chưa có kết quả MCTS.

