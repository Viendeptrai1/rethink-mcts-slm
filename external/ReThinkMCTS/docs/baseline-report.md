# Benchmark Baseline: Direct Generation

## 1. Mục tiêu

Baseline đo khả năng sinh mã trực tiếp của LLM khi không có MCTS, feedback kiểm thử hoặc rethink. Mỗi bài được xử lý độc lập:

```text
đọc đề bài -> xây prompt -> gửi một request tới LLM -> bóc code -> lưu candidate
-> chấm candidate bằng executor ở stage evaluation
```

Baseline không dùng lời giải tham khảo, test case hoặc kết quả chấm trong prompt sinh code.

## 2. Dataset và phạm vi benchmark

| Dataset | Split | Quy mô generation | Cohort dùng cho bảng benchmark |
|---|---|---:|---:|
| APPS | `test` | 5.000 bài | 300 bài: 100 Introductory, 100 Interview, 100 Competition |
| HumanEval | `test` | 164 bài | Toàn bộ 164 bài |

Cohort được khóa trong `data/samples/benchmark_v2/`. Baseline và RethinkMCTS phải dùng cùng manifest problem ID. Có thể sinh candidate cho toàn bộ dataset, nhưng bảng kết quả chỉ chấm cohort đã công bố.

## 3. Cách đọc dữ liệu

### APPS

Loader đọc `question.txt` và `starter_code.py` nếu có. Loader không đọc `solutions.json` hoặc `input_output.json` trong bước generation; model không nhận lời giải tham khảo hoặc test case APPS.

### HumanEval

Loader đọc `prompt`, `task_id` và `entry_point` từ dataset Arrow. Các trường `canonical_solution` và `test` của official harness không được đưa vào prompt. `given_tests` chỉ phục vụ pipeline MCTS, không thuộc baseline direct-generation.

## 4. Prompt gửi tới LLM

Mỗi request dùng một `system` message cố định và một `user` message được tạo từ bài toán.

### System prompt

```text
You are an expert Python programmer.
Solve the given programming problem correctly and efficiently.
Return only complete Python source code. Do not use Markdown fences and do not explain the solution.
```

### User prompt cho APPS không có starter code

```text
Programming problem:

<nội dung question.txt>

Return a complete program that reads input and writes output.
```

### User prompt cho APPS có starter code

```text
Programming problem:

<nội dung question.txt>

Starter code:

<nội dung starter_code.py>

Complete the starter code and return the full program.
```

### User prompt cho HumanEval

```text
Complete the following Python function. Return the full Python source, including the supplied signature and docstring.

<nội dung prompt của bài HumanEval>
```

Model phải trả về toàn bộ Python source, không chỉ phần thân hàm.

## 5. Cấu hình generation

Config hiện tại nằm ở `baselines/direct_generation/configs/qwen25_coder_7b_instruct.json`:

| Tham số | Giá trị |
|---|---:|
| Model | `qwen2.5-coder:7b-instruct` |
| Prompt version | `v1` |
| Temperature | `0.2` |
| Top-p | `0.95` |
| Max tokens | `8192` |
| Reasoning effort | Không đặt |
| Số candidate mỗi bài | 1 |

Request được gửi qua client OpenAI-compatible tới provider cấu hình trong `.env`/Modal. Token, endpoint và secret không nằm trong config benchmark và không được ghi vào artifact.

`generation-workers` chỉ quyết định số request có thể chờ đồng thời; không tạo thêm candidate cho cùng một bài. `delay` chỉ giãn thời điểm scheduler gửi request.

## 6. Bóc code và lưu candidate

Response gốc được lưu trước khi xử lý. Nếu model trả code trong Markdown fence, pipeline lấy fence Python dài nhất; nếu không có fence, dùng toàn bộ response sau khi trim. Artifact hoàn chỉnh cần có response và solution không rỗng, cùng `finish_reason` là `stop` hoặc provider không trả trường này.

```text
outputs/baselines/direct_generation/<run>/<model>/<dataset>/<problem_timestamp>/
├── problem.txt       # user prompt thực tế
├── response.txt      # response nguyên bản
├── solution.py       # code sau khi bóc fence
└── metadata.json      # model, tham số, finish reason, token usage
```

Manifest và log batch nằm tại `outputs/baselines/batch_manifests/<run>/<model>/`. Resume được bật mặc định: bài đã có artifact hoàn chỉnh sẽ được bỏ qua; bài rỗng, bị cắt bởi token hoặc request lỗi sẽ được xử lý lại.

## 7. Evaluation và metric

Evaluation không gọi LLM lại. Executor đọc candidate đã lưu rồi chạy code:

- APPS: chạy toàn bộ test trong `input_output.json` của cohort;
- HumanEval: chạy official harness từ trường `test`; không có hidden test độc lập nên báo cáo `Pass@1`.

Với APPS, báo cáo gồm macro Pass Rate, Pass@1 và micro Pass Rate. Candidate thiếu hoặc không hoàn chỉnh được tính là không pass trong mẫu số benchmark. Kết quả nằm dưới `outputs/baselines/evaluations/<run>/<model>/<dataset>/`.

## 8. Ý nghĩa của baseline

Baseline trả lời câu hỏi: “Nếu chỉ đưa đề bài cho model một lần, không cho model xem test và không sửa code qua feedback, chất lượng đạt bao nhiêu?” Đây là mốc đối chứng cho RethinkMCTS. So sánh chỉ hợp lệ khi giữ nguyên model, cohort ID, executor, timeout và chính sách metric.

Chi tiết schema dataset nằm ở [dataset-report.md](dataset-report.md), còn lệnh chạy nằm ở [runbooks/baseline-full.md](runbooks/baseline-full.md).

## 9. Ba benchmark được so sánh

Ba benchmark dùng cùng model `qwen2.5-coder:7b-instruct` và cohort
`benchmark_v2`. Prompt, hạ tầng inference và độ phủ candidate của các run đã
chạy khác nhau; xem báo cáo riêng trước khi diễn giải chênh lệch điểm.

### 9.1. Direct-generation baseline

Baseline không có state tree, action thought, selection, expansion,
backpropagation hoặc rethink. Mỗi bài chỉ có một candidate trực tiếp từ LLM.

| Hyperparameter generation | Giá trị |
|---|---:|
| Model | `qwen2.5-coder:7b-instruct` |
| Prompt version | `v1` |
| Temperature | `0.2` |
| Top-p | `0.95` |
| Max tokens | `8192` |
| Candidate mỗi bài | `1` |
| MCTS rollouts | Không áp dụng |
| MCTS width | Không áp dụng |
| Reward | Không áp dụng trong generation |

System prompt và ba loại user prompt của baseline được mô tả ở mục 4.

### 9.2. RethinkMCTS `dual`

Đây là phiên bản đầy đủ dùng Dual Evaluation. Mỗi node lưu reasoning path,
thought, candidate code, số visit, prior `p(a|s)`, reward và feedback. Search
chọn nhánh bằng P-UCB, mở rộng bằng các thought mới, sinh code ở node hiện tại,
chạy public tests, sau đó backpropagate reward. Nếu candidate fail public test,
thought gần nhất có thể được rethink tại chỗ.

| Hyperparameter | Giá trị đã chạy |
|---|---:|
| Model | `qwen2.5-coder:7b-instruct` |
| Prompt version | APPS `native_v2`; HumanEval `native_v1` |
| Temperature | `0.2` |
| Top-p | `0.95` |
| Max tokens | `null` (không gửi giới hạn riêng) |
| Rollouts | `2` |
| Width / thoughts mỗi expansion | `3` |
| Seed | `0` |
| `c_base` | `10` |
| `c` / exploration weight | `4` |
| Max rethink mỗi node | `2` |
| Public policy APPS | `half` = `floor(total_tests / 2)` |
| Reward khi `v_test < 1` | `v_test` |
| Reward khi `v_test = 1` | `0.8 * v_test + 0.2 * v_llm` |

HumanEval dùng `given_tests` trong search; official harness chỉ dùng ở final
evaluation. APPS dùng nửa đầu test làm public trong search; final evaluation
chạy toàn bộ test. Xem [báo cáo dual](rethinkmcts-dual-report.md) để đọc prompt
và nguồn của từng run.

### 9.3. RethinkMCTS `test_only` (không dùng `v_llm`)

Đây là ablation của `dual` về công thức reward và request self-evaluation.
Các hyperparameter search chính được giữ nguyên. APPS cùng dòng prompt
`native_v2`; HumanEval `dual` thực tế dùng `native_v1` nên hai run HumanEval
còn khác prompt và hạ tầng inference.

| Hyperparameter | Giá trị đã chạy |
|---|---:|
| Model | `qwen2.5-coder:7b-instruct` |
| Prompt version | `native_v2` |
| Temperature | `0.2` |
| Top-p | `0.95` |
| Max tokens | `null` (không gửi giới hạn riêng) |
| Rollouts | `2` |
| Width / thoughts mỗi expansion | `3` |
| Seed | `0` |
| `c_base` | `10` |
| `c` / exploration weight | `4` |
| Max rethink mỗi node | `2` |
| Public policy APPS | `half` = `floor(total_tests / 2)` |
| Reward | `v_test = passed_public_tests / total_public_tests` |
| LLM self-evaluation `v_llm` | Không gọi, không dùng |

Xem [báo cáo test-only](rethinkmcts-test-only-report.md) để đọc từng prompt và
điều kiện gọi. Chênh lệch kết quả đã chạy chưa đủ để quy nguyên nhân riêng cho
`v_llm`, đặc biệt ở HumanEval do khác prompt version.

### 9.4. Tham số điều phối, không phải hyperparameter thuật toán

Các tham số sau ảnh hưởng thời gian chạy và độ ổn định hạ tầng, nhưng không
thay đổi công thức MCTS:

| Tham số | Vai trò |
|---|---|
| `workers` | Số bài có thể search đồng thời |
| `apps_test_workers` | Số worker chấm test APPS trong một bài |
| `problem_timeout_seconds` | Giới hạn thời gian cho toàn bộ search của một bài |
| timeout mỗi test | Giới hạn khi executor chạy từng test |
| Modal GPU/container | Hạ tầng phục vụ LLM, không phải một thành phần của reward |

Các tham số này phải được ghi trong metadata của từng run để phân biệt thay
đổi thuật toán với thay đổi hạ tầng.
