# Trạng thái dự án

Cập nhật lần cuối: **2026-10-18**.

## Dual với evaluator riêng: HumanEval hoàn tất, APPS còn 1 timeout

Modal deployment/preflight xác nhận generator `qwen2.5-coder:7b-instruct`
(digest `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`)
và evaluator `qwen2.5-coder:14b-instruct`
(digest `9ec8897f747e246e970bc5cfdda85d22f1123dc2e3d34978a010a75968716849`)
trên L40S. Smoke APPS `2788` và HumanEval `HumanEval/0` đều hoàn tất trong
`rethinkmcts_dual_external_qwen25_14b_smoke_v1`. HumanEval event log xác nhận
`self_evaluation` dùng 14B, còn `expand`/`code_generation` dùng 7B. APPS smoke
không gọi `self_evaluation` vì candidate không pass public tests; đây là điều
kiện gọi evaluator của Dual. Smoke không phải kết quả benchmark. Pilot
`rethinkmcts_dual_external_qwen25_14b_pilot_v1` hiện có 29/30 APPS và
164/164 HumanEval candidate. HumanEval `HumanEval/17` hoàn tất khi resume.
APPS `0841` vẫn chưa có summary. Hai lần retry mới đều chạm giới hạn batch
900 giây; event trace ở cả hai dừng sau `rethink`, trước khi có kết quả của
request LLM kế tiếp. Một lần retry trước đó trả HTTP 500 từ Modal. Đây không
phải timeout của test executor: batch timeout là 900 giây trong khi HTTP
inference timeout ở `tools/modal_mcts/inference.py` là 1100 giây, vì vậy batch
giết subprocess trước khi client ghi nhận timeout HTTP. Không tính bài này là
pass; nếu lập báo cáo pilot thì giữ mẫu số 30 và ghi candidate thiếu/timeout.
Chưa tạo bảng kết quả cuối. Hướng dẫn tại
`docs/runbooks/rethinkmcts-external-evaluator-pilot.md`.

## Local search trace viewer

Đã thêm viewer read-only tại `tools/trace_viewer/` để duyệt run/model/dataset/problem,
xem cây search và event trace từ artifact đã lưu. Chạy bằng
`.\venv\Scripts\python.exe -m tools.trace_viewer.server` và mở
`http://127.0.0.1:8765`. Viewer không gọi LLM hoặc chạy candidate. Đây là playback,
không phải live trace; chỉ hiển thị dữ liệu đã persist. Hướng dẫn tại
`docs/runbooks/trace-viewer.md`.

## Ablation reward test-only (da chay)

Da chay `reward_mode=test_only` tren Modal L40S voi model
`qwen2.5-coder:7b-instruct`, digest
`dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`.
Search APPS `rethinkmcts_apps_test_only_v1` co 297/300 candidate; ba ID
`0841`, `1033`, `3702` timeout 900 giay va duoc tinh 0. Rejudge all-tests
297 candidate: 68 bai pass het; macro Pass Rate 45,34%, Pass@1 22,67%
tren 300 ID. HumanEval `rethinkmcts_humaneval_test_only_v1` co 164/164
candidate; official harness pass 147/164, Pass@1 89,63%. Bang chi tiet,
provenance va caveat tai `docs/results/rethinkmcts-test-only-v1.md`; lenh chay tai
`docs/runbooks/rethinkmcts-test-only-ablation.md`. Reward `dual` cua run cu
khong doi. Khong goi day la run APPS sach 300/300 candidate.

## Repair hai APPS technical failure

Đã xác định `1684` và `3702` mất candidate do `collect_trace()` gọi
`ast.parse()` trên Python code LLM sai cú pháp, làm search crash. Đã sửa
trace trả feedback `syntax_error`, thêm chọn ID thuộc cohort và tùy chọn
số APPS test worker trong một candidate (mặc định 1). Test toàn repo
85/85 pass. Repair run riêng đã tạo candidate cho cả hai: `1684` chấm
6/13 all-tests; `3702` cần 2 test worker và timeout tổng 1.800 giây để
hoàn tất search, final judge 0/104 do timeout từng test. Run gốc 295/300
và bảng của nó được giữ bất biến; số 297/300, 43,20% macro Pass Rate,
19,00% Pass@1 chỉ là phép ghép phân tích, không phải benchmark đồng nhất
source/config. Xem `docs/results/rethinkmcts-apps-ast-repair.md`.

## Rejudge APPS native_v2 (ket qua tam thoi)

Run `rethinkmcts_apps_interface_v2_half_w4` đã đi qua 300/300 ID. Sau một
lượt retry, có 295 artifact hoàn chỉnh; còn 3 search timeout 900 giây
(`1033`, `1634`, `3698`) và 2 lỗi kỹ thuật AST (`1684`, `3702`). Rejudge
295 `final_solution.py` trên **toàn bộ** APPS tests với 5 giây/test,
2 worker, không gọi LLM. Không có `executor_error`; 57/295 candidate pass
hết tests. Ba search timeout tính không pass; hai bài lỗi kỹ thuật còn
thiếu candidate đóng góp 0 vào denominator tạm thời, không kết luận code
sai. APPS overall 43,04% macro Pass Rate và 19,00% Pass@1 trên 300 ID.
HumanEval 91,46% được tái sử dụng từ run `native_v1` cũ, chưa chạy lại
bằng `native_v2`. Xem `docs/results/rethinkmcts-apps-native-v2-w4-retry.md`;
snapshot 286/300 được giữ để truy vết.

## Audit APPS sau benchmark

Đã đối chiếu paper và repo tác giả pin commit với run APPS lịch sử. Prompt
native v1 thiếu mô tả giao diện stdin/stdout dù upstream APPS loader cung cấp
thông tin đó. Bản native hiện dùng prompt `native_v2`, đưa interface vào
Expansion/Code/Feedback/Rethink và đưa chẩn đoán stdout rỗng vào feedback.
`half` vẫn là public split mặc định của upstream; thêm tùy chọn `half_min2`
cho run nghiên cứu coverage riêng. Cohort có 85/300 bài chỉ 3 test, nên
`half` nhìn thấy một public test ở các bài đó. Test offline đã pass và đã
smoke một bài. Hiện đã có bảng tạm thời `native_v2` với 295/300 candidate;
bang v2 all-tests lich su van phan anh code/prompt `native_v1`, khong duoc
gan cho `native_v2`. Xem
`docs/implementation-audit.md` và `docs/results/benchmark-v2-all-tests.md`.

Pilot thật bài APPS `0395` trên Modal L40S, cùng cấu hình search với run cũ:
prompt `native_v2` chọn candidate pass 26/26 public và 53/53 final tests;
run `native_v1` trước đó 0/26 public, 0/53 all-tests. Pilot dùng 9 requests,
13.579 tokens. Phát hiện LLM feedback gán nhầm lỗi thiếu print dù code có
stdout; đã thêm guard nhất quán với executor sau pilot và kiểm thử offline.
Guard chưa được xác minh bằng request thật. Kết quả 300 bài chưa thay đổi.
Xem `docs/results/rethinkmcts-apps-0395-native-v2-smoke.md`.

## Giai đoạn hiện tại

Dự án đã hoàn thành checkpoint **DIRECT-GENERATION + OFFLINE EVALUATION**.
Native RethinkMCTS đã chạy thật với LLM trên Modal L4 và judge cục bộ:
**HumanEval 164/164 hoàn tất; APPS L40S song song đạt 297/300**. Đã tạo
báo cáo benchmark **adjudicated** 300+164 theo quyết định tính ba bài thiếu
candidate là thất bại. Xem `docs/results/rethinkmcts-modal-benchmark-v2-adjudicated.md`;
không trình bày đây là run sạch 300/300 candidate.

Đã triển khai và chạy thật đường APPS tăng tốc: Modal L40S tối đa 4 replica và
batch 4 problem worker, run mới `rethinkmcts_qwen25_modal_l40s_parallel_v1`.
Test offline pass; `--plan` xác nhận 300 APPS. Run full và một lượt resume
đã hoàn chỉnh 297 bài. Còn `0796`, `1581` lặp lỗi Windows khóa file tạm
`.executor-stderr`; `1033` hai lần chạm timeout 900 giây ở Evaluation.
Run L4 lịch sử và 164 HumanEval được giữ nguyên;
finalizer hỗ trợ ghép hai run với kiểm tra model digest, search config và cohort.
Core finalizer vẫn từ chối thiếu artifact; reporter riêng
`tools.modal_mcts.adjudicate` đã tạo bảng Pass Rate/Pass@1 với ba ID tính 0,
có bằng chứng attempt log. Sau khi chấm lại toàn bộ tests, APPS overall 19,96%
Pass Rate và 9,67% Pass@1;
HumanEval 91,46% Pass@1.

## Baseline đã hoàn thành

**Paired baseline benchmark_v2 đã chấm xong 300 APPS + 164 HumanEval** bằng
solution cũ, không gọi LLM. APPS chấm toàn bộ tests; HumanEval
official harness. Không còn candidate thiếu hoặc `executor_error`. APPS overall
Pass Rate 30,51%, Pass@1 14,00%; HumanEval Pass@1 80,49%. Chi tiết ở
`docs/results/benchmark-v2-all-tests.md`. Bảng phía dưới là sample lịch
sử 100+100, không được so trực tiếp với benchmark_v2.

| Thuộc tính | Giá trị |
|---|---|
| Model | `qwen2.5-coder:7b-instruct` |
| Provider | Ollama trên GPU CKEY |
| Run | `qwen25_coder_7b_instruct_baseline_v1` |
| Generation | APPS test 5.000 + HumanEval test 164 |
| Judge sample đã chạy | APPS 100 + HumanEval 100 |
| Manifest của kết quả cũ | `data/samples/evaluation_v1/` |

Kết quả judge đã kiểm chứng:

| Nhóm | Pass Rate (%) | Pass@1 (%) |
|---|---:|---:|
| APPS Intro. | 39.02 | 23.08 |
| APPS Inter. | 26.14 | 7.46 |
| APPS Comp. | 25.09 | 0.00 |
| APPS Overall | 27.60 | 8.00 |
| HumanEval | N/A | 84.00 |

Artifact tổng hợp:

```text
outputs/baselines/evaluations/
└── qwen25_coder_7b_instruct_baseline_v1/
    └── qwen2.5-coder_7b-instruct/
        ├── benchmark_table.md
        ├── benchmark_table.csv
        ├── benchmark_summary.json
        ├── apps/
        └── humaneval/
```

## Đã kiểm chứng

- Dataset cục bộ có APPS train/test, mỗi split 5.000 bài.
- HumanEval Arrow có 164 bài test.
- Sample judge có đúng 100 ID duy nhất cho mỗi dataset và được khóa bằng seed.
- Cohort cho các run mới đã khóa tại `data/samples/benchmark_v2/`: 300 ID APPS
  (100 mỗi độ khó, đúng danh sách nhóm đối chiếu) và toàn bộ 164 HumanEval.
  MCTS đã có báo cáo adjudicated; paired direct baseline đã chấm đủ 464/464.
- Đối chiếu cục bộ: 300 ID APPS đều tồn tại ở split test, đúng difficulty,
  có ít nhất 3 input/output tương ứng; 164 HumanEval trùng task index,
  entry point và prompt với dữ liệu `processed.jsonl` của nhóm đối chiếu.
- Generation lưu `solution.py`, `response.txt`, `metadata.json` và `problem.txt`
  theo `run/model/dataset/problem_timestamp`.
- APPS executor hỗ trợ `stdin_stdout` và `call_based`.
- HumanEval executor dùng official harness.
- Evaluation chạy song song theo candidate; APPS còn hỗ trợ song song test bằng
  `--test-workers`.
- Judge tạo macro Pass Rate, micro Pass Rate và Pass@1 cho APPS; HumanEval chỉ
  báo Pass@1 theo quy ước đã chốt.
- Unit test offline hiện pass `69/69`, gồm direct baseline, executor, judge,
  native search, bundle, batch resume và aggregate synthetic.
- HumanEval search nay dùng `data/humaneval/public_tests.jsonl` lấy từ
  `processed.jsonl` nhóm đối chiếu đã pin commit/SHA; đã xác minh 164/164
  hàng với prompt/entry point Arrow cục bộ, mỗi bài 1-8 assertions.
- MCTS batch đã có plan 300+164, xác nhận full, subprocess timeout, attempt
  log và resume cấp bài; bundle Docker gồm đúng input cohort, không gồm
  baseline solutions hoặc `.env`. Chưa smoke trên GPU thuê.
- Code generated của baseline không bị thay đổi trong quá trình cleanup tài liệu.
- Run cũ Modal/Qwen được giữ riêng trong namespace `direct_full_v1`.
- Repo tác giả được pin tại `vendor_rethinkmcts/` ở commit
  `3908cacd94feed849f671f6de39f0baec00ed72c`.
- Native package nằm tại `rethinkmcts/`, artifact tách dưới `outputs/rethinkmcts/`.
- Native selection, vòng Rethink, candidate thought snapshot và APPS call-based
  trace đã được chỉnh theo audit; xem `docs/implementation-audit.md`.
- Native search được điều phối bằng LangGraph, với Pydantic state và thought
  contract; offline tests xác nhận routing, nhiều rollout và Rethink.
- Đã chuẩn bị workflow đóng gói candidate cohort 300+164 và Docker evaluator
  trên máy thuê. Bundle từ run baseline cũ chứa đủ 300+164 candidate và plan
  sau giải nén nhận đúng số bài. Chưa triển khai remote evaluation lên CKEY
  instance mới; baseline benchmark v2 đã chấm cục bộ bằng pipeline riêng.
- Đã thêm hồ sơ benchmark bất biến dưới `outputs/benchmarks/<run>/<model>/`
  để lưu tham số thực tế, cohort/data/code hash, candidate index và bảng.
  Paired baseline v2 hiện có bảng judge trong working artifacts nhưng chưa
  đóng băng thành hồ sơ `outputs/benchmarks/`.
- Đã thêm wrapper direct generation từ Windows qua SSH tunnel: kiểm tra model
  Ollama, tự pull nếu thiếu rồi mới gọi pipeline. Mới kiểm thử offline, chưa
  thử với instance CKEY mới; remote evaluation không sử dụng wrapper này.
- Modal GPU inference Function đã deploy và smoke thật với model
  `qwen2.5-coder:7b-instruct` trên L4, digest được ghi trong `run_config.json`.
- Run `rethinkmcts_qwen25_modal_v1` có đủ 164 HumanEval, 150 pass official
  harness (Pass@1 91,46%); 1.207 request, 809.036 token. Xem báo cáo riêng
  tại `docs/results/rethinkmcts-modal-humaneval-v1.md`.
- APPS có 1/300 artifact hoàn chỉnh từ smoke; batch full dừng theo yêu cầu ở
  bài 4005. Chạy tiếp bằng resume, không gọi lại bài hoàn chỉnh.

## Quyết định phạm vi

- Không dùng CodeContests.
- Generation full và evaluation sample là hai phạm vi độc lập.
- Mọi model/MCTS mới phải dùng lại `data/samples/benchmark_v2/`; số liệu
  baseline 100+100 hiện tại chỉ thuộc `evaluation_v1` và không được đổi nhãn.
- Candidate bị manual stop được ghi rõ trong `evaluation.json`, không sửa
  `solution.py`.

## Chưa hoàn thành

- Chạy smoke thật một bài HumanEval và một bài APPS với Ollama trên GPU CKEY.
- Đối chiếu output native với log/reward của repo gốc sau khi có smoke run.
- Thay trace AST hiện tại bằng CFG/basic-block đầy đủ nếu cần đối chiếu feedback
  chính xác với repo gốc.
- Cô lập từng test APPS/HumanEval trong sandbox riêng; Docker hiện chỉ giới
  hạn toàn bộ batch và chưa chống candidate đọc test/artifact cùng container.
- Xác nhận instance CKEY mới hỗ trợ Docker, rồi smoke remote evaluation trước
  khi chạy 300+164; Docker hiện chỉ cô lập cả batch, chưa từng test riêng.
- Chạy smoke remote MCTS hai bài rồi mới quyết định full 300+164. LangGraph
  chưa có checkpointer giữa một bài; batch resume ở ranh giới problem.
- Sandbox từng candidate trước khi dùng trong môi trường có dữ liệu/secret
  nhạy cảm; container batch hiện dùng host networking để gọi Ollama.

## Cách cập nhật

Chỉ ghi một điều vào mục đã kiểm chứng sau khi đọc trực tiếp file, chạy lệnh hoặc
đối chiếu nguồn. Khi thay đổi dataset, sample, output schema hoặc workflow, cập
nhật thêm `data/README.md`, `docs/decisions.md` và runbook liên quan.
