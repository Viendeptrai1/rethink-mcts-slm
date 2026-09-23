# Nền thực nghiệm và protocol feedback-selection-v0

Trạng thái: thiết kế và kiểm chứng chức năng offline. Không có kết quả LLM mới. Phiên bản artifact mới là schema 2; bảng cũ trong `results/` thuộc exploratory protocol trước sửa.

## 1. Biến nghiên cứu

Phương pháp chính: thought-level MCTS kế thừa RethinkMCTS. Thay đổi một yếu tố chính là mức feedback: `facts_only`, `trace`, `block`, `adaptive`. `none` bỏ phần nội dung feedback khi render prompt để làm ablation; việc chỉ thực hiện rethink sau một failure vẫn thuộc control flow của thuật toán.

Các baseline chạy cùng PublicProblem/evaluator: `direct`, `best_of_n`, `iterative_repair`. `graph` còn được hỗ trợ để thăm dò, không là baseline trung tâm hay một bản tái hiện Graph-of-Thoughts được chứng nhận.

Graph tạo hai bản nháp trong một request trước khi tổng hợp; code-generation counter hiện tính chương trình tổng hợp/patch được đánh giá, không tính riêng hai bản nháp. Không đưa graph vào so sánh matched-code-budget khi chưa chuẩn hóa định nghĩa này và cách dừng khi hết budget.

Cấu hình ablation hoạt động: `search.backup=max|mean`, `reward.policy=dual|test_only` (test_only thật sự không gọi critic), `search.max_rethinks_per_node=0` (không rethink), `feedback.mode`. Sampling theo role đi vào request thật. Seed mỗi request = experiment.seed + thứ tự logical request trong bài; tránh Best-of-N dùng cùng seed/prompt ở mọi mẫu. Endpoint vẫn phải được kiểm tra thực tế về hỗ trợ seed; gửi seed không bảo đảm deterministic tuyệt đối.

## 2. Controller v0 chính xác

Đầu vào duy nhất: failure kind của public test đầu tiên thất bại, public pass rate, code hash, lịch sử quan sát public trên cùng đường đi. Trong MCTS, con kế thừa lịch sử feedback của cha; iterative repair giữ lịch sử trong bài. Không đọc hidden verdict, lời giải tham chiếu hay difficulty từ hidden suites.

- Fixed mode luôn yêu cầu mức tương ứng.
- Adaptive gặp CE hoặc TLE dùng facts, vì không có trace hữu ích/an toàn để yêu cầu thêm.
- WA bắt đầu ở trace; các lỗi runtime khác bắt đầu ở facts.
- Đếm chuỗi quan sát không cải thiện. Một lần được tính là cải thiện nếu pass rate tăng và code hash thay đổi; khi có cải thiện thì reset chuỗi.
- Mỗi `feedback.escalate_after` quan sát không tiến triển tăng một mức, tối đa block. Mặc định 1 là **ngưỡng heuristic chưa tune**.
- Trace thất bại/timeout hạ về facts. Block analysis không đủ call budget sau khi dành phần cho sửa/sinh lại code thì hạ về trace. Mọi downgrade có reason và requested/effective level trong artifact.
- Cấu hình nghiên cứu đặt 2 rethink/node để có cơ hội quan sát tăng mức; mọi fixed/adaptive variant phải dùng cùng giới hạn này.

Chính sách này không biết sửa có thành công trên hidden hay không; chỉ cải thiện public cũng có thể overfit. So sánh với fixed feedback và no-adaptation là bắt buộc.

## 3. Model và dữ liệu có thể thay bằng cấu hình

Các model qua endpoint OpenAI-compatible dùng `model.base_url`, `model.model`, `model.api_key_env` và sampling. `model.revision` là metadata khai báo; runner chưa thể tự xác thực trọng số đang phục vụ từ một endpoint bất kỳ. Phải pin model/serving revision ở server trước final benchmark.

Dataset dùng prepared JSONL chứa PublicProblem và một hidden suite JSON cho mỗi ID. Runner không hardcode danh sách tên dataset. Ba adapter raw hiện có: HumanEval, APPS, CodeContests. Dataset mới đúng prepared schema chỉ cần đổi đường dẫn; raw schema mới cần adapter một lần, không sửa solver. Hiện giới hạn Python và các harness stdin/function/assertion (có fallback Solution method), không tuyên bố chấm chuẩn mọi benchmark/ngôn ngữ chỉ bằng đổi tên.

Ví dụ kiểm tra offline:

```bash
python3 -m rethink_mcts.cli benchmark \
  --config configs/research_smoke.yaml \
  --output-dir runs/foundation_dry_run --dry-run
```

Ví dụ chạy toàn luồng bằng mock, không gọi mạng LLM:

```bash
python3 -m rethink_mcts.cli benchmark \
  --config configs/research_smoke.yaml \
  --output-dir runs/foundation_mock_v2
```

Chuẩn bị APPS từ raw local sang thư mục mới, giữ dữ liệu cũ:

```bash
python3 -m rethink_mcts.cli prepare --dataset apps \
  --raw-path data/apps/apps_300.jsonl --output prepared/apps_v2
python3 -m rethink_mcts.cli benchmark \
  --config configs/research_base.yaml \
  --output-dir runs/apps_v2_dry_run --dry-run
```

Đổi model và dataset đã chuẩn hóa mà vẫn chỉ dry-run:

```bash
python3 -m rethink_mcts.cli benchmark \
  --config configs/research_base.yaml --output-dir runs/he_7b_trace \
  --set model.model=Qwen/Qwen2.5-Coder-7B-Instruct \
  --set data.adapter=humaneval \
  --set data.prepared_public_path=prepared/humaneval/public/problems.jsonl \
  --set data.judge_suites_dir=prepared/humaneval/judge/suites \
  --set feedback.mode=trace --dry-run
```

`--dry-run` không gửi request, không tạo thư mục run. Khi chuyển sang thực nghiệm thật, bỏ cờ này sau khi serving/Docker/cohort đã sẵn sàng. Dùng thư mục mới cho mỗi model × dataset × method × seed × budget.

## 4. Development và final test

Không dùng 164 HumanEval và 300 APPS test đã phân tích để gọi là tập development mới hoặc kiểm định độc lập. Dữ liệu hiện tại phục vụ dry-run, regression và exploratory analysis. Chưa tải hoặc chạy LLM trên development cohort mới trong giai đoạn này.

Development dự kiến: APPS train, lấy cohort phân tầng difficulty và khóa ID bằng seed trước pilot. Kiểm tra trùng nội dung với final cohort. Tune ngưỡng controller/sampling trên development; sau đó cố định. Final APPS test nên có phần holdout chưa dùng tune; báo rõ phần đã quan sát. HumanEval là external benchmark thứ hai, có thảo luận contamination và ceiling.

Cohort file là JSON list ID hoặc object `{"problem_ids":[...]}`. `experiment.stage=test` yêu cầu `data.cohort_path` và `experiment.protocol_id` khác unregistered. Runner không cho filter ad hoc trên final cohort. Cơ chế này hỗ trợ kỷ luật thực nghiệm, không thể tự chứng minh người nghiên cứu chưa nhìn hidden data.

Ma trận dự kiến: 3B/7B làm chính, 14B đối chiếu; 3 seeds; code budget 4/8/16. Chạy đầy đủ fixed feedback trên development trước, chỉ đưa cấu hình đã khóa vào final. Không cần tăng số model nếu điều đó làm yếu kiểm soát các yếu tố nhiễu.

## 5. Budget, metrics và giới hạn hiện tại

- `total_model_calls`: logical requests, tính cả expansion/code/rethink/critic/block analysis. `transport_attempts` báo riêng, `tokens_by_role` và tổng input/output lưu usage provider. Missing/retry usage không biết được phải null, không phải 0. Research base đặt retries=0 và require_exact_token_count=true.
- Token cap hiện là cap trên **usage đã nhận**, dừng request tiếp theo khi chạm cap; một request đang chạy có thể vượt cap. Chưa có tokenizer/server reservation cho hard token cap. Báo realized tokens và độ vượt; không gọi đây là strict matched-token experiment cho đến khi có cơ chế reservation hoặc phân tích budget phù hợp.
- Wall-time kiểm tra ở biên request/sandbox; request và trace có deadline riêng. Một public evaluation gồm nhiều test có thể vượt tổng wall cap. Không dùng wall cap này để khẳng định strict matched-latency.
- Các trường context-window/max-format-retries/caching cũ chưa tạo thành capability hoàn chỉnh. Feedback text được giới hạn theo ký tự (ước lượng 4 chars/token từ cấu hình cũ), không cam kết đúng số tokenizer tokens. Cần kiểm tra context bằng tokenizer server trước sweep model thật.
- Correctness chính: phần trăm selected programs pass toàn hidden suite trên **cohort đã khóa**. No-candidate/infra failure báo riêng, không silently giảm denominator; completed-only chỉ để chẩn đoán. Mean hidden pass rate là macro average theo bài đã chấm, không pooled tests.
- HumanEval official assertions đang đóng trong một suite; metric này không đếm từng assertion. CodeContests generated suite chấm riêng, không nhập ngầm vào private metric.
- Tổng solve/judge time được cộng từ từng bài kể cả resume; không dùng thời gian phiên resume làm tổng thời gian thí nghiệm.
- Final cần mean/std nhiều seed, paired bootstrap CI theo bài; so sánh regression, số lần sửa không đổi code, level selection và token breakdown. Chưa thực hiện phân tích thống kê mới bằng mock.

## 6. Artifacts và resume

`manifest.json`: effective config, cohort IDs, hashes dữ liệu/source/prompt, Python/dependencies, git revision và dirty flag. Nó nhận diện trạng thái source bằng hash dù chưa commit. Snapshot revision phục vụ provenance; không chỉ dựa vào tên thư mục chứa chữ 14b.

Mỗi bài có `candidates.json`, `evaluations.json`, `selected.py`/`selected.json`, `usage.json`, `search.json` (tree và stop reason), `requests.json`, `feedback.json`, `judge_results.json`, `completed.json`. Theo config có thể tắt raw requests/trace; final protocol nên giữ để audit. Lỗi có `error.json`, không có completion marker và được retry khi resume.

Chỉ resume nếu manifest khớp; kiểm tra completion record và selected-code hash. Run cũ thiếu schema 2 không được nhập tự động. Đây là resume ở mức **bài hoàn tất**, chưa khôi phục giữa search; lỗi giữa chừng có thể phải sinh lại bài đó. Không chạy đồng thời hai process ghi cùng một output directory.

## 7. Executor và trạng thái kiểm chứng

`trusted_fixture` là subprocess trên host cho fixture/code tin cậy, không phải security sandbox. Docker và host dùng cùng harness/comparator; Docker không tự fallback. Tracing dùng worker riêng, timeout và opcode mapping theo code object/frame. CFG/tracing hiện là Python bytecode implementation có giới hạn; chưa chứng nhận đầy đủ exception-flow CFG cho mọi chương trình Python.

Máy phiên phát triển có Docker binary nhưng daemon không hoạt động; chưa chạy container integration thực. Trước LLM benchmark, cần build/pin image, kiểm tra stdin/function/assertion/trace trên container, resource limits và serving usage. Probe thất bại phải báo infrastructure error, không giả thành bài giải sai.

Đây là nền chạy và đo lường đã có kiểm thử offline; không phải xác nhận mọi hạng mục đặc tả cũ hoặc mọi điều kiện benchmark-production đã hoàn tất.
