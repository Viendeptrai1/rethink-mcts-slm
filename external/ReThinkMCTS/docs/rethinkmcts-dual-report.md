# Benchmark RethinkMCTS: Dual Evaluation

## 1. Run và dữ liệu

Benchmark dùng `qwen2.5-coder:7b-instruct` trên cohort `benchmark_v2`: 300 APPS (100 bài mỗi mức khó) và 164 HumanEval. Bảng `dual` hiện ghép hai search run có provenance khác nhau:

| Dataset | Search run | Prompt | Hạ tầng LLM | Candidate hoàn chỉnh |
|---|---|---|---|---:|
| APPS | `rethinkmcts_apps_interface_v2_half_w4` | `native_v2` | Modal L40S | 295/300 |
| HumanEval | `rethinkmcts_qwen25_modal_v1` | `native_v1` | Modal L4 | 164/164 |

Vì vậy hàng kết quả `dual` hiện tại không phải một run đồng nhất prompt version trên hai dataset. Chi tiết kết quả và bài thiếu candidate ở [báo cáo APPS](results/rethinkmcts-apps-native-v2-w4-retry.md) và [báo cáo HumanEval](results/rethinkmcts-modal-humaneval-v1.md).

## 2. Cấu hình

| Tham số | Giá trị |
|---|---:|
| Model | `qwen2.5-coder:7b-instruct` |
| Temperature / top-p | `0.2` / `0.95` |
| Rollouts / width | `2` / `3` thought mỗi expansion |
| Seed | `0` (tie-break cục bộ; không khóa sampling của model) |
| P-UCB `c_base` / `c` | `10` / `4` |
| Reward `a` / `b` | `0.8` / `0.2` |
| Max rethink mỗi node | `2` |
| APPS public policy | `half`: nửa đầu test, `floor(n/2)` |
| HumanEval public policy | `given_tests` |
| Số failed test đưa vào feedback | Tối đa `1` |
| Giới hạn trace / feedback | `10` block; `5000` ký tự/block; `8000` ký tự feedback |
| Timeout mỗi public test | `5` giây |
| Timeout mỗi problem | `900` giây |
| Problem workers | APPS `4`; HumanEval `1` |
| Max tokens mặc định | `null`: không đặt `num_predict` riêng cho Expansion và Code Generation |
| Max tokens Self Evaluation / Feedback / Rethink | `256` / `1024` / `512` |

`max_tokens=null` vẫn chịu giới hạn của model và backend. `width=3` là số thought được đề xuất khi expansion; số code candidate thực tế có thể nhiều hơn do rethink và nhiều rollout.

## 3. Luồng search

State chứa đề bài và chuỗi thought đã tích lũy. Mỗi rollout chọn leaf bằng P-UCB, yêu cầu model đề xuất ba thought, chọn child, sinh code hoàn chỉnh, chạy public tests và gán reward. Node được cập nhật bằng backpropagation với `Q=max(reward)`. Khi public test fail, hệ thống lấy test fail đầu tiên, trace và phân tích feedback, rồi có thể thay thought mới nhất tại node và sinh code lại. Cuối search chọn candidate reward cao nhất; final judge chấm candidate được chọn bằng toàn bộ APPS tests hoặc official HumanEval harness.

```text
P-UCB(s,a) = Q(s,a) + beta(s) * p(a|s) * sqrt(log(N(s))) / (1 + N(s'))
beta(s) = log((N(s) + c_base + 1) / c_base) + c
```

`p(a|s)` là `reasonableness` do LLM trả trong JSON, được parser chuẩn hóa; đó không phải token log probability.

```text
v_test = passed_public_tests / total_public_tests
reward = v_test                         nếu v_test < 1
reward = 0.8 * v_test + 0.2 * v_llm   nếu v_test = 1
```

`v_llm` nằm trong `[-1,1]`. Model chỉ tự đánh giá code khi tất cả public tests pass. Nếu public tests fail, không có request Self Evaluation; `reward=v_test` và hệ thống đi theo nhánh feedback/rethink.

## 4. Cách gửi request và prompt

Mỗi thao tác LLM dùng một request chat gồm system message cố định và user message theo thao tác:

```text
You are an expert programming assistant.
```

Các mẫu dưới đây là nguyên văn template từ source; các chỗ `<...>` được thay bằng dữ liệu của bài hoặc trạng thái node. `Previous thoughts` và `Reasoning path` là danh sách đánh số `1. ...`, `2. ...`; khi trống là `(none)`. Header của Expansion/Code có dạng `Problem statement:\n<statement>`, sau đó có thể nối `\n\nStarter code:\n<starter_code>`.

### Expansion: `native_v2` APPS

```text
You are the reasoning planner for a code-generation search.
Problem statement:
<question.txt>
[\n\nStarter code:\n<starter_code.py>]
<execution interface>

Previous thoughts:
<numbered thoughts hoặc (none)>
[\n\nExecution feedback:\n<feedback JSON>]

Produce exactly 3 distinct next reasoning strategies. Do not write code. Return only a JSON list. Each item must contain a short `thought` string and a `reasonableness` number in [0, 1]. The numbers should sum to 1.
```

`<execution interface>` phụ thuộc `fn_name` trong APPS `input_output.json`:

```text
Execution interface: standard input/output. The judge runs the source as a standalone Python program. Read from stdin, invoke your solution for the provided input, and print the answer to stdout. A function definition by itself produces no output and fails the tests.
```

Hoặc khi `fn_name` có giá trị:

```text
Execution interface: call-based. Define `<fn_name>` as a top-level function or a method on `Solution`; the judge calls it with the test arguments. Return the result instead of printing it.
```

`native_v1` HumanEval dùng cùng cấu trúc Expansion nhưng không có đoạn `Execution interface`; `<statement>` là `prompt` của HumanEval, không có APPS starter code. Feedback chỉ được nối khi node có feedback thật.

### Code Generation

```text
You are an expert Python programmer.
Problem statement:
<statement>
[\n\nStarter code:\n<starter_code>]
<execution interface nếu là APPS native_v2>

Reasoning path:
<numbered thoughts hoặc (none)>

Return only the complete Python solution. Include imports and the required function signature when the task is call-based. Do not explain the solution and do not use Markdown fences.
```

HumanEval `native_v1` không có đoạn interface. Code sau khi bóc Markdown fence được chạy trên public tests; reference solutions và official harness không nằm trong prompt này.

### Self Evaluation: chỉ khi `v_test=1`

````text
You are a strict code correctness evaluator.
Problem statement:
<statement>

Reasoning path:
<numbered thoughts hoặc (none)>

Candidate code:
```python
<candidate code>
```

The candidate already passes all public tests. Estimate whether it passes unseen edge cases. Return only JSON with one numeric key `evaluation` in [-1, 1].
````

Đây là **user prompt**. LLM trả `{"evaluation": <score>}`; parser đọc score và dùng trong reward.

### Verbal Feedback: khi `v_test<1`

```text
You are a code debugger performing block-level analysis.
Problem statement:
<statement>
<execution interface nếu là APPS native_v2>

Reasoning path:
<numbered thoughts hoặc (none)>

Candidate code:
<candidate code trong python fence>

Failed public test:
<test fail đầu tiên: index, status, expected, actual, error, diagnosis>

Execution trace by AST statement block:
<trace>

<hướng dẫn phân tích block theo prompt version>
```

`native_v2` yêu cầu xác định block sai đầu tiên và trả JSON `block`, `correct`, `explanation`. Với APPS stdin/stdout, prompt còn nhắc kiểm tra driver/print nếu stdout rỗng. `native_v1` HumanEval yêu cầu cùng ba trường JSON và phân tích trace, nhưng không có hướng dẫn interface mới này.

### Rethink: khi còn ngân sách sửa

```text
You are refining one erroneous reasoning step in a code-generation search.
Problem statement:
<statement>
<execution interface nếu là APPS native_v2>

Thoughts:
Thought-1: <thought 1>
...

Generated code:
<candidate code trong python fence>

Execution feedback:
<feedback JSON>

Replace only the most recent thought with a better reasoning step that avoids the observed error. Return one or two sentences of thought only, never code.
```

Kết quả thay thought cuối tại node. Candidate cũ và reward đã ghi được giữ trong artifact. Request Rethink không gửi official/private tests.

## 5. Artifact và giới hạn diễn giải

Mỗi problem lưu `search_summary.json`, `tree.json`, `events.jsonl`, `final_solution.py` và các candidate dưới `outputs/rethinkmcts/<run>/<model>/<dataset>/<problem_id>/`. Metadata request chứa model, prompt version, finish reason và token usage. `run_config.json` lưu cấu hình run. Bảng final judge nằm dưới `outputs/rethinkmcts_evaluations/`.

APPS `dual` còn 5 bài thiếu candidate trong run chính. HumanEval `dual` là prompt `native_v1`; vì vậy chênh lệch với HumanEval `test_only` không thể quy riêng cho thay đổi reward. Source của prompt `native_v1` được kiểm tra tại commit `eb247acb`; prompt `native_v2` ở `rethinkmcts/prompts.py` hiện tại.

## 6. Biến thể evaluator riêng (đã chuẩn bị, chưa chạy)

Run pilot mới giữ generator `qwen2.5-coder:7b-instruct` và định tuyến riêng
operation `self_evaluation` sang `qwen2.5-coder:14b-instruct`. Các operation
khác vẫn dùng generator; request metadata ghi model thực tế. Reward Dual,
prompt, parser và điều kiện gọi evaluator chỉ khi pass toàn bộ public tests
không đổi. Cấu hình run ghi evaluator model và digest riêng. Hướng dẫn Modal
đầy đủ ở [runbook pilot](runbooks/rethinkmcts-external-evaluator-pilot.md).

APPS chỉ chạy manifest cố định 30 bài, 10 bài mỗi độ khó; HumanEval chạy đủ
164 bài. Đây là pilot, không phải benchmark APPS 300 và không được ngoại suy.
Reporter riêng tạo bảng ở `outputs/benchmarks/<run>/<generator>/apps30_pilot/`;
finalizer 300+164 hiện có không dùng cho run này.
