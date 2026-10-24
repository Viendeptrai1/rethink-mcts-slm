# Bản đồ tài liệu

Thư mục này là bộ nhớ chung giữa người thực hiện và trợ lý. Mục tiêu là giữ rõ ba
loại thông tin: điều đã kiểm chứng, điều đang dự định và điều còn chưa chắc chắn.

## Thứ tự đọc

1. [project-status.md](project-status.md): trạng thái thực tế mới nhất và bước kế tiếp.
2. [plan.md](plan.md): roadmap, phạm vi từng giai đoạn và điều kiện hoàn thành.
3. [theory-rethinkmcts.md](theory-rethinkmcts.md): thuật toán từ paper nền tảng.
4. [rethinkmcts/README.md](../rethinkmcts/README.md): thuật toán native từng bước và chi phí mỗi node.
5. [rethinkmcts-implementation.md](rethinkmcts-implementation.md): kiến trúc bản native và khác biệt với repo gốc.
6. [datasets.md](datasets.md): quyết định sử dụng APPS và HumanEval; [dataset-report.md](dataset-report.md): báo cáo cấu trúc, schema và cohort đã kiểm tra.
7. [baseline-direct.md](baseline-direct.md): baseline đưa đề bài cho LLM và nhận code; [baseline-report.md](baseline-report.md): mô tả triển khai, prompt và protocol benchmark.
8. [executors.md](executors.md): chạy code và tính số test pass cho từng dataset.
9. [pipeline-direct.md](pipeline-direct.md): generation trước, evaluation song song sau.
10. [environment.md](environment.md): virtual environment và dependency.
11. [implementation-audit.md](implementation-audit.md): khoảng cách giữa paper và code.
12. [llm-provider.md](llm-provider.md): cấu hình Ollama/Modal và quy tắc sử dụng API.
13. [decisions.md](decisions.md): các quyết định đã chốt và lý do.
14. [theory-rap.md](theory-rap.md): đối chiếu khái niệm với RAP, không phải baseline chính.
15. [gpu/README.md](gpu/README.md): thông tin instance CKEY, Ollama và kế hoạch chạy GPU thuê.
16. [runbooks/README.md](runbooks/README.md): hướng dẫn thao tác generation/evaluation và smoke test.
17. [runbooks/benchmark-v2.md](runbooks/benchmark-v2.md): cohort 300+164 và lệnh evaluation cho run mới.
18. [runbooks/remote-evaluation.md](runbooks/remote-evaluation.md): chạy judge trên CPU máy thuê, không dùng worker laptop.
19. [benchmark-results.md](benchmark-results.md): hồ sơ tham số và bảng benchmark bất biến theo run/model.
20. [runbooks/gpu-generation.md](runbooks/gpu-generation.md): tự kiểm tra/tải model Ollama qua SSH tunnel trước direct generation.
21. [runbooks/remote-mcts.md](runbooks/remote-mcts.md): đóng gói, smoke và resume MCTS trên GPU thuê.
22. [runbooks/modal-mcts.md](runbooks/modal-mcts.md): inference Modal L4 với judge cục bộ.
23. [results/rethinkmcts-modal-humaneval-v1.md](results/rethinkmcts-modal-humaneval-v1.md): kết quả HumanEval 164 đã kiểm chứng; APPS còn dở.
24. [results/rethinkmcts-modal-benchmark-v2-adjudicated.md](results/rethinkmcts-modal-benchmark-v2-adjudicated.md): bảng APPS 300 + HumanEval 164 với ba APPS technical failure được tính 0 có ghi provenance.
25. [results/direct-baseline-benchmark-v2.md](results/direct-baseline-benchmark-v2.md): bảng direct baseline chấm lại trên cùng 300 APPS + 164 HumanEval.
26. [results/benchmark-v2-all-tests.md](results/benchmark-v2-all-tests.md): bảng chính thức chấm toàn bộ APPS tests cho baseline và MCTS.
27. [results/rethinkmcts-apps-0395-native-v2-smoke.md](results/rethinkmcts-apps-0395-native-v2-smoke.md): pilot APPS sai ở run cũ và pass 53/53 sau sửa prompt.
28. [results/rethinkmcts-apps-ast-repair.md](results/rethinkmcts-apps-ast-repair.md): nguyên nhân AST crash, fix, hai repair run và giới hạn của phép ghép 297/300.
29. [results/rethinkmcts-apps-native-v2-w4-retry.md](results/rethinkmcts-apps-native-v2-w4-retry.md): run gốc sau retry, rejudge all-tests 295/300 APPS candidate native_v2.
30. [results/rethinkmcts-apps-native-v2-w4-provisional.md](results/rethinkmcts-apps-native-v2-w4-provisional.md): snapshot lịch sử trước retry, 286/300 APPS candidate.
31. [runbooks/rethinkmcts-test-only-ablation.md](runbooks/rethinkmcts-test-only-ablation.md): ablation reward chi dung public-test pass rate, khong goi LLM self-evaluation.
32. [results/rethinkmcts-test-only-v1.md](results/rethinkmcts-test-only-v1.md): bang ablation `test_only`, artifact, do phu va cac bai timeout.
33. [rethinkmcts-dual-report.md](rethinkmcts-dual-report.md): triển khai, prompt và hyperparameter benchmark dual.
34. [rethinkmcts-test-only-report.md](rethinkmcts-test-only-report.md): triển khai, prompt và hyperparameter benchmark test-only.
35. [runbooks/trace-viewer.md](runbooks/trace-viewer.md): mở web local để xem cây search và trace artifact theo từng problem.
36. [runbooks/rethinkmcts-external-evaluator-pilot.md](runbooks/rethinkmcts-external-evaluator-pilot.md): chạy Dual với evaluator Qwen 14B riêng, APPS pilot 30 + HumanEval 164 trên Modal.

## Source of truth

| Nội dung | File chịu trách nhiệm |
|---|---|
| Trạng thái hiện tại, blocker, bước tiếp theo | `docs/project-status.md` |
| Roadmap và phạm vi từng giai đoạn | `docs/plan.md` |
| Công thức/thuật toán RethinkMCTS | `docs/theory-rethinkmcts.md` |
| Diễn giải từng bước của bản native và chi phí mỗi node | `rethinkmcts/README.md` |
| Kiến trúc implementation native và khác biệt với repo gốc | `docs/rethinkmcts-implementation.md` |
| Dataset nào được dùng và vì sao | `docs/datasets.md` |
| Cohort benchmark mới và ID cố định | `data/samples/benchmark_v2/` |
| Cấu trúc file, schema và cách load dữ liệu | `data/README.md` |
| Hành vi và cách chạy direct-generation baseline | `docs/baseline-direct.md` |
| Giao diện, cách chấm và giới hạn an toàn của executor | `docs/executors.md` |
| Pipeline generation/evaluation và artifact tổng hợp | `docs/pipeline-direct.md` |
| Python environment và dependency | `docs/environment.md` |
| Trạng thái implementation và điểm chưa rõ | `docs/implementation-audit.md` |
| Provider, biến môi trường và quy tắc gọi LLM | `docs/llm-provider.md` |
| Quyết định kiến trúc/phạm vi đã chốt | `docs/decisions.md` |
| Lệnh vận hành benchmark theo từng bước | `docs/runbooks/baseline-full.md` |
| Metric Pass Rate/Pass@1 và bảng judge | `evaluation/benchmark_judge.py` |
| Lưu trữ, schema và so sánh các bảng benchmark | `docs/benchmark-results.md` |
| Public tests HumanEval dùng trong search | `data/humaneval/public_tests.jsonl` và `public_tests_source.json` |
| Batch/cohort/resume MCTS | `rethinkmcts/batch.py` |
| Bảng MCTS và provenance | `rethinkmcts/benchmark.py` |
| Báo cáo APPS pilot n=30 với evaluator riêng | `rethinkmcts/pilot_benchmark.py` |
| Web đọc lại cây search và event trace | `tools/trace_viewer/` |

Không sao chép toàn bộ cùng một nội dung sang nhiều file. File khác chỉ nên tóm tắt
và liên kết tới source of truth tương ứng.

## Quy ước trạng thái

Các tài liệu dùng ba nhãn sau:

- **Đã kiểm chứng**: đã đọc trực tiếp từ file, chạy lệnh hoặc đối chiếu nguồn gốc.
- **Giả thuyết**: suy luận hợp lý nhưng chưa xác nhận bằng code/chạy thử.
- **Cần xác minh**: câu hỏi mở phải kiểm tra trước khi triển khai.

Khi trạng thái thay đổi, cập nhật `project-status.md` trong cùng task. Khi một quyết
định thay đổi phạm vi hoặc kiến trúc, cập nhật thêm `decisions.md` và các tài liệu
chịu ảnh hưởng.

## Quy tắc tránh tài liệu lỗi thời

- Mỗi dữ kiện chỉ có một file chịu trách nhiệm chính.
- Đường dẫn, số lượng mẫu và trạng thái code phải được kiểm tra trực tiếp.
- Không đánh dấu hoàn thành chỉ vì file/thư mục tồn tại.
- Không âm thầm sửa khác biệt giữa paper và code; ghi vào audit trước.
- Sau khi đổi tên/di chuyển file, tìm tên cũ trên toàn workspace.
