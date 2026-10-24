# RethinkMCTS: thuật toán từng bước

Tài liệu này giải thích **bản native tại `rethinkmcts/` đang làm gì**, theo mạch
State/Action → Selection → Expansion → Evaluation → Verbal Feedback →
Backpropagation → Rethink → Final Selection. Công thức gốc nằm trong
[lý thuyết paper](../docs/theory-rethinkmcts.md); các điểm chưa tương đương
được ghi tại [implementation audit](../docs/implementation-audit.md).

**Trạng thái:** mới kiểm thử offline bằng fake LLM/executor. Chưa smoke Ollama
và chưa chạy benchmark MCTS, nên các phần dưới là mô tả thuật toán và code,
**không phải kết quả thực nghiệm**.

## 0. State, Action, Reward: MCTS + LLM search cái gì?

MCTS **search trong không gian thought**, không search token Python hay source
code trực tiếp. Một node là một trạng thái suy luận; một action là một thought
mới. LLM sinh các thought để mở rộng cây, rồi sinh code hoàn chỉnh từ chuỗi
thought tại node được chọn. Code được *thực thi để đánh giá node*, chứ bản thân
code không phải action của cây.

Luồng các bước dưới đây do [workflow.py](workflow.py) (`LangGraph StateGraph`)
điều phối. Pydantic kiểm tra state điều phối và thought từ Expansion; công thức
P-UCB, reward và executor vẫn là code miền riêng. Graph hiện chạy tuần tự và
**chưa bật checkpointer**, nên không có resume giữa chừng.

$$
s_t=(P,z_1,z_2,\ldots,z_t),\qquad a_t=z_{t+1}
$$

$$
s_{t+1}=\operatorname{CONCAT}(s_t,a_t)
       =(P,z_1,z_2,\ldots,z_t,z_{t+1}).
$$

| Thành phần | Ý nghĩa |
| --- | --- |
| `P` | Đề bài; root chỉ có `P` |
| `z_1,...,z_t` | Reasoning path: các thought theo thứ tự từ root đến node hiện tại |
| `a_t` | Một thought tiếp theo, tạo một child |
| `r` | Reward nội bộ từ public tests và, nếu pass hết, LLM self-evaluation |

Ví dụ:

```text
P: tìm đáp án nhỏ nhất thỏa điều kiện
  └─ z1: "Dùng binary search trên đáp án"
       └─ z2: "Kiểm tra tính khả thi bằng greedy"
            └─ LLM sinh complete Python code từ (P, z1, z2)
                 └─ chạy public tests → reward / feedback
```

Giữ reasoning path cho phép feedback sửa **cách suy nghĩ dẫn đến code sai**.
Nếu state chỉ là code, quan hệ giữa quyết định thuật toán và lỗi thực thi sẽ
bị mất. Transition chỉ nối thought, không dùng world model để tưởng tượng
state như RAP. `ProblemContext` giữ `P`; `SearchNode` trong [tree.py](tree.py)
giữ thoughts, parent, children, prior, visit count, Q, feedback và code gần nhất.

Reward `r` **không phải điểm benchmark cuối**: private/hidden tests tuyệt đối
không được dùng để chọn nhánh, Rethink hay tính reward.

## 1. Selection: chọn nhánh nào?

Từ root, nếu node đã có children, tính P-UCB cho **mọi child** rồi chọn child
điểm cao nhất. Lặp lại đến leaf chưa có con.

$$
\operatorname{P\text{-}UCB}(s,a)=Q(s,a)+\beta(s)\,p(a\mid s)
\frac{\sqrt{\log N(s)}}{1+N(s')},
\qquad
\beta(s)=\log\!\left(\frac{N(s)+c_{base}+1}{c_{base}}\right)+c.
$$

| Ký hiệu | Trong code |
| --- | --- |
| `s`, `s'` | Node cha và child tạo bởi action `a` |
| `Q(s,a)` | `child.q_value`: **reward lớn nhất**, không phải trung bình |
| `N(s)`, `N(s')` | `parent.visit_count`, `child.visit_count` |
| `p(a\mid s)` | `child.prior`: reasonableness LLM tự chấm rồi normalize; **không phải** token probability thực của model |
| `c_base`, `c` | Mặc định `10` và `4` |

`Q=max` giữ bằng chứng tốt nhất rằng một hướng suy luận có tiềm năng: một lần
sinh code tệ không phủ nhận hoàn toàn nhánh đó. Prior đưa đánh giá ban đầu
của LLM vào exploration; mẫu số `1+N(s')` giảm ưu tiên cho child đã thăm nhiều.
`beta(s)` tăng theo log số lần thăm parent để exploration không bị triệt tiêu
quá nhanh. Native **không** ưu tiên cứng child chưa thăm ngoài công thức.

**Trường hợp biên cần phân biệt với ghi chú lý thuyết:** trong
[policies.py](policies.py), exploration bằng `0` khi `N(s) <= 1` (tránh
`log(0)`; `log(1)=0`). Với children đều chưa thăm và `Q=0`, prior **chưa**
phân biệt chúng ở lần đầu: điểm bằng nhau và tie-break bằng RNG cục bộ theo
`--seed`. Khi `N(s)>1`, nếu hai child cùng `N(s')=0` và `Q=0`, điểm của chúng
tỷ lệ với `p(a|s)` như suy luận trong ghi chú. Seed không cố định sampling của
LLM/provider.

## 2. Expansion: sinh các action mới

Tại leaf, LLM sinh đúng `k=width` thought khác nhau, mặc định `k=3`, mỗi
thought có `reasonableness` trong `[0,1]`. Parser yêu cầu đúng số lượng,
normalize score về tổng `1`, rồi tạo một child cho mỗi thought. **Chưa sinh
code ở bước này.**

$$
[(z^1,e^1),\ldots,(z^k,e^k)]\sim
\begin{cases}
p((z,e)^{1:k}\mid s,f), & \text{nếu node có verbal feedback }f,\\
p((z,e)^{1:k}\mid s), & \text{nếu không có }f.
\end{cases}
$$

`e^i` được lưu làm prior `p(a|s)` cho Selection sau này; child có state
`CONCAT(s,z^i)`. Feedback chỉ vào prompt khi node thật sự từng fail. Xem
[parsing.py](parsing.py), [prompts.py](prompts.py), [search.py](search.py).

**Thứ tự của native:** select tới leaf → expand leaf → P-UCB chọn **một child
vừa tạo** để Evaluation. Các child khác nằm lại trong cây. Algorithm 1 của
paper ghi `GENERATE(node)` sau Expansion nhưng không chỉ rõ đánh giá leaf cũ
hay child mới; đây là lựa chọn cụ thể của bản native, **không nên khẳng định
paper đã chỉ định như vậy**.

## 3. Evaluation: đánh giá node bằng gì?

LLM nhận `P` và toàn bộ reasoning path của child được chọn để sinh **complete
Python code**. Executor chạy code trên public tests:

$$
v_{test}=\frac{\text{số public tests pass}}{\text{tổng public tests}}.
$$

Vì reasoning path đã đủ để sinh một chương trình hoàn chỉnh, RethinkMCTS
dùng direct Evaluation thay cho simulation tưởng tượng tới terminal state của
MCTS cổ điển. Dual Evaluation trong [reward.py](reward.py):

$$
r=\begin{cases}
v_{test}, & 0\le v_{test}<1,\\
a\,v_{test}+b\,v_{llm}, & v_{test}=1,
\end{cases}
\qquad a=0.8,\;b=0.2,\;v_{llm}\in[-1,1].
$$

- **Fail public test:** `r=v_test`, không gọi LLM self-evaluation.
- **Pass hết public tests:** gọi LLM self-evaluation một lần. Với trọng số
  mặc định, reward thuộc `[0.6,1.0]`.
- `v_test=1` không chứng minh hidden tests sẽ pass; `v_llm` chỉ là ước lượng
  bổ sung khi public tests không còn khả năng phân biệt.

APPS search dùng **nửa đầu** test cases trong `input_output.json` làm public,
nửa sau chỉ chấm candidate cuối. HumanEval search dùng `given_tests` đã pin
trong `data/humaneval/public_tests.jsonl`; nếu thiếu sẽ dừng, không âm thầm
chấm 0 public test. Official harness đầy đủ chỉ chạy sau search. Policy thực
tế nằm trong [runner.py](runner.py).

## 4. Verbal Feedback: khi code sai

Khi `v_test<1`, native lấy failed public test đầu tiên, replay code để lấy
runtime trace, rồi đưa đề bài + reasoning path + code + failed test +
expected/actual/error + trace cho LLM phân tích. Feedback `f` được lưu **tại
node hiện tại**, không truyền lên ancestor.

**Giới hạn cần nói rõ:** native đang dùng AST statement spans và
`sys.settrace` để ghi giá trị biến trước/sau statement. Nó **chưa xây CFG/
basic blocks đầy đủ** như paper/repo tác giả. Với exception, nhiều statement
cùng dòng hoặc trace bị timeout, thông tin có thể thiếu. Feedback là tín hiệu
sửa lỗi, không phải bằng chứng root cause chắc chắn.

## 5. Backpropagation: cập nhật đường đi

Sau mỗi Evaluation, kể cả code được sinh lại sau Rethink, scalar reward lan
từ node hiện tại về root:

$$
N(u)\leftarrow N(u)+1,\qquad
Q(u)\leftarrow\max(Q(u),r),
\quad\forall u\in\operatorname{path}(\text{current}\to\text{root}).
$$

Ancestor cần `Q` để so sánh các nhánh trong rollout sau. Ngược lại, verbal
feedback mô tả lỗi của **một code cụ thể** nên chỉ giữ ở node hiện tại; đẩy
nó lên parent sẽ gán lỗi cho một reasoning state khác.

## 6. Rethink: thay thought gần nhất

$$
z_{new}\sim p(z\mid s,f,z_{old}).
$$

Nếu `v_test != 1`, còn ngân sách `max_rethink_times` và LLM trả thought mới
không rỗng, native thay thought cuối **tại chính node hiện tại**:

```text
(P, z1, z2_old) → (P, z1, z2_new)
```

Nó không tạo child "reflection" và không sửa parent. Sau mỗi lần thay, LLM
sinh code hoàn chỉnh mới; executor chạy lại public tests, tạo reward/feedback
mới. Dừng khi pass hết hoặc hết số lần sửa. Nếu vẫn fail và còn rollout, node
Expansion với feedback cuối (`RETHINK_NEXT`). Candidate/code/thought snapshot
cũ được giữ trong `CandidateRecord`, không sửa lại artifact của candidate cũ.

Để không gán thống kê của *action cũ* cho thought mới, [tree.py](tree.py)
reset visit/Q/prior của node bị thay. Ancestor không đổi state nên vẫn giữ
lịch sử reward đã backprop. Điều này **không** xóa reward/candidate cũ khỏi
danh sách ứng viên chọn đáp án cuối.

**Vì sao không sửa parent?** Parent có thể đã tích lũy reward từ nhiều child;
đổi nội dung parent sẽ làm lịch sử đó không còn ứng với state hiện tại. Paper
cũng giả định parent đã được kiểm thử/rethink khi nó được mở rộng. Giả định
này chỉ đảm bảo tính nhất quán nội bộ, **không** chứng minh parent đúng trên
hidden tests hoặc đủ tốt về độ phức tạp. Native chưa có TLE-aware reward hay
cơ chế tìm thought gốc gây lỗi ở tầng sâu hơn.

## 7. Final Selection và benchmark

Hết `rollouts`, native chọn **candidate có reward cao nhất** trong mọi code
đã sinh, kể cả code trước Rethink. Không chọn most-visited path. Chỉ sau khi
chọn mới chấm code đó trên toàn bộ APPS tests hoặc official harness
(HumanEval). Kết quả cuối **không** quay lại cập nhật cây.

Prompt APPS `native_v2` lấy `fn_name` từ `input_output.json`: với bài
stdin/stdout yêu cầu đọc stdin và in stdout, với bài call-based yêu cầu
trả kết quả từ đúng hàm/method. Khi stdout rỗng dù test đợi output,
executor ghi chẩn đoán vào verbal feedback để Rethink có thể sửa
entrypoint. Public split mặc định `half` theo upstream; `half_min2` là
policy nghiên cứu riêng để các bài 3 test có 2 public test. Bảng run cũ
vẫn thuộc `native_v1`, không phản ánh sửa đổi này.

**Phân biệt paper với dự án:** paper đánh giá APPS 300 bài (100 bài mỗi mức
khó) và HumanEval 164 bài. Benchmark mới dùng đúng cohort APPS 300 của nhóm
đối chiếu và toàn bộ HumanEval trong `data/samples/benchmark_v2/`. Baseline
đã hoàn thành trước đó dùng **100 APPS + 100 HumanEval** tại
`data/samples/evaluation_v1/` và không được gán sang cohort mới. MCTS runner
được điều phối tuần tự qua [batch.py](batch.py) cho đúng 300+164 bài, có
checkpoint cấp problem; chưa có kết quả MCTS thật.

Khi tổng hợp trên sample của dự án:

$$
\text{APPS Pass Rate}=\operatorname{mean}_{i}
\left(\frac{\text{all tests pass}_i}{\text{all tests}_i}\right),
\quad
\text{Pass@1}=\frac{\#\text{bài pass toàn bộ APPS tests}}
{\#\text{bài trong sample}}.
$$

HumanEval chỉ báo Pass@1 trên official harness; không có cột Pass Rate riêng.
Reward public-test của search và metric all-tests cuối phải tách bạch.

## Chi phí mỗi node / mỗi rollout

Selection và Backpropagation **không gọi LLM**. Một Expansion gọi LLM **một
lần để lấy `k` thought**, không phải `k` lần. Mỗi Evaluation gọi LLM một lần
sinh code và chạy public tests; nếu pass gọi thêm self-evaluation, nếu fail
gọi thêm verbal feedback và replay trace. Mỗi Rethink gọi LLM một lần sửa
thought, sau đó lại sinh code + Evaluation. Nếu fail cuối và còn rollout,
`RETHINK_NEXT` thêm một request Expansion.

| Sau một Expansion | Request LLM |
| --- | ---: |
| Candidate đầu pass public | `1 expand + 1 code + 1 self-eval = 3` |
| Candidate đầu fail, không Rethink | `1 expand + 1 code + 1 feedback = 3` |
| Fail, Rethink một lần rồi pass | `1 expand + 1 code + 1 feedback + 1 rethink + 1 code + 1 self-eval = 6` |

Nếu mọi candidate đều fail qua `m` lần Rethink: trước `RETHINK_NEXT` cần
`3+3m` request LLM; nếu còn rollout và mở tiếp theo feedback thì cộng `1`.
Đây là **số request**, không phải chi phí tiền hay thời gian: số token, độ dài
trace, số public tests, timeout và tốc độ provider cũng quan trọng.
`search_summary.json` ghi request count/token usage provider trả về, không
ghi secret.

## Code, artifact và kiểm tra offline

| Thành phần | Source |
| --- | --- |
| State, candidate, Backpropagation, Rethink tại node | [tree.py](tree.py) |
| P-UCB | [policies.py](policies.py) |
| LangGraph routing, Pydantic workflow state | [workflow.py](workflow.py) |
| Expansion/Evaluation/search loop | [search.py](search.py) |
| Reward | [reward.py](reward.py) |
| Public/private policy, LLM adapter, artifact | [runner.py](runner.py) |
| Prompt/parser | [prompts.py](prompts.py), [parsing.py](parsing.py) |
| Runtime trace | [feedback/trace.py](feedback/trace.py) |
| Batch cohort/resume | [batch.py](batch.py) |
| Bảng benchmark và provenance | [benchmark.py](benchmark.py) |

Một problem tạo artifact tại
`outputs/rethinkmcts/<run>/<model>/<dataset>/<problem_id>/`: `tree.json`,
`events.jsonl`, `search_summary.json`, `final_solution.py` và
`candidates/<candidate_id>/` (thought snapshot, response, code, execution,
feedback, metadata). Namespace này tách hẳn `outputs/baselines/`.

Kiểm thử offline, **không gọi provider**:

```powershell
.\venv\Scripts\python.exe -m unittest tests.test_rethinkmcts -v
```

Xem plan một bài, **không gọi provider**:

```powershell
.\venv\Scripts\python.exe -m rethinkmcts `
  --dataset humaneval `
  --problem-id 0 `
  --run-name rethinkmcts_v1 `
  --model qwen2.5-coder:7b-instruct `
  --rollouts 2 `
  --width 3 `
  --plan
```

Hướng dẫn smoke thật nằm trong
[docs/runbooks/rethinkmcts-smoke.md](../docs/runbooks/rethinkmcts-smoke.md).
