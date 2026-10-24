# Nhật ký quyết định

Các quyết định ở đây được xem là đang có hiệu lực cho tới khi có entry mới thay thế.

## D-027: Modal GPU cho LLM, executor cục bộ

- Ngày: 2026-10-04
- Trạng thái: Đã deploy/smoke thật; HumanEval 164 hoàn tất, APPS tạm dừng.
- Quyết định: Chạy Ollama `qwen2.5-coder:7b-instruct` trên Modal L4 qua private
  Function, giữ MCTS coordinator, dataset, executor và artifact trên laptop theo
  yêu cầu hiện tại. Dùng cohort `benchmark_v2` 300+164, digest model và source
  inference hash trong run config, resume theo problem.
- Giới hạn: Code do LLM sinh vẫn chạy trong subprocess trên laptop, không phải
  sandbox bảo mật. Full chỉ chạy sau smoke hai bài và kiểm tra phí.

## D-026: Batch RethinkMCTS trên GPU thuê

- Ngày: 2026-10-04
- Trạng thái: Chuẩn bị offline; cần xác minh Docker và smoke trên instance mới.
- Quyết định: Gói đúng APPS 300 + HumanEval 164. HumanEval search dùng
  `given_tests` từ nguồn nhóm đối chiếu đã pin commit/SHA, không dùng fallback
  prompt rỗng. APPS search dùng nửa đầu test công khai. D-020 thay thế quy tắc
  chấm cuối: final evaluation chạy toàn bộ APPS tests.
- Batch chạy tuần tự một bài tại một thời điểm, mỗi bài trong subprocess có
  trần 900 giây mặc định; kết quả hoàn tất ghi vào `outputs/rethinkmcts/`,
  attempt chưa hoàn tất giữ riêng, resume bỏ qua bài đã hoàn tất.
- Run khóa model, config, source/data/manifest hash và model digest; bảng chỉ
  được đóng băng khi đủ 300+164 bài. `--plan` không gọi model, `--smoke` chỉ
  chạy hai bài, full đòi `--confirm-full-run`.
- Giới hạn: container Docker cô lập cả batch, không cô lập từng candidate
  khỏi mạng hoặc test khác.

## D-025: Tự pull Ollama model cho direct generation qua SSH tunnel

- Ngày: 2026-10-04
- Trạng thái: Đã triển khai và test offline; chờ instance GPU mới để smoke thật.
- Quyết định: Wrapper Windows mở SSH local-forward tới Ollama trên GPU thuê,
  kiểm tra `/api/tags`, chỉ gọi `/api/pull` khi thiếu model, sau đó chạy
  `pipelines --stage generate` với provider/base URL tạm thời. Dataset và
  artifact giữ trên Windows; inference dùng GPU thuê.
- Lý do: Một lệnh đủ chuẩn bị model và generation, không phải tự SSH gõ lệnh,
  không mở API Ollama public hay chuyển toàn bộ dataset.
- Giới hạn: Cần instance có Ollama đang chạy và SSH truy cập được. Đây là
  wrapper direct generation, không dùng cho remote evaluation chỉ chạy CPU.

## D-024: Hồ sơ benchmark bất biến và so sánh cùng protocol

- Ngày: 2026-10-04
- Trạng thái: Đã triển khai offline, chờ run v2 thực tế.
- Quyết định: Giữ output evaluator thô ở `outputs/baselines/evaluations/`, chỉ
  đóng băng run đủ 300+164 tại `outputs/benchmarks/<run>/<model>/`. Ghi manifest
  và dữ liệu test hash, cấu hình generation/evaluation, môi trường Docker,
  candidate hash và metric. Bảng so sánh từ chối cohort/policy/timeout khác.
- Lý do: Truy vết chính xác tham số chạy và tránh so sánh nhầm 100+100 với
  300+164 hoặc ghi đè bảng cũ.
- Giới hạn: Chưa có kết quả v2; MCTS cần adapter candidate riêng khi chạy batch.

## D-023: Chạy evaluation trên CPU máy thuê, artifact tách khỏi laptop

- Ngày: 2026-10-04
- Trạng thái: Chuẩn bị offline; chờ instance mới và kiểm tra Docker.
- Quyết định: Đóng gói đúng cohort `benchmark_v2`, code candidate và test data
  cần thiết; chấm bằng evaluator hiện có trong Docker trên máy thuê, 2 worker
  ban đầu; thu hồi report dưới run name mới.
- Lý do: Không chạy code LLM sinh trên laptop, giới hạn tài nguyên và giữ
  kết quả baseline 100+100 cũ bất biến.
- Giới hạn: Docker chỉ cô lập batch, chưa cô lập từng test; không chuyển secret.
  Nếu instance CKEY không có Docker daemon thì chưa chạy.

## D-022: Khoa cohort benchmark doi chieu APPS 300 + HumanEval 164

- Ngày: 2026-10-04
- Trạng thái: Chấp nhận; thay phạm vi judge/MCTS tương lai trong D-017/D-018.
- Quyết định: Dùng `data/samples/benchmark_v2/apps_test_300.json` với đúng 300
  ID của cohort APPS phân tầng seed 2027 từ nhóm đối chiếu; HumanEval dùng toàn
  bộ 164 bài trong `data/samples/benchmark_v2/humaneval_test_164.json`.
- Lý do: So sánh trên cùng bài toán với nhóm đối chiếu và giữ cohort cố định
  cho các model/MCTS tiếp theo.
- Ràng buộc: Không thay đổi `evaluation_v1` hay gán số liệu baseline 100+100
  cho cohort mới. Generation full vẫn độc lập với judge. Khi so kết quả giữa
  hai project, cần thống nhất cả public/hidden test policy, không chỉ ID.
- Nguồn: https://github.com/Viendeptrai1/rethink-mcts-slm/blob/main/data/cohorts/apps_benchmark_300.json

## D-021: LangGraph điều phối, Pydantic kiểm tra hợp đồng native

- Ngày: 2026-10-04
- Trạng thái: Chấp nhận
- Quyết định: Dùng một `StateGraph` tuần tự cho các pha search; dùng Pydantic
  để kiểm tra `WorkflowState` và `ThoughtProposal`. Giữ P-UCB, tree, reward,
  executor, provider adapter và output schema ngoài graph.
- Lý do: Luồng nhánh/retry hiện rõ trong graph, dễ test routing và kiểm tra dữ
  liệu LLM; không thay đổi công thức hay số request theo chủ ý.
- Giới hạn: Chưa bật checkpointer hoặc LangSmith tracing; resume chỉ áp dụng
  cho search đã có artifact hoàn chỉnh. Không gọi API trong test offline.

## D-020: Selection, Rethink và tính toàn vẹn candidate native

- Ngày: 2026-10-04
- Trạng thái: Chấp nhận
- Quyết định: Chọn child bằng P-UCB thuần; seed chỉ chi phối tie-break cục bộ.
  Rethink sửa thought tại node tối đa theo cấu hình, reset visit/Q/prior của
  action bị thay; giữ candidate cũ cùng thought snapshot. Khi vẫn fail và còn
  rollout, Expansion điều kiện hóa trên feedback cuối.
- Lý do: Tránh chọn unvisited bất chấp P-UCB, tránh gán reward/prior của thought
  cũ cho thought mới và tránh sai lịch sử artifact.
- Giới hạn: Trace portable hiện mới là AST statement span + runtime snapshots,
  không phải CFG hoàn chỉnh; seed không điều khiển sampling bên provider.

## D-019: Native RethinkMCTS package và upstream audit snapshot

- Ngày: 2026-09-27
- Trạng thái: Chấp nhận
- Quyết định: Giữ repo tác giả tại `vendor_rethinkmcts/` và triển khai native tại
  `rethinkmcts/`. Upstream pin commit `3908cacd94feed849f671f6de39f0baec00ed72c`.
- Lý do: Windows không phân biệt `RethinkMCTS` và `rethinkmcts`; tách tên vendor tránh
  xung đột import và giữ rõ code gốc với code thí nghiệm.
- Ràng buộc: Không sửa source upstream; artifact native nằm dưới `outputs/rethinkmcts/`,
  không dùng chung `outputs/baselines/`.
- Phạm vi v1: faithful paper implementation, public/private policy theo repo gốc, chưa
  thêm TLE-aware reward hoặc root-cause identification.

## D-018: Full generation, sampled evaluation judge

- Ngày: 2026-09-27
- Trạng thái: Chấp nhận
- Quyết định: Generation chay full APPS test + HumanEval test. Evaluation chi
  chay 100 bai moi dataset theo manifest `data/samples/evaluation_v1/`.
- Metric APPS: macro Pass Rate la metric chinh, micro Pass Rate la metric phu,
  va Pass@1 la ty le bai pass toan bo test. HumanEval chi bao Pass@1.
- Lý do: Giữ toàn bộ candidate để tái sử dụng, nhưng giới hạn chi phí thực thi và
  giữ một tập judge cố định để so sánh model/MCTS.
- Ràng buộc: Không sample lại khi chấm; không dùng sample judge làm giới hạn
  generation; missing candidate vẫn nằm trong denominator của Pass Rate/Pass@1.

## D-017: Khoa sample benchmark va tach model output

- Ngày: 2026-09-27
- Trạng thái: Chấp nhận
- Quyết định: Baseline hiện tại dùng `qwen2.5-coder:7b-instruct` qua Ollama và
  judge 100 bài APPS test + 100 bài HumanEval test trong hai manifest cố định tại
  `data/samples/evaluation_v1/`. `baseline_v1` chỉ giữ để truy vết lịch sử.
- Lý do: Giam chi phi, tranh sample drift va tao tap so sanh co dinh cho MCTS sau nay.
- Ràng buộc: Moi lan chay generation/evaluation phai dung cung sample file; output
  phai nam duoi `outputs/baselines/<stage>/<run>/<model>/<dataset>/`. Run cu cua
  model Modal/Qwen duoc giu rieng, khong tron voi run moi.

## D-001: Baseline trước, đóng góp sau

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Phải hiểu và chạy được RethinkMCTS gốc trước khi viết MCTS riêng hoặc
  thêm reward/root-cause mới.
- Lý do: Cần baseline quan sát được để tránh triển khai dựa trên giả định sai.

## D-002: Chỉ dùng APPS và HumanEval

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Không dùng CodeContests trong phạm vi dự án.
- Lý do: Tập trung tái lập setup của paper và giới hạn khối lượng chuẩn bị dữ liệu.

## D-003: APPS chỉ giữ bản raw

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Chỉ giữ `data/apps/raw`; không giữ bản Arrow trùng lặp.
- Lý do: Repo gốc cần cấu trúc raw và bản Arrow chiếm thêm khoảng 1,33 GB.

## D-004: HumanEval giữ bản Arrow

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Giữ HumanEval tại `data/humaneval/arrow`.
- Lý do: Dataset nhỏ, load trực tiếp được và chưa có yêu cầu từ repo gốc buộc đổi dạng.

## D-005: Tài liệu có source of truth

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Mỗi loại thông tin có một file chịu trách nhiệm theo `docs/README.md`.
- Lý do: Tránh đường dẫn, trạng thái và số liệu mâu thuẫn giữa nhiều file Markdown.

## D-006: Sử dụng LLM qua Modal.com

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Dùng endpoint OpenAI-compatible trên Modal.com; cấu hình endpoint,
  token và model qua `.env`.
- Lý do: Tách provider/runtime khỏi code và cho phép thay đổi deployment mà không sửa
  thuật toán.
- Ràng buộc: Không commit secret, không hard-code endpoint/model, và mọi smoke test
  phải giới hạn request để kiểm soát chi phí.

## D-007: Virtual environment chuẩn

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Toàn bộ Python/pip của dự án dùng `D:\ReThinkMCTS\venv`.
- Lý do: Tránh dependency global và giữ một môi trường chung có thể kiểm tra.
- Ràng buộc: Mọi thay đổi Python version hoặc dependency phải cập nhật
  `requirements.txt`, `docs/environment.md` và `project-status.md`.

## D-008: Direct generation trước evaluation và MCTS

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Baseline đầu tiên chỉ gửi một bài cho LLM và lưu code trả về.
- Chưa bao gồm: chạy code, test pass/fail, reward, tree search hoặc rethink.
- Lý do: Xác minh riêng data-to-prompt-to-code pipeline trước khi thêm execution và
  search, giúp lỗi ở mỗi tầng dễ quan sát hơn.

## D-009: Mỗi baseline có package và namespace artifact riêng

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Baseline nằm dưới `baselines/<name>/`, có config versioned và output
  dưới `outputs/baselines/<name>/<run>/<model>/`.
- Lý do: Cho phép benchmark nhiều model, prompt và sampling parameters mà không trộn
  code hoặc artifact giữa các phương pháp.
- Ràng buộc: Secret/endpoint vẫn nằm trong `.env`; config benchmark chỉ chứa model
  identifier và tham số không nhạy cảm.

## D-010: Tách sinh code và chấm code thành hai tầng

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Core direct generation chỉ sinh artifact; `Executors/` nhận source
  code và trả `ExecutionReport` thống nhất cho APPS/HumanEval. CLI có thể điều phối
  hai tầng khi người dùng chọn rõ `--evaluate`, nhưng không trộn logic executor vào
  pipeline sinh code.
- Lý do: Cho phép tái chấm cùng candidate, thay executor hoặc benchmark nhiều model
  mà không phải gọi lại LLM.
- Quy ước: APPS tính theo từng test trong `input_output.json`; HumanEval tính theo
  toàn bộ official harness (`1/1` hoặc `0/1`), không tự tách các câu assert.
- Ràng buộc: Subprocess và timeout không phải security sandbox. Chạy quy mô lớn cần
  thêm container/VM, tắt mạng và giới hạn tài nguyên ở tầng hệ điều hành.

## D-011: Entry point riêng theo dataset, implementation dùng chung

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Người dùng chạy `baselines.generate_apps` hoặc
  `baselines.generate_humaneval`; hai wrapper cố định dataset và gọi chung
  `baselines.direct_generation.cli`.
- Lý do: Lệnh ngắn, khó chọn nhầm dataset nhưng không nhân đôi logic gọi Modal,
  prompt, config hoặc lưu artifact.
- Quy ước: Output mặc định luôn nằm dưới
  `outputs/baselines/direct_generation/<run>/<model>/<dataset>/` của project.

## D-012: Full benchmark phải resumable và có xác nhận

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: APPS và HumanEval có batch entry point riêng nhưng dùng chung bộ điều
  phối tuần tự. Resume bật mặc định và mỗi kết quả được ghi vào JSONL manifest.
- Lý do: Full APPS test + HumanEval cần 5.164 request; batch phải tiếp tục được sau
  lỗi hoặc gián đoạn mà không mặc định gọi lại các bài đã hoàn thành.
- Ràng buộc: Chọn hơn 20 bài cần `--confirm-full-run`; retry mặc định bằng 0 và phải
  có `--plan` để xem model, số bài, output và manifest trước khi chạy.

## D-013: Generation hoàn tất trước parallel evaluation

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Pipeline chính có hai checkpoint. Toàn bộ generation của các dataset
  đã chọn phải thành công trước khi evaluation bắt đầu. Evaluation song song theo
  candidate bằng process pool; test trong một candidate không dùng pool lồng nhau.
- Lý do: Tách chi phí/gọi LLM khỏi thực thi code, cho phép chấm lại không gọi model,
  và giữ mức song song có thể kiểm soát trên Windows.
- Artifact: Mỗi candidate có `evaluation.json`; mỗi run/model/dataset có
  `results.jsonl`, `results.csv` và `summary.json`.
- Ràng buộc: Mặc định tối đa 4 worker. Process isolation hiện tại không thay thế
  container/VM sandbox cho code không tin cậy.

## D-014: Log phải truy ngược được tới problem và test fail

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Generation, pipeline stage và evaluation đều có text log; evaluation
  còn tách `passed.jsonl`, `failures.jsonl/csv` và báo cáo tổng hợp.
- Mỗi failure phải có: dataset, problem ID, artifact, loại lỗi, số test pass/tổng
  test, index test fail và lỗi đầu tiên. Expected/actual đầy đủ nằm trong
  `evaluation.json` của candidate.
- Lý do: Có thể đọc nhanh bài nào sai và tỷ lệ pass, đồng thời vẫn giữ đủ bằng chứng
  để phân tích lỗi hoặc dùng làm feedback cho MCTS sau này.

## D-015: Không resume generation rỗng hoặc bị cắt

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Config mặc định không gửi `max_tokens`. Artifact chỉ hoàn chỉnh khi
  source không rỗng và finish reason là `stop` hoặc không được provider cung cấp.
- Lý do: Giới hạn 2.048 token đã tạo nhiều response `length` và solution chỉ chứa
  xuống dòng; xem chúng là hoàn thành làm mất candidate trong benchmark.
- Ràng buộc: Không gửi `max_tokens` không có nghĩa vô hạn; context/model/provider
  vẫn có giới hạn. Artifact lỗi vẫn giữ để audit nhưng resume và evaluation bỏ qua.

## D-016: Generation song song có giới hạn

- Ngày: 2026-09-26
- Trạng thái: Chấp nhận
- Quyết định: Batch generation hỗ trợ `--generation-workers N` bằng thread scheduler;
  mỗi worker chạy một problem trong subprocess, manifest/log do scheduler chính ghi.
- Mặc định: 1 worker để tương thích và kiểm soát chi phí; full run bắt đầu với 2.
- Lý do: Request LLM chủ yếu chờ mạng/model nên chạy đồng thời giảm wall-clock time
  mà không cần thay đổi artifact hoặc resume semantics.
- Ràng buộc: Không tăng quá khả năng concurrency/rate limit của Modal. Parallelism
  không giảm tổng request, token hay chi phí; completion có thể về khác thứ tự ID.

## D-017: APPS MCTS song song trên Modal, giữ provenance hai run

- Ngày: 2026-10-04
- Trạng thái: Đã chạy thật; 297/300 APPS candidate hoàn chỉnh
- Quyết định: Giữ model `qwen2.5-coder:7b-instruct`, chuyển inference mới sang
  L40S tối đa 4 replica, batch tối đa 4 problem worker. Các bước trong một
  search vẫn tuần tự; chỉ những bài APPS độc lập mới chạy song song.
- Run APPS mới là `rethinkmcts_qwen25_modal_l40s_parallel_v1`; không resume
  run L4 cũ vì source hash và worker count đã khóa. HumanEval 164 kết quả cũ
  không bị sao chép hoặc chạy lại.
- Finalizer ghép APPS run mới với HumanEval run cũ chỉ khi model digest,
  search settings và cohort trùng nhau. Hồ sơ benchmark ghi hai source run,
  source code/inference hash và GPU theo dataset.
- Judge vẫn chạy cục bộ trên laptop, tối đa 4 bài cùng lúc; chưa có sandbox
  từng candidate.

## D-018: Báo cáo adjudicated cho ba APPS technical failure

- Ngày: 2026-10-04
- Trạng thái: Chấp nhận theo yêu cầu người dùng, báo cáo đã tạo
- Quyết định: `0796`, `1033`, `1581` không có candidate hoàn chỉnh sau ít
  nhất hai failed/timeout attempts được tính 0 trong denominator macro Pass
  Rate và Pass@1 của cohort 300. Không tuyên bố đã chạy private tests cho ba
  bài đó và không tạo `final_solution.py` giả.
- Artifact báo cáo nằm trong `adjudicated_v1/`, tách khỏi core frozen benchmark;
  `run.json` ghi failure type, log hash, coverage 297+3 và nguồn HumanEval L4.
- Micro Pass Rate chỉ tính các private tests thực sự đã chạy ở 297 bài; bảng
  chính dùng macro Pass Rate và Pass@1. Kết quả phải mang nhãn
  `RethinkMCTS (adjudicated)`, không được gọi là clean-complete.

## D-019: Direct baseline paired cohort benchmark_v2

- Ngày: 2026-10-04
- Trạng thái: Đã chạy judge đủ 300 APPS + 164 HumanEval, không lỗi hạ tầng còn lại
- Quyết định: Tái sử dụng solution của generation run
  `qwen25_coder_7b_instruct_baseline_v1` cho đúng 300 APPS và 164 HumanEval
  trong `data/samples/benchmark_v2/`. Không gọi LLM và không sửa solution.
- APPS dùng private second half giống MCTS; HumanEval dùng official harness.
  Baseline lịch sử 100+100 đã chấm toàn bộ APPS tests nên không so trực tiếp.
- Evaluation mới nằm ở run `qwen25_coder_7b_instruct_baseline_benchmark_v2`;
  báo cáo từng bài được tách khỏi artifact generation cũ, cấu hình/hash cohort
  được khóa để resume không trộn chính sách chấm.

## D-020: Final evaluation dùng toàn bộ APPS tests

- Ngày: 2026-10-04
- Trạng thái: Chấp nhận; đã chấm lại baseline và MCTS
- Quyết định: Public split chỉ điều khiển MCTS search. Bảng benchmark cuối chạy
  toàn bộ `input_output.json` cho final solution của baseline và MCTS.
  HumanEval tiếp tục dùng toàn bộ official harness.
- Các bảng private-half trước đây được giữ để audit và đánh dấu đã bị thay thế.
  Bảng chính nằm tại `docs/results/benchmark-v2-all-tests.md`.

## D-021: APPS interface trong prompt và thí nghiệm public coverage

- Ngày: 2026-10-04.
- Trạng thái: Đã sửa và kiểm thử offline; chưa benchmark lại.
- Quyết định: Prompt native v2 truyền `stdin_stdout` hoặc `fn_name` đúng với
  `input_output.json` vào Expansion, Code, Feedback và Rethink. Khi stdout
  rỗng dù expected có nội dung, ghi chẩn đoán vào feedback thay vì chỉ dựa
  vào phân tích thuật toán của LLM.
- Public policy mặc định vẫn là `half` theo repo tác giả. Có thể chạy thí
  nghiệm riêng với `half_min2`; thay đổi public coverage yêu cầu run mới,
  lưu policy trong `run_config.json`. Final benchmark vẫn chấm toàn bộ tests.
- Không đổi reward/P-UCB hoặc tie-break candidate: upstream dùng `np.argmax`
  trên train reward, native dùng `max` chọn candidate đầu tiên khi hòa.
- Các kết quả APPS 19,96/9,67 và baseline 30,51/14,00 là kết quả lịch sử,
  không phải kết quả sau sửa prompt. Cần chạy LLM mới mới biết tác động.

## D-022: Dual với evaluator model riêng và pilot APPS 30

- Ngày: 2026-10-18.
- Trạng thái: Đã implement/test offline; chưa deploy hoặc gọi Modal.
- Quyết định: Giữ `qwen2.5-coder:7b-instruct` làm generator; chỉ operation
  `self_evaluation` dùng `qwen2.5-coder:14b-instruct`. Giữ nguyên prompt,
  gate `v_test=1`, parser và reward Dual `a=0.8`, `b=0.2`. Ghi model/digest
  từng vai trò vào run config và model thực tế vào từng request event.
- APPS dùng manifest pilot seed `20261018`, 10 ID mỗi difficulty, lấy từ
  cohort benchmark_v2; HumanEval giữ đủ 164 ID. Kết quả APPS chỉ được báo cáo
  là n=30, không nội suy hoặc gán thành n=300. Reporter riêng tránh finalizer
  chuẩn benchmark 300+164.
- Run name pilot được tách riêng; không thay đổi artifacts/kết quả lịch sử.
