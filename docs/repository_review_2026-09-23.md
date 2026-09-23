# Đánh giá repository và hướng phát triển tiểu luận

Ngày rà soát: 23/09/2026. Đánh giá working tree hiện tại, gồm cả thay đổi chưa commit; HEAD tại thời điểm rà soát: `9bf04c4`. Đây là báo cáo quan sát và đề xuất, không phải chứng nhận tái lập đầy đủ bài báo hay quyết định đã chốt về phương pháp mới.

## 1. Kết luận và mục tiêu của chủ đề tài

Repository đang hiện thực lại và điều chỉnh **RethinkMCTS** cho mô hình sinh mã 7B–14B. Lõi có thật: tìm kiếm trên thought, P-UCB, max backup, dual reward, thay thought ở lá và sinh lại chương trình. Tuy nhiên, còn khoảng cách giữa đặc tả, mã chạy thực tế và những khẳng định trong báo cáo kết quả. Cách mô tả phù hợp hiện tại là **bản tái hiện có điều chỉnh, đã có thực nghiệm sơ bộ**.

Thông tin người dùng xác nhận trong phiên này:

- Còn khoảng 2 tháng đến hạn nộp.
- Muốn có đóng góp riêng ngoài tái hiện bài báo; quan tâm việc ghi nhận nguồn và tránh đạo văn.
- Ngân sách GPU không phải ràng buộc chính.

Đổi backbone sang mô hình nhỏ có giá trị thực nghiệm nhưng tự nó chưa tạo ra thuật toán mới. Tái hiện có trích dẫn và phân định đóng góp là hoạt động nghiên cứu hợp lệ; không được trình bày thought-level MCTS, leaf rethink, block feedback hoặc dual evaluation như phát minh của đề tài. Đánh giá học thuật cuối cùng còn phụ thuộc yêu cầu của giảng viên; phiên này không thực hiện kiểm tra tương đồng văn bản toàn văn.

## 2. Phạm vi kiểm tra

Rà soát các tầng source, cấu hình, prompt, adapter dữ liệu/thực thi/LLM, runner, báo cáo, test, deployment và tài liệu phương pháp. Source có 54 file Python, khoảng 5.625 dòng; test có 11 file. Dữ liệu và artifacts được kiểm tra bằng thống kê, đối chiếu từng bài và truy vết mẫu, không đọc thủ công từng chương trình trong mọi run. Tài liệu tổng hợp lớn `Agentic_AI.md` không được thẩm định toàn văn như một nguồn học thuật.

- Chạy `python3 -m pytest -q`: **36 passed in 1.09s**.
- Đối chiếu 792 file `judge_results.json` thuộc 6 run chính với summary; số bài đúng khớp.
- Kiểm tra hash của 792 `selected.py` theo đúng `ProgramCandidate.compute_hash`: tất cả khớp hash lưu trong kết quả judge.
- Chạy các probe cục bộ với gateway giả và chương trình tổng hợp để xác minh lỗi chi phí, sampling, tracing và TLE.
- Không gọi endpoint sinh mã thật, triển khai GPU, chạy lại toàn bộ hidden judge hay sửa thuật toán trong phiên review.

## 3. Bản đồ hệ thống và mức độ bám bài báo

| Phần | Vị trí | Trạng thái quan sát |
|---|---|---|
| Cây thought và revision | `src/rethink_mcts/domain/tree.py` | Có node, revision, reset thống kê lá, giữ lịch sử tổ tiên |
| Điều phối tìm kiếm | `application/search.py` | Có expand → generate → public evaluate → rethink → backup |
| P-UCB, max backup, dual reward | `policies/` | Đã hiện thực và có unit tests |
| Public/hidden | `domain/problem.py`, `application/judge.py` | Tách đối tượng dữ liệu và chọn chương trình trước khi judge |
| LLM endpoint | `adapters/llm/` | HTTP tương thích OpenAI, Jinja prompts, parser, transport retry |
| Feedback | `application/feedback.py`, `adapters/execution/` | Có facts, CFG, trace, block analyzer; còn lỗi quan trọng bên dưới |
| Baseline | `application/baselines.py` | Direct và Best-of-N; chưa có iterative repair/Self-Refine hoàn chỉnh |
| Hướng graph | `application/graph_solver.py` | Pipeline analyze/drafts/aggregate/patch; run hiện có chỉ trên 21 bài chọn lọc |
| Dữ liệu | `prepared/` | 164 HumanEval; 300 APPS gồm 100 bài mỗi mức khó, tất cả APPS hiện tại là stdin |
| Serving | `deploy/modal_vllm.py` | Có cấu hình Modal/vLLM, mặc định H200; không pin phiên bản chính xác |
| Persistence | `adapters/storage/filesystem.py` | Có API checkpoint/event nhưng luồng chạy chính chưa tích hợp đầy đủ |

RAP là tài liệu nền/baseline liên quan; code hiện tại không phải một bản RAP hoàn chỉnh. CodeContests có adapter nhưng chưa có bộ thực nghiệm tương đương HumanEval/APPS trong artifacts đã kiểm tra.

Sai khác đáng chú ý với RethinkMCTS: bài báo dùng verbal feedback cho cả **expansion** và **rethink**, nhưng `search.py` luôn truyền `feedback=None` khi expansion; `SemanticPromptedLLM.propose()` cũng chưa render feedback. Cấu hình `paper_reference.yaml` trỏ đến `prompts/paper_v1`, thư mục này chưa tồn tại. Vì vậy chưa thể gọi profile này là chế độ tái lập paper đã chạy được.

Nguồn đối chiếu: [RethinkMCTS, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.410/), bản trích xuất `Rethink_extracted.md` trong repo, và [repository tác giả](https://github.com/SIMONLQY/RethinkMCTS). Trong báo cáo nên dùng trích dẫn hội nghị năm 2025 thay cho cách ghi mơ hồ “2024/2025”.

## 4. Kết quả đã lưu và giới hạn diễn giải

| Benchmark | Direct | Best-of-3 | RethinkMCTS | Calls ghi nhận: Direct / BoN / MCTS |
|---|---:|---:|---:|---:|
| HumanEval, 164 bài | 148/164 = 90,24% | 150/164 = 91,46% | 153/164 = 93,29% | 314 / 947 / 747 |
| APPS Introductory, 100 bài | 21% | 23% | 30% | 127 / 379 / 1.158 |

Nguồn: `runs/{humaneval,apps_intro}_{direct,bon3,mcts}_14b/`, đối chiếu với `results/*_benchmark_summary.json`. Đây là số liệu artifacts đã có, chưa được tái chạy trong phiên này. Nhận diện checkpoint 14B dựa trên cấu hình và tên run; artifacts chưa có manifest đủ để chứng minh cấu hình hiệu lực cho mọi bài.

Những điều cần sửa trong diễn giải:

- HumanEval tăng **3,05 điểm phần trăm**, APPS Introductory tăng **9 điểm phần trăm** so với Direct; cần ghi đúng đơn vị.
- MCTS thắng Direct trên 9 bài HumanEval nhưng thua lại 4 bài; APPS tương ứng 11 thắng, 2 thua. Phải phân tích cả regression.
- “MCTS giải đúng bài Direct giải sai” không đồng nghĩa “rethink sửa thành công”. Trong 9 bài thắng ở HumanEval, chỉ 4 chương trình được chọn mang `origin=rethink`; 5 mang `origin=initial`. APPS tương ứng 5 và 6. Nhãn origin chưa chứng minh hoặc bác bỏ ảnh hưởng gián tiếp của rethink ở tổ tiên; cần trajectory để kết luận cơ chế.
- “Direct Greedy” chưa đúng với source hiện tại: code generation đặt cứng `temperature=0.2`.
- “Tiết kiệm hơn 21% chi phí” được suy từ calls, trong khi calls thiếu block analysis, chưa có token tổng và độ dài mỗi call khác nhau. Chưa đủ căn cứ kết luận tiết kiệm compute.
- `elapsed_seconds` trong batch summary chỉ đo phiên chạy hiện tại. HumanEval MCTS có 11 bài resumed: summary 2.640,6s, tổng thời gian từng bài 3.433,9s. APPS MCTS có 81 bài resumed: summary 1.401,5s, tổng từng bài 8.674,7s. Không dùng summary này như tổng thời gian toàn benchmark. Thời gian từng bài còn gồm cả hidden judging.
- HumanEval đóng gói official test thành một `AssertionSuite`: hidden pass rate ở đây là kết quả của toàn suite, không phải tỷ lệ từng assertion.
- Các bảng chính chưa có lặp nhiều seed hay confidence interval. Chênh lệch điểm ước lượng không tự chứng minh ưu thế ổn định hoặc nguyên nhân do từng thành phần.

## 5. Những việc phải sửa trước thực nghiệm cuối

### P0 — Chi phí và cấu hình chưa phản ánh lệnh chạy thật

`adapters/llm/semantic.py` đặt cứng nhiệt độ và giới hạn token từng role; `bootstrap.py` không truyền `config.sampling`. `experiment.seed` chưa được nối vào request/payload. Gateway đọc token usage nhưng các semantic methods bỏ thông tin này; `BudgetManager` thường nhận giá trị token mặc định 0. `FeedbackService` gọi block analyzer mà không ghi budget. `max_search_iterations` được khai báo nhưng chưa được kiểm soát bởi vòng lặp.

Probe kiểm chứng: đặt call cap 4, code cap 2, sampling code `(temperature=0.99, max_output_tokens=99)`. Gateway thực nhận 5 calls theo thứ tự `expansion, code, block_analysis, rethink, code`; usage chỉ ghi 4. Gateway trả tổng 75 token giả lập, usage ghi 0. Sampling code thực tế vẫn `(0.2, 1536)`.

Hướng sửa: accounting tại gateway cho mọi role/retry; reservation trước request; lưu usage đầy đủ; token không đo được phải là missing/null thay vì 0; truyền sampling và ghi seed support thực tế. Kiểm tra call/time/sandbox cap tại ranh giới hoạt động, thay vì chỉ đầu vòng lặp.

### P0 — Tracing chưa tái chạy đúng ca kiểm thử hàm

`adapters/execution/tracing.py:200` chỉ `exec(compiled_code, sandbox_globals)`, không gọi entry point với `FunctionCase`, không chạy test harness của `AssertionSuite`. Với HumanEval chỉ định nghĩa hàm, trace có thể báo success dù chưa vào thân hàm. Probe hàm `f(x)` xác nhận chỉ có một module visit và không thấy biến tham số `x`.

Ngoài ra, `SemanticPromptedLLM.analyze()` chỉ đưa source snippet vào prompt phân tích block, bỏ trạng thái biến. Prompt rethink có formatter delta biến, nhưng đó không thay thế phần input thiếu của analyzer. Feedback facts chưa xử lý riêng `AssertionSuite` để ghi input/expected rõ ràng. Timeout của tracer được khai báo nhưng chưa thực thi; trace chạy trong chính tiến trình điều phối. CFG mapping chưa định danh offset theo từng code object; trạng thái frame tracing cần kiểm chứng chặt hơn cho đệ quy.

Hướng sửa: dùng chung hợp đồng harness giữa evaluate và trace; tách worker có timeout; map `(code_object, offset)` và frame stack; gửi snapshot đã giới hạn tới analyzer; kiểm thử lỗi thật trong function/assertion/loop/recursion. Sửa lỗi này là khôi phục fidelity, chưa phải đóng góp phương pháp mới.

### P0 — Bộ chấm và sandbox chưa đồng nhất

- `DockerExecutor` chưa dùng `wrap_code_for_execution`; function/assertion suites không được chạy như host executor. Với assertion, có nguy cơ chỉ chạy định nghĩa hàm rồi chấp nhận output rỗng.
- Bootstrap cho phép tự chuyển từ Docker sang host nếu thiếu binary. Tracing vẫn ở host. Chưa thể mô tả toàn pipeline là sandbox cô lập.
- Host executor gặp một test TLE sẽ gán toàn bộ test còn lại là TLE. Probe hai đầu vào `slow` và `fast` cho kết quả `[TLE,TLE]`, nhưng chạy riêng `fast` thì AC. Cách này có thể giữ kết luận “không pass toàn bộ”, nhưng làm sai mean hidden pass rate.
- `HiddenJudge` chưa chấm `generated_cases` của CodeContests. Không được báo đã hỗ trợ đầy đủ metric này.

Hướng sửa: đồng nhất harness/container, không âm thầm fallback khi benchmark; phân biệt fail với skipped/incomplete; chạy đủ ca khi công bố partial pass rate; pin runtime và comparator protocol. Các lỗi Docker không được suy diễn là nguyên nhân trực tiếp của bảng cũ vốn dùng host.

### P1 — Protocol dữ liệu và tái lập cần khóa lại

APPS adapter lấy 2 test đầu làm public, phần còn lại làm hidden; đây là quy tắc tự đặt và phải ghi deviation, chưa chứng minh trùng mapping của paper. Nhánh `len(all_cases)<=2` dùng lại public làm hidden. Không phát hiện exact-case overlap trên **300 bài đã chuẩn bị hiện tại**, nên đây là lỗi tiềm ẩn adapter, không phải bằng chứng bộ hiện tại đã bị leakage theo nhánh đó. Kiểm tra này cũng không chứng minh không có mọi dạng leakage khác.

Batch resume chỉ kiểm tra tồn tại `selected.py` và `judge_results.json`; không xác thực model/config/prompt/dataset/code revision. Chưa có bằng chứng chắc chắn các bài đã trộn cấu hình, nhưng hệ thống không ngăn hoặc xác minh được điều đó. Manifest hiện tại chỉ có đường dẫn, số bài và mô tả provenance chung; cần hashes và nguồn phiên bản cụ thể.

`save_checkpoint`, `append_event` và execution cache có implementation nhưng chưa nối đầy đủ vào luồng solve/batch. Các run kiểm tra chưa có checkpoint, event log, raw responses hay trace artifacts dù config có cờ lưu. Seed, môi trường, model revision và prompt hash cần đi cùng mỗi run.

### P1 — Ablation và baseline chưa đủ để giải thích kết quả

- `search.backup` có cấu hình nhưng bootstrap luôn tạo `MaxBackupPolicy`; đổi YAML sang mean chưa tạo ra mean backup.
- `feedback.mode=none` vẫn tạo execution facts, sau đó refiner nhận chúng; chưa phải ablation “không verbal feedback”.
- Chưa có iterative code repair baseline để tách lợi ích của feedback khỏi lợi ích của tree search.
- Đặt `llm_weight=0` chưa đủ đảm bảo tắt critic call; cần một ablation thật sự không gọi critic.
- Graph run trên 21 bài chọn lọc chỉ là phân tích thăm dò; không so 6/21 với kết quả full benchmark và không dùng lại tập này làm kiểm định độc lập sau tuning.

36 tests hiện có là nền tốt nhưng chưa bao phủ các lỗi trên. Ví dụ test checkpoint tự gọi storage, chưa chứng minh runner thực sự checkpoint/resume; test leakage chủ yếu kiểm tra object, chưa kiểm tra toàn bộ prompt/worker/artifact boundary.

## 6. Đóng góp riêng được đề xuất — chưa chốt tính mới

Tên làm việc: **“Nghiên cứu cơ chế lựa chọn phản hồi thực thi thích ứng cho tìm kiếm sinh mã với mô hình ngôn ngữ quy mô nhỏ.”**

Câu hỏi trung tâm: **Với từng kích thước mô hình và loại lỗi, khi nào facts ngắn đã đủ, khi nào cần runtime trace, và khi nào cần thêm LLM phân tích block?**

Giả thuyết cần kiểm chứng: feedback chi tiết hơn không luôn đem lại lợi ích tương xứng; lựa chọn mức feedback theo loại lỗi và tiến triển public tests có thể cải thiện quan hệ độ chính xác–chi phí. Chưa có bằng chứng từ repo để khẳng định giả thuyết này đúng.

Một thay đổi phương pháp đủ hẹp để triển khai trong 8 tuần:

1. Định nghĩa ba mức feedback: facts; facts + trace; facts + trace + analysis.
2. Bộ chọn mức chỉ dùng thông tin public: loại lỗi, biến động pass rate, lặp lại code/lỗi và lịch sử sửa của bài hiện tại. Không dùng hidden verdict của bài đang giải.
3. Thử chính sách tăng mức khi sửa không tiến triển; ngưỡng chọn trên development set riêng. Giữ các thành phần MCTS khác cố định để cô lập tác dụng.
4. So với mọi mức cố định, simple iterative repair và RethinkMCTS baseline đã sửa fidelity; báo cả accuracy, regression và toàn bộ token theo role.

Đóng góp hướng tới gồm: (a) phân tích thực nghiệm tương tác kích thước mô hình × loại feedback × loại lỗi; (b) chính sách chọn feedback mô tả rõ và tái lập được; (c) đánh giá ngang ngân sách, ablations và phân tích thất bại. Nếu chính sách không thắng, kết quả âm và bản đồ điều kiện có/không có lợi vẫn có giá trị phân tích, nhưng không được viết thành tuyên bố cải tiến đã thành công.

SLM cần được định nghĩa theo phạm vi đề tài, không giả định có ngưỡng chuẩn duy nhất. Có thể dùng Qwen2.5-Coder-Instruct **3B và 7B làm trọng tâm**, **14B làm mốc đối chiếu**, cùng họ để giảm yếu tố nhiễu; không tuyên bố đây là dòng mới nhất. Các kích thước này có trong [công bố chính thức Qwen2.5-Coder](https://qwenlm.github.io/blog/qwen2.5-coder-family/). Cùng họ vẫn không loại bỏ mọi khác biệt huấn luyện, nên tránh kết luận nhân quả tuyệt đối chỉ từ số tham số.

## 7. Đối chiếu nghiên cứu gần và cách ghi nhận nguồn

Tra cứu ban đầu đến 23/09/2026 cho thấy hướng tổng quát đã có prior work; đây chưa phải systematic literature review hay xác nhận novelty toàn cầu:

| Nguồn | Liên quan và hệ quả cho đề tài |
|---|---|
| [RethinkMCTS — EMNLP 2025](https://aclanthology.org/2025.emnlp-main.410/) | Nền thought search/rethink; phải trích dẫn và phân định phần kế thừa |
| [Reason-Code — ACL Industry 2026](https://aclanthology.org/2026.acl-industry.30/) | Đã có execution-guided MCTS và conditional budget khi greedy thất bại; chỉ thêm cơ chế này chưa đủ khác biệt |
| [Feedback Over Form — preprint 2026](https://arxiv.org/abs/2604.21950) | Nghiên cứu pipeline/feedback trên 1–3B, báo lợi ích phụ thuộc loại lỗi; cần so với simple repair và kiểm tra đúng điều kiện áp dụng |
| [Learning How Hard to Think](https://arxiv.org/abs/2410.04707) | Adaptive allocation đã là hướng nghiên cứu; tránh nhận ý tưởng “phân bổ compute thích ứng” nói chung là mới |

Tuần đầu cần đọc toàn văn các nguồn gần, bổ sung LDB và nghiên cứu chọn/thu gọn feedback, lập bảng **đã có / khác biệt cụ thể / bằng chứng phải thu**. Không đặt tên thuật toán mới rồi coi tên đó là bằng chứng đóng góp.

Trong báo cáo nên có bảng provenance: cơ chế kế thừa từ paper, module tự hiện thực, code/dataset bên ngoài có sử dụng, và thay đổi đề xuất. Tự diễn giải nội dung đã hiểu, dẫn nguồn cho thuật toán/công thức/hình; không nhận bảng kết quả paper làm kết quả của mình. Giữ attribution và thông tin nguồn cho phần tái sử dụng. Việc ghi nhận công cụ AI hỗ trợ viết/code cần theo quy định của môn học.

## 8. Lộ trình 8 tuần đề xuất

| Tuần | Công việc | Điều kiện hoàn thành |
|---|---|---|
| 1 | Chốt câu hỏi, đọc prior work gần, khóa phạm vi với giảng viên; xác định development/final cohort | Bảng đóng góp và protocol ngắn; phân biệt exploratory data đã xem với test dành riêng |
| 2 | Sửa accounting, config, harness, tracing, resume; chuẩn hóa baseline | Regression tests cho lỗi review; request/usage thật khớp; artifacts đủ tái lập |
| 3 | Hiện thực các mức feedback và controller đơn giản; thêm iterative repair | Policies thay được bằng config; kiểm tra prompt thực sự khác đúng một yếu tố |
| 4 | Pilot trên development set, 3B/7B; kiểm tra hiệu ứng và failure modes | Chọn controller/ngưỡng bằng development; khóa trước final; nếu không có tín hiệu thì thu hẹp đóng góp |
| 5–6 | Thực nghiệm chính và ablations trên 3B/7B/14B, ít nhất 3 seeds | So cùng code budget và cùng token budget; báo CI/paired comparison, accuracy và chi phí |
| 7 | Phân tích regression, trace case studies, viết kết quả và giới hạn | Bảng/biểu đồ sinh từ artifacts; kết luận chỉ trong phạm vi dữ liệu |
| 8 | Hoàn thiện báo cáo, demo, slide và đóng gói tái lập | Một lệnh chạy smoke; env/config/data/prompt hashes; đối chiếu toàn bộ claim với bằng chứng |

APPS nên là benchmark chính vì kết quả hiện tại còn nhiều dư địa; HumanEval dùng làm đối chiếu. Nếu dùng APPS train làm development và APPS test làm final phải ghi rõ ID/revision; các bài test đã xem và dùng để sửa phương pháp cần được khai báo là exploratory. Có thể mở rộng final cohort chưa dùng để tune. Chỉ thêm benchmark thứ ba sau khi pipeline hai bộ chính đáng tin cậy.

Mỗi thí nghiệm phải lưu: cohort, model revision, serving/runtime version, effective config, seed support, prompt hash, git revision và dirty diff, requests/responses, usage theo role, candidate/evaluation/selection, trace/feedback, stop reason và hidden judge sau đóng băng. GPU không thiếu vẫn cần ngân sách so sánh ngang nhau để trả lời câu hỏi nghiên cứu.

## 9. Việc nên làm tiếp

Ưu tiên hoàn thiện nền thực nghiệm và chốt nghiên cứu về **lựa chọn mức feedback** trước khi mở rộng sang Graph-of-Thoughts, fine-tuning hoặc RL. Chưa nên chạy thêm hàng loạt để củng cố bảng cũ khi accounting và tracing còn lỗi. Báo cáo này lưu các phát hiện hiện tại; chưa sửa `Proposal.md`, source hay dữ liệu thí nghiệm.
