# Benchmark RethinkMCTS: Test-only Reward

## 1. Mục tiêu và phạm vi

`test_only` là thí nghiệm ablation của RethinkMCTS: search vẫn dùng LLM để đề xuất thought, sinh code, phân tích test fail và rethink; điểm reward chỉ lấy từ kết quả thực thi public tests. Benchmark dùng cùng cohort `benchmark_v2`: 300 APPS (100 mỗi mức khó) và toàn bộ 164 HumanEval.

| Dataset | Search run | Prompt | Candidate hoàn chỉnh |
|---|---|---|---:|
| APPS | `rethinkmcts_apps_test_only_v1` | `native_v2` | 297/300 |
| HumanEval | `rethinkmcts_humaneval_test_only_v1` | `native_v2` | 164/164 |

Cả hai dùng `qwen2.5-coder:7b-instruct`, digest `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`, chạy inference trên Modal L40S. Kết quả và bài timeout ở [báo cáo thí nghiệm](results/rethinkmcts-test-only-v1.md).

## 2. Hyperparameter

| Tham số | Giá trị |
|---|---:|
| Temperature / top-p | `0.2` / `0.95` |
| Rollouts / width | `2` / `3` thought mỗi expansion |
| Seed | `0` (tie-break cục bộ) |
| P-UCB `c_base` / `c` | `10` / `4` |
| Max rethink mỗi node | `2` |
| Reward mode | `test_only` |
| Reward | `passed_public_tests / total_public_tests` |
| APPS public policy | `half`: `floor(n/2)` test đầu |
| HumanEval public policy | `given_tests` |
| Số failed test đưa vào feedback | Tối đa `1` |
| Giới hạn trace / feedback | `10` block; `5000` ký tự/block; `8000` ký tự feedback |
| Timeout mỗi public test | `5` giây |
| Timeout mỗi problem | `900` giây |
| Problem workers / APPS test worker | `4` / `1` |
| Max tokens Expansion / Code Generation | `null`: không đặt `num_predict` riêng |
| Max tokens Feedback / Rethink | `1024` / `512` |

`null` vẫn chịu giới hạn của model/backend. Số candidate thực tế của một bài phụ thuộc số lần rethink và rollout, không cố định bằng width. Seed không làm response của LLM tất định.

## 3. Search và reward

State gồm bài toán và reasoning path. Mỗi rollout đi qua Selection, Expansion, Evaluation, Backpropagation và có thể Rethink. Selection dùng P-UCB:

```text
P-UCB(s,a) = Q(s,a) + beta(s) * p(a|s) * sqrt(log(N(s))) / (1 + N(s'))
beta(s) = log((N(s) + c_base + 1) / c_base) + c
```

`p(a|s)` lấy từ trường `reasonableness` do LLM cung cấp trong Expansion, rồi chuẩn hóa; không phải token probability. Khi code chạy public tests:

```text
v_test = passed_public_tests / total_public_tests
reward = v_test
```

Reward được backpropagate về root với `Q=max(reward)`. Nếu `v_test<1`, hệ thống phân tích một test fail và có thể rethink thought cuối tối đa hai lần. Nếu `v_test=1`, không gọi LLM tự đánh giá, vẫn tiếp tục/hoàn tất search theo ngân sách rollout. Cuối cùng chọn candidate có reward cao nhất; các candidate cùng reward có thể vẫn khác khả năng pass full tests.

## 4. Cách gửi prompt

Mọi request LLM dùng system message:

```text
You are an expert programming assistant.
```

User message thay đổi theo thao tác. `<statement>` là `question.txt` APPS hoặc `prompt` HumanEval. `<history>` là danh sách thought đánh số; rỗng thì `(none)`. Ký hiệu `[ ... ]` trong các template bên dưới chỉ phần được nối có điều kiện, không phải ký tự literal trong request.

### Expansion

```text
You are the reasoning planner for a code-generation search.
Problem statement:
<statement>
[\n\nStarter code:\n<starter_code.py>]
<execution interface nếu là APPS>

Previous thoughts:
<history>
[\n\nExecution feedback:\n<feedback JSON>]

Produce exactly 3 distinct next reasoning strategies. Do not write code. Return only a JSON list. Each item must contain a short `thought` string and a `reasonableness` number in [0, 1]. The numbers should sum to 1.
```

LLM trả JSON list ba thought và ba reasonableness score. Sau khi parse/normalize, các score là prior cho selection. Feedback chỉ được đưa vào expansion khi node đang có feedback từ test fail.

### Code Generation

```text
You are an expert Python programmer.
Problem statement:
<statement>
[\n\nStarter code:\n<starter_code.py>]
<execution interface nếu là APPS>

Reasoning path:
<history>

Return only the complete Python solution. Include imports and the required function signature when the task is call-based. Do not explain the solution and do not use Markdown fences.
```

Với APPS stdin/stdout, `<execution interface>` được thay bằng đúng đoạn:

```text
Execution interface: standard input/output. The judge runs the source as a standalone Python program. Read from stdin, invoke your solution for the provided input, and print the answer to stdout. A function definition by itself produces no output and fails the tests.
```

Với APPS call-based (`fn_name` có giá trị), đoạn đó là:

```text
Execution interface: call-based. Define `<fn_name>` as a top-level function or a method on `Solution`; the judge calls it with the test arguments. Return the result instead of printing it.
```

HumanEval không nối execution interface và không có APPS starter code. Code response được bóc fence nếu cần, rồi chạy public tests. Official harness không nằm trong prompt generation.

### Verbal Feedback khi test fail

```text
You are a code debugger performing block-level analysis.
Problem statement:
<statement>
<execution interface nếu là APPS>

Reasoning path:
<history>

Candidate code:
<candidate code trong python fence>

Failed public test:
<test fail đầu tiên: index, status, expected, actual, error, diagnosis>

Execution trace by AST statement block:
<trace>

Identify the first incorrect block using the trace. Return JSON containing `block`, `correct`, and `explanation`. Do not rewrite the code.
```

Với APPS stdin/stdout, prompt có thêm hướng dẫn: khi stdout rỗng mà kỳ vọng có output, kiểm tra driver/print trước khi quy lỗi cho thuật toán. `trace` được lấy từ runtime/AST trên candidate vừa sinh, không phải từ official private tests.

### Rethink khi còn ngân sách

```text
You are refining one erroneous reasoning step in a code-generation search.
Problem statement:
<statement>
<execution interface nếu là APPS>

Thoughts:
Thought-1: <thought 1>
...

Generated code:
<candidate code trong python fence>

Execution feedback:
<feedback JSON>

Replace only the most recent thought with a better reasoning step that avoids the observed error. Return one or two sentences of thought only, never code.
```

LLM trả một thought mới, thay thought gần nhất tại node; sau đó lại sinh một candidate code để chấm public tests. Request Rethink không sửa trực tiếp `solution.py` của candidate cũ.

### Self Evaluation

**Không có request này trong `test_only`.** Kể cả khi candidate pass toàn bộ public tests, hệ thống không hỏi LLM chấm khả năng pass unseen tests. Đây là khác biệt trực tiếp so với `dual`.

## 5. Final judge, artifact và giới hạn kết luận

Search APPS dùng nửa đầu test làm public; final judge chấm toàn bộ test APPS. Search HumanEval dùng `given_tests`; final judge chạy official harness. Candidate thiếu được tính 0 trong mẫu số benchmark, nhưng không có báo cáo chạy test giả cho bài chưa có code.

Artifact mỗi bài nằm tại `outputs/rethinkmcts/<run>/<model>/<dataset>/<problem_id>/`, gồm `search_summary.json`, `tree.json`, `events.jsonl`, `final_solution.py` và `candidates/`. Mỗi request ghi model, operation, prompt version, finish reason và token usage; config run ở `run_config.json`. Bảng rejudge nằm dưới `outputs/rethinkmcts_evaluations/`.

So với `dual`, APPS `test_only` có 297/300 candidate còn `dual` có 295/300; HumanEval `dual` dùng prompt `native_v1` trên Modal L4, trong khi `test_only` dùng `native_v2` trên L40S. Vì thế chênh lệch điểm hiện tại chưa thể xem là hiệu ứng riêng của việc bỏ `v_llm`. Xem [báo cáo dual](rethinkmcts-dual-report.md) và [baseline](baseline-report.md) để đối chiếu.
