# Audit implementation

Tài liệu này phân biệt rõ mô tả trong paper với hành vi đã quan sát trong code.

## APPS prompt, feedback và public tests (2026-10-04)

Đối chiếu trực tiếp `RelativeWork/2409.09584v2.pdf` (mục 3.1, 4, phụ lục C,
Table 10) với repo gốc commit `3908cacd94feed849f671f6de39f0baec00ed72c`:

- Paper yêu cầu sinh complete program từ thoughts, chạy public tests trong search
  và dùng feedback từ failed cases để Rethink. Table 10 không tự mô tả giao diện
  APPS stdin/stdout; upstream loader `dataSet/dataHandlers/APPSHandler.py`
  thêm `Use Standard Input format` hoặc `Use Call-Based format` vào prompt,
  dựa trên `fn_name` trong `input_output.json`.
- Upstream `get_test_cases()` dùng `len(inputs)//2` public test khi chọn `half`;
  nó yêu cầu mỗi bên có ít nhất một test. Native `half` làm cùng phép chia.
- Upstream `models/RethinkMCTS.py` chọn `np.argmax(train_rewards)`; candidate
  đầu tiên thắng khi reward hòa. Native `max(..., key=reward)` tương đương
  về tie-break, nên không thay quy tắc này để ưu ái kết quả sau khi chấm.
- Upstream cũng tính `test_rewards` của mọi candidate ở bước báo cáo, nhưng
  `best_idx` chỉ dựa trên `train_rewards`. Native final selection vẫn không
  dùng private/all-tests score để quyết định chọn code.

Phát hiện ở run APPS lịch sử: prompt native v1 không truyền mode stdin/stdout.
Chẳng hạn `0395` chỉ định nghĩa `can_form_equal_teams` và không in gì; public
feedback ghi expected `YES`, actual rỗng nhưng LLM lại phân tích lỗi greedy.
Đây là sai lệch giao diện so với upstream loader, không phải lỗi APPS judge.
Kiểm tra lại artifact best candidate của 297 bài: 295 bài stdin/stdout,
106 bài có actual stdout rỗng trên **mọi public test**; 181 bài có best
reward bằng 0 và chỉ 46 bài pass toàn bộ public tests. Số liệu này mô tả
run cũ, không chứng minh tất cả stdout rỗng đều do cùng một nguyên nhân.

Đã sửa trong prompt `native_v2`: APPS stdin/stdout phải đọc stdin, gọi solver
và in output; APPS call-based phải định nghĩa đúng `fn_name` và return kết quả.
Expansion, code generation, verbal feedback và Rethink đều nhận giao diện.
Khi APPS stdin/stdout fail với stdout rỗng và expected không rỗng, feedback
ghi thêm chẩn đoán xác định từ executor; LLM được yêu cầu kiểm tra driver
trước khi suy luận lỗi thuật toán. Chẩn đoán không sửa code candidate hoặc
thay reward.

Pilot thật `0395` với cùng digest và search config cũ đạt 53/53 all-tests
thay vì 0/53. Tuy vậy, LLM feedback của candidate đầu đã gán `block=interface`
và nói thiếu print dù executor ghi actual `NO` và source có print. Đã thêm
guard: nếu stdout không rỗng, feedback `interface` bị thay bằng
`output_mismatch`, raw feedback vẫn được lưu để audit. Guard này được thêm
**sau** pilot, mới có test offline; xem báo cáo pilot trong `docs/results/`.

Cohort `benchmark_v2` có 85/300 bài chỉ có 3 test, nên `half` đưa đúng 1
public test cho từng bài đó; tổng trung bình 19,86 test/bài. Đây là giới hạn
dữ liệu, không phải bug của phép chia. Native thêm **tùy chọn**
`half_min2 = max(2, len(inputs)//2)` (vẫn giữ ít nhất một private test theo
điều kiện cohort), để nghiên cứu ảnh hưởng của public coverage. Tùy chọn này
khác upstream và phải có run name, config, bảng riêng. `half` vẫn là mặc định.
Final benchmark của dự án tiếp tục chấm toàn bộ test APPS cho cả hai phương pháp.

Bảng cũ trong `docs/results/benchmark-v2-all-tests.md` được sinh trước các
sửa đổi này; pilot một bài chưa đủ để suy diễn prompt v2 cải thiện Pass@1
trên cohort 300 bài.

## Snapshot workspace hiện tại

| Thành phần | Trạng thái đã kiểm chứng |
|---|---|
| `Executors/APPSExecutor.py` | Chạy từng test `stdin_stdout` và `call_based`, có timeout và báo partial pass |
| `Executors/HumanevalExecutor.py` | Chạy nguyên official harness, báo `1/1` hoặc `0/1` |
| `Executors/common.py` | Report schema và subprocess runner dùng chung; chưa phải security sandbox |
| `Models/` | Rỗng |
| `ChatModels/modal_client.py` | Adapter Modal đã gọi API thật và lưu response/usage |
| `DataProcess/problem_loader.py` | Loader đề APPS/HumanEval, không đọc solution/test |
| `baselines/direct_generation/` | Direct generation package; bước chấm được tách sang `Executors/` |
| `pipelines/direct_baseline.py` | Điều phối generation hoàn tất trước parallel evaluation |
| `evaluation/batch_evaluation.py` | Process pool theo candidate; report JSONL/CSV/summary và resume |
| `requirements.txt` | Đã tổng hợp từ import của code hiện tại và repo gốc; native offline tests đã chạy |
| `vendor_rethinkmcts/` | Repo tác giả, pin commit `3908cacd94feed849f671f6de39f0baec00ed72c`, giữ nguyên để audit |
| `rethinkmcts/` | Native tree/P-UCB/reward/feedback/search loop và CLI plan đã triển khai |
| Dataset | Đã chuẩn bị, xem `docs/datasets.md` |
| `data/scripts/prepare_humaneval.py` | Sau bước kiểm tra dữ liệu cục bộ vẫn gọi `load_dataset()` ở cuối, nên có thể truy cập mạng không cần thiết |
| `data/scripts/prepare_apps.py` | Chỉ kiểm tra thư mục `raw` tồn tại, chưa tự xác minh đủ file/số mẫu trước khi bỏ qua |
| LLM provider | Ollama hiện tại; Modal.com được giữ để audit run cũ; cấu hình qua `.env` |
| `tools/smoke_modal.py` | Smoke script lịch sử cho Modal, không phải benchmark entry point |
| Python environment | `D:\ReThinkMCTS\venv`, Python 3.14.5 |
| Windows portability | Executor gốc import module Unix `resource`; cần xử lý hoặc chạy trong Linux/WSL |
| `pyext` compatibility | `pyext==0.7` không build trên Python 3.14; cần thay `RuntimeModule.from_string` bằng local shim |

Kết luận: workspace có direct-generation baseline, executor offline độc lập và native
implementation có thể đọc/test offline; smoke provider thật vẫn chưa chạy.

## Sửa sai lệch native (2026-10-04)

Sau các sửa thuật toán bên dưới, phần điều phối đã chuyển sang LangGraph.
Chuyển đổi này chỉ thay luồng control, không thay P-UCB/reward/public-private
policy. Pydantic chặn state sai kiểu, thought rỗng, score không hữu hạn và
response Expansion thiếu/thừa; kết quả offline cần được xác nhận thêm bằng
smoke provider thật. LangGraph hiện chưa có checkpoint/resume giữa chừng.

- Selection trước đây ưu tiên cứng unvisited; nay chọn theo P-UCB cho toàn bộ child.
  Điểm hòa được tie-break bằng RNG cục bộ theo seed.
- Expansion nay yêu cầu đúng `width` thought khác nhau; trước đây parser âm thầm
  nhận ít hơn cấu hình và làm cây có độ rộng không mong muốn.
- Vòng Rethink trước đây chỉ sửa một lần dù cấu hình lớn hơn; nay sửa lặp có giới hạn,
  dừng khi public tests pass và dùng feedback cuối để Expansion khi còn rollout.
- Node bị thay thought nay reset visit/Q/prior, tránh gán thống kê action cũ cho action
  mới; ancestor giữ lịch sử vì state của ancestor không đổi. Candidate cũ vẫn giữ.
- Candidate artifact nay ghi snapshot thought tại thời điểm Evaluation; trước đây
  `thoughts.json` có thể phản ánh thought sau Rethink.
- Trace cho APPS call-based nay luôn được trả về. Trace AST giảm gán lặp event và
  ghi trạng thái biến trước/sau, nhưng **chưa tạo CFG thực** như repo tác giả.
- Chưa kiểm chứng bằng smoke Ollama hoặc so output với upstream trên cùng problem;
  không gọi đây là tương đương hoàn toàn với paper.

## Paper mô tả, code cần xác minh

| Chủ đề | Paper | Cần tìm trong code gốc |
|---|---|---|
| Selection | P-UCB với Q là reward lớn nhất | Khởi tạo visit, tie-break, cách lưu Q |
| Expansion | Sinh tối đa `k` thought và reasonableness | Parser, normalize score, retry prompt |
| Evaluation | Sinh code hoàn chỉnh từ current thoughts | Node nào được evaluate sau expansion |
| Dual evaluation | Chỉ cần self-eval để phân biệt code pass public tests | Thứ tự gọi và range score thực tế |
| Verbal feedback | Block-level trace và giá trị biến | Công cụ CFG, giới hạn trace/test/token |
| Backpropagation | Cập nhật node và ancestor bằng scalar reward | Max hay aggregate nội bộ |
| Rethink | Thay thought gần nhất bằng thought mới | Mutation cây, child cũ, số lần rethink |
| Final answer | Code có reward cao nhất trong `program_dict` | Deduplicate và xử lý cùng reward |
| APPS tests | Public để search, private để báo kết quả | Quy tắc chia test cụ thể |

## Checklist audit repo gốc

- [x] Ghi URL, branch và commit hash tại `vendor_rethinkmcts/`.
- [x] Lập sơ đồ entry point và module.
- [x] Đọc loader APPS/HumanEval.
- [x] Đọc executor và timeout policy.
- [x] Đọc node/state/action representation.
- [x] Đọc implementation P-UCB và backpropagation.
- [x] Đọc prompt expansion, code generation, self-eval và rethink.
- [x] Xác định nơi tạo verbal feedback/block trace.
- [x] Ghi các khác biệt chính trong `docs/rethinkmcts-implementation.md`.
- [x] Tạo adapter OpenAI-compatible dùng client hiện tại; chưa gọi provider trong task này.
- [ ] Kiểm tra response usage, timeout, retry và lỗi rate limit của provider trong smoke thật.
- [x] Không sửa code upstream.

## Mẫu ghi quan sát

```text
Ngày:
Commit:
Lệnh chạy:
Dataset / problem ID:
Model / rollout / seed:
Hành vi quan sát:
Khớp paper:
Khác paper:
Bằng chứng (file:line hoặc log):
Câu hỏi còn mở:
```
# Cap nhat provider/benchmark (2026-09-27)

Phan audit Modal ben duoi la lich su cua run cu. Benchmark hien tai dung Ollama
voi `qwen2.5-coder:7b-instruct` va hai sample manifest lich su tai
`data/samples/evaluation_v1/`. Cohort moi la `data/samples/benchmark_v2/`;
xem `docs/llm-provider.md` và `docs/pipeline-direct.md`.

