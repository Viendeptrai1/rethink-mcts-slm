# RethinkMCTS - lý thuyết từ paper 2409.09584v2

Nguồn chính: `RelativeWork/2409.09584v2.pdf` - **RethinkMCTS: Refining Erroneous
Thoughts in Monte Carlo Tree Search for Code Generation**.

Trạng thái nguồn: đã đọc lại trực tiếp từ PDF 19 trang ngày 2026-09-26. Những điểm
chưa được paper định nghĩa rõ được giữ ở mục "Cần xác minh khi đọc/chạy repo gốc".

Phạm vi file này:
- Đúc kết lại thuật toán từ paper, phục vụ mục tiêu **implement lại RethinkMCTS**.
- Giữ đúng giai đoạn hiện tại của dự án: hiểu paper/chạy lại bản gốc trước, chưa thêm reward
  TLE-aware hay root-cause identification riêng.
- Các điểm paper chưa nói rõ được ghi ở mục "Cần xác minh khi đọc repo gốc", không mặc định
  là sự thật implementation.

---

## 1. Một câu tóm tắt

RethinkMCTS là một framework dùng **Monte Carlo Tree Search trên không gian thought** thay vì
trên token/code; tại mỗi node, LLM sinh code hoàn chỉnh từ chuỗi thought hiện có, chạy public
tests để lấy scalar reward và block-level verbal feedback, rồi dùng cơ chế **Rethink** để sửa
thought sai ngay trong cây.

Ý tưởng cốt lõi:

```text
Không search trực tiếp code
-> search reasoning/thought trước
-> sinh code từ thought
-> chạy test thật
-> dùng feedback để sửa thought
-> tiếp tục search trên cây đã được cải thiện
```

---

## 2. Động lực và gap paper giải quyết

### Gap 1 - Search sai tầng

Các phương pháp trước đó như PG-TD, LATS, ToT khi áp dụng cho code thường search ở
token-level, line-level hoặc code-level. Paper lập luận rằng code generation là task đòi hỏi
reasoning, trong khi LLM thường mạnh hơn ở **semantic reasoning** so với **symbolic reasoning**.
Vì vậy, search trực tiếp trên code/token bỏ qua phần quyết định: quá trình nghĩ ra thuật toán.

Giải pháp của RethinkMCTS: search ở **thought-level**. Mỗi action trong MCTS là một thought mới.

### Gap 2 - Reflection chỉ ghi nhớ lỗi, không sửa đường đi

Reflection-based methods lưu lỗi cũ vào memory/prompt nhưng vẫn giữ node sai trong cây. Hậu quả:
- Cây vẫn chứa reasoning path sai.
- Search sau vẫn có thể đi tiếp từ một nền tảng sai.
- Prompt ngày càng dài vì tích lũy lịch sử lỗi.

RethinkMCTS thay reflection bằng **rethink**: sửa trực tiếp thought đang sai tại node hiện tại.
Sau khi thought được sửa, các nhánh con sinh ra về sau sẽ dựa trên reasoning tốt hơn.

### Gap 3 - Reward public test quá thô

Nếu chỉ dùng pass rate public test, nhiều chương trình cùng pass 100% public tests sẽ có reward
bằng nhau, dù hidden tests có thể phân biệt chúng. Vì vậy paper dùng **Dual Evaluation**:
chỉ khi code pass toàn bộ public tests mới gọi LLM self-evaluation để phân biệt chất lượng.

### Gap 4 - Scalar reward không đủ để sửa lỗi

Một số như `v_test = 0.4` chỉ cho biết code sai, nhưng không nói block nào sai hoặc biến nào
có giá trị bất thường. RethinkMCTS bổ sung **verbal feedback** từ block-level code analysis.

---

## 3. Problem Formulation

Paper theo setup của PG-TD:

```text
Input:  problem statement P + public test cases T_pub
Output: code C ~ M(P, T_pub)
Eval:   chạy C trên private test cases T_priv
Metric: pass private tests
```

Trong quá trình search, model được dùng public tests để tối ưu. Private tests chỉ dùng để báo
kết quả cuối.

---

## 4. State, Action, Transition

State là đề bài cộng chuỗi thought đã tích lũy:

```text
s_t = (P, z_1, z_2, ..., z_t)
```

Action là thought kế tiếp:

```text
a_t = z_{t+1}
```

Transition là phép nối xác định:

```text
s_{t+1} = CONCAT(s_t, a_t)
```

Điểm quan trọng: RethinkMCTS **không dùng world model** kiểu RAP để tưởng tượng state mới.
State mới chỉ là nối thêm thought, còn chất lượng state được kiểm bằng code execution thật ở
bước Evaluation.

---

## 5. Luồng MCTS Trong RethinkMCTS

Paper mô tả các bước:

1. Selection
2. Expansion
3. Evaluation
4. Verbal Feedback
5. Backpropagation
6. Rethink

Thực chất Evaluation + Verbal Feedback cùng đến từ việc generate code rồi chạy public tests.

---

## 6. Selection

Mục tiêu Selection là cân bằng exploitation và exploration. RethinkMCTS dùng P-UCB:

```text
P-UCB(s,a) = Q(s,a) + beta(s) * p(a|s) * sqrt(log(N(s))) / (1 + N(s'))

beta(s) = log((N(s) + c_base + 1) / c_base) + c
```

Ký hiệu:

| Ký hiệu | Ý nghĩa |
|---|---|
| `Q(s,a)` | reward lớn nhất từng đạt khi đi từ state `s` qua action `a` |
| `N(s)` | số lần state/node cha `s` được visit |
| `N(s')` | số lần state/node con `s'` được visit |
| `p(a|s)` | probability/reasonableness score do LLM gán cho thought `a` khi Expansion |
| `c_base` | hyperparameter, paper dùng `10` |
| `c` | exploration weight, paper dùng `4` |

Vì sao `Q` là max thay vì average:
- Một rollout tệ không phủ nhận toàn bộ tiềm năng của nhánh.
- Code generation có ngẫu nhiên; cùng hướng reasoning có thể sinh code tốt/xấu tùy lần.
- Max giữ lại bằng chứng tốt nhất rằng hướng này có khả năng đúng.

Vì sao có `p(a|s)`:
- Action space là thought tự nhiên, rất rộng.
- LLM đã tự ước lượng thought nào hợp lý hơn qua reasonableness score.
- P-UCB dùng score này như prior để ưu tiên exploration những thought có vẻ hứa hẹn hơn.

Lưu ý implement:
- Khi `N(s') = 0`, `Q` của các child chưa evaluate thường bằng nhau, nên `p(a|s)` là tín hiệu
  quan trọng để xếp thứ tự thử.
- Khi `N(s) = 1`, `log(N(s)) = 0`, exploration term có thể bị triệt tiêu. Cần kiểm tra code
  gốc xử lý tie-break thế nào.

---

## 7. Expansion

Action space là tập các possible thoughts/strategies để viết code. Vì action space mở, paper
không duyệt hết mà sample `k` thought, với `k = 3`.

Có 2 kịch bản prompt:

### 7.1 Node hiện tại có failed public tests

Nếu node có verbal feedback `f`, LLM sinh thought mới có điều kiện trên state và feedback:

```text
[(z_1,e_1), ..., (z_k,e_k)] ~ p((z,e)^(1..k) | s, f)
```

Trong đó:
- `z_i` là thought.
- `e_i` là reasonableness score, chính là `p(a|s)` dùng trong P-UCB.

Prompt dạng này gồm problem, previous thoughts, generated code và verbal feedback.
Mục tiêu là thought mới không chỉ tránh lỗi hiện tại mà còn xử lý được các test tiềm ẩn chưa
gặp.

### 7.2 Node hiện tại pass public tests

Nếu không có feedback lỗi, LLM sinh thought chỉ dựa trên state:

```text
[(z_1,e_1), ..., (z_k,e_k)] ~ p((z,e)^(1..k) | s)
```

Prompt yêu cầu thought tiếp theo là detailed thinking/enhancement cho các thought trước đó.

### 7.3 Format output của Expansion

Appendix Table 8/9 yêu cầu output là list JSON-like:

```json
[
  {"Thought-1": "...", "Reasonableness": 0.7},
  {"Thought-2": "...", "Reasonableness": 0.29},
  {"Thought-3": "...", "Reasonableness": 0.01}
]
```

Ràng buộc quan trọng:
- Mỗi thought là một reasoning riêng.
- Không được viết code ở bước này.
- Reasonableness nằm trong `[0,1]` và tổng bằng `1`.

---

## 8. Evaluation

RethinkMCTS không dùng Simulation kiểu MCTS cổ điển. Thay vào đó, với chuỗi thought tại node
hiện tại, LLM sinh **complete code** rồi executor chạy public tests.

| MCTS/RAP/LATS kiểu simulation | RethinkMCTS |
|---|---|
| Đi tiếp từ intermediate state tới terminal state để ước lượng | Sinh code hoàn chỉnh trực tiếp từ thoughts hiện tại |
| Thường cần world model hoặc rollout tưởng tượng | Dùng executor chạy code thật |
| Terminal state rõ ràng | Không cần terminal state riêng |

Prompt code generation (Table 10) yêu cầu:
- Sinh complete Python program.
- Có đủ imports/function header.
- Chỉ trả code, không giải thích.
- Dựa vào previous thoughts để viết code.

---

## 9. Dual Evaluation

Reward được tính:

```text
reward = v_test                         nếu 0 <= v_test < 1
       = a * v_test + b * v_llm         nếu v_test = 1
```

Trong đó:
- `v_test`: pass rate trên public tests.
- `v_llm`: LLM self-evaluation score, chỉ dùng khi `v_test = 1`.
- Paper dùng `(a,b) = (0.8, 0.2)`.

Ý nghĩa của 2 nhánh:
- Nếu `v_test < 1`, executor đã có bằng chứng khách quan code sai, không cần LLM chấm thêm.
- Nếu `v_test = 1`, public tests đã cạn khả năng phân biệt, nên dùng LLM đọc code để dự đoán
  khả năng pass hidden/corner cases.

Appendix Table 11 yêu cầu `v_llm` trong `[-1,1]`. Với `(a,b)=(0.8,0.2)`, code pass public tests
có reward trong `[0.6,1.0]`, vẫn nằm trong `[0,1]`.

Paper so sánh reward weights (Table 3):

| `(a,b)` | APPS Intro Pass@1 | APPS Inter Pass@1 | APPS Comp Pass@1 | HumanEval |
|---|---:|---:|---:|---:|
| `(0.8, 0.2)` | 59 | 49 | 28 | 94.5 |
| `(1.0, 0.2)` | 60 | 53 | 27 | 92.7 |
| `(1.0, 1.0)` | 60 | 54 | 24 | 91.5 |

Paper chọn `(0.8,0.2)` vì các cấu hình có `a=1.0` làm code pass public tests luôn nhận điểm
trên `1.0`, dễ loại sớm các reasoning path còn chưa hoàn hảo public pass rate nhưng có tiềm năng.

---

## 10. Verbal Feedback Bằng Block-Level Analysis

Scalar reward dùng để chọn nhánh, nhưng không đủ để sửa lỗi. Vì vậy RethinkMCTS dùng verbal
feedback từ block-level analysis, kế thừa ý tưởng từ LDB.

Quy trình:

1. Chia code thành basic blocks.
2. Xây control-flow graph (CFG).
3. Chạy một failed public test qua CFG để lấy execution trace `[B1, B2, ..., Bn]`.
4. Ghi lại giá trị biến trước/sau mỗi block.
5. Đưa trace + biến cho LLM, yêu cầu phân tích block nào đúng/sai và vì sao.

Basic block là một đoạn code tuyến tính có một entry point và một exit point.

Verbal feedback được lưu tại **current node** và dùng ở 2 nơi:

| Nơi dùng | Vai trò |
|---|---|
| Expansion | Gợi ý thought con tiếp theo tránh lỗi đã gặp |
| Rethink | Sửa trực tiếp thought hiện tại |

Không nên backprop verbal feedback lên ancestor như scalar reward, vì feedback mô tả lỗi cụ thể
của một code/thought trace cụ thể.

---

## 11. Backpropagation

Sau Evaluation, scalar reward `r` được dùng để update các node trên path từ current node về root.
Paper mô tả `Q(s,a)` là maximum reward đã đạt được qua action đó.

Tư duy implement đơn giản:

```text
for every edge/state-action pair on selected path:
    Q(s,a) = max(Q(s,a), r)
    update visit counts
```

Verbal feedback không lan truyền ngược. Nó chỉ nằm ở node hiện tại để dùng cho Expansion/Rethink
sau này.

---

## 12. Rethink

Khi generated code không pass public tests (`v_test != 1`), paper dùng verbal feedback để sửa
thought hiện tại:

```text
z_new ~ p(z | s, f, z_old)
```

Ý nghĩa:
- `s`: context/problem + previous thoughts.
- `f`: verbal feedback từ failed execution.
- `z_old`: thought hiện tại bị coi là sai.
- `z_new`: thought mới thay thế `z_old`.

Rethink là **in-place refinement**:
- Không tạo một nhánh reflection mới.
- Không chỉ append lỗi vào memory.
- Ghi đè thought sai để các search path sau đi từ reasoning đã được sửa.

Prompt Rethink (Table 12) yêu cầu:
- Cung cấp new Thought để replace previous thought.
- Thought mới phải tránh lỗi.
- Chỉ trả thought 1-2 câu, không viết code.

### Vì sao không regenerate parent nodes?

Paper đưa 2 lý do:

1. Parent nodes đã tích lũy reward qua nhiều child/evaluation. Nếu sửa parent, các reward cũ
   không còn tương ứng với nội dung node mới.
2. Parent node đã có cơ hội trải qua rethink của chính nó. Nếu nó fail public tests, nó đã được
   refine; nếu không fail, nó được xem là hợp lệ tại thời điểm đó.

### Lợi ích của Rethink

Từ góc nhìn code generation:
- Thought tốt hơn dẫn tới code tốt hơn.

Từ góc nhìn MCTS:
- Sửa current action/node làm tăng chất lượng các path sinh ra sau đó.
- Cây được xây incremental, nên sửa sớm ở node hiện tại có tác động xuôi tới các child tương lai.

---

## 13. Algorithm 1 Theo Paper

Pseudocode rút gọn:

```text
program_dict = {}
f = EMPTY

for i in 1..max_rollouts:
    node = root

    # Selection
    while node.children is not empty:
        node = P_UCB_SELECT(node.children, c)

    # Expansion
    next_thoughts = TOP_K(node, k)
    for next_thought in next_thoughts:
        next_state = CONCAT(node, next_thought)
        create child node for next_state

    # Evaluation
    C = GENERATE(node)
    v_test, f = GET_PASS_RATE(C)
    if v_test == 1:
        v_llm = GET_LLM_EVAL(C)
        r = a * v_test + b * v_llm
    else:
        r = v_test
    program_dict[C] = r

    # Backpropagation
    update node and ancestors with r

    # Rethink
    if v_test != 1:
        node.thought = RETHINK(node, f)
        next_thoughts = RETHINK_NEXT(node, k, f)
        C2 = RE-GENERATE(node)
        r2 = RE-EVALUATION(C2)
        program_dict[C2] = r2

return code in program_dict with highest reward
```

### Điểm nhập nhằng/cần cẩn thận trong Algorithm 1

Paper pseudocode có vài điểm cần kiểm tra khi implement:

- Dòng Evaluation trong Algorithm 1 ghi `C = GENERATE(node)` sau khi đã tạo các child, nhưng
  không chỉ rõ evaluate selected leaf hay một child mới được expand. Cần đối chiếu repo gốc để
  tránh implement sai.
- Algorithm 1 gọi `GET_LLM_EVAL` trước nhánh `if v_test = 1`, nhưng phần mô tả Evaluation nói
  LLM self-evaluation chỉ dùng khi pass toàn bộ public tests. Khi implement nên theo mô tả công
  thức reward: chỉ gọi LLM eval nếu `v_test == 1`.
- Dòng `next_thoughts = RETHINK_NEXT(node,k,f)` sau rethink xuất hiện trong pseudocode nhưng
  không được giải thích kỹ trong phần method. Cần kiểm tra repo gốc xem nó tạo child mới, refresh
  children hay chỉ là phần thừa của pseudo-code.

---

## 14. Experiment Settings Trong Paper

### Datasets

| Dataset | Cách dùng trong paper |
|---|---|
| APPS | 100 bài đầu tiên mỗi difficulty: introductory, interview, competition |
| HumanEval | Toàn bộ benchmark |

Paper nói APPS có public test trung bình khoảng 27.52 test/bài, HumanEval khoảng 2.8 test/bài.
Điều này giải thích vì sao self-evaluation và block-level feedback quan trọng hơn trên HumanEval.

### Baselines

Feedback-enhanced:
- LDB
- Reflexion

Tree-search-enhanced:
- PG-TD
- ToT
- LATS
- RAP

### Hyperparameters chính

| Tham số | Giá trị |
|---|---|
| Backbone | GPT-3.5-turbo, GPT-4o-mini |
| max children per node `k` | 3 |
| `c_base` | 10 |
| `c` | 4 |
| `(a,b)` | (0.8, 0.2) |
| max rollouts/simulations | 16 |
| LDB max debug times | 10 |

---

## 15. Kết Quả Chính

Table 1 với GPT-4o-mini:

| Method | APPS Intro Pass@1 | APPS Inter Pass@1 | APPS Comp Pass@1 | HumanEval |
|---|---:|---:|---:|---:|
| Base(1) | 35 | 29 | 16 | 87.20 |
| Base(16) | 47 | 41 | 21 | 93.29 |
| PG-TD | 47 | 43 | 23 | 91.46 |
| ToT | 52 | 46 | 23 | 92.68 |
| LATS | 50 | 45 | 19 | 93.29 |
| RAP | 39 | 32 | 20 | 87.20 |
| LDB | 40 | 38 | 23 | 90.85 |
| Reflexion | 40 | 31 | 18 | 90.85 |
| **RethinkMCTS** | **59** | **49** | **28** | **94.51** |

Quan sát:
- RethinkMCTS tốt nhất trên toàn bộ datasets được báo cáo.
- RAP kém trong code generation, ủng hộ nhận định world model tưởng tượng không phù hợp bằng
  execution feedback thật trong domain code.
- Lợi ích trên GPT-3.5-turbo lớn hơn GPT-4o-mini, có thể vì model yếu hơn hưởng lợi nhiều hơn
  từ cơ chế sửa reasoning.

---

## 16. Ablation Và Phân Tích

### 16.1 Ablation

Paper loại từng thành phần:

| Variant | Ý nghĩa |
|---|---|
| w/o selfEval | bỏ LLM self-evaluation |
| VF w/o blockInfo | verbal feedback nhưng không có block-level variable trace |
| w/o VF | bỏ verbal feedback |
| w/o rethink | bỏ rethink |

Kết luận:
- Mỗi thành phần đều đóng góp.
- Verbal feedback và rethink là hai thành phần quan trọng nhất.
- Trên HumanEval, block-level analysis có tác động mạnh hơn vì public tests quá ít.

Figure 6 với GPT-4o-mini:
- HumanEval full model 94.5; w/o VF 91.5; w/o rethink 92.7.
- APPS Intro full model 59; w/o VF 53; w/o rethink 52.

### 16.2 Search granularity

Paper so sánh token-level, line-level, code-level, thought-level và RethinkMCTS.

Kết luận:
- Thought-level search tốt hơn các mức còn lại, đặc biệt trên APPS competition.
- Token-level có thể tốt hơn line/code-level trong một số setting vì ít ràng buộc hơn ở bước
  đầu, nhưng vẫn kém thought-level.
- Rethink + feedback làm thought-level search hiệu quả hơn nữa.

### 16.3 Rethink vs Reflection

Table 2:

| Dataset | Reflection Pass@1 | Rethink Pass@1 | Reflection Avg Token | Rethink Avg Token |
|---|---:|---:|---:|---:|
| APPS Intro | 54 | 59 | 177353 | 143048 |
| APPS Inter | 45 | 49 | 163494 | 126648 |
| APPS Comp | 24 | 28 | 189215 | 182193 |
| HumanEval | 93.29 | 94.51 | 57027 | 36678 |

Rethink vừa tăng pass@1 vừa giảm token cost so với reflection.

### 16.4 Test-time scaling

Figure 5 so sánh tăng số lần rethink với tăng rollout nhưng không rethink. Kết luận: tăng rethink
hiệu quả hơn tăng rollout thuần.

Table 4 đo success rate của các searched codes:

| Method | APPS Intro | HumanEval |
|---|---:|---:|
| W/O Rethink | 10.04 | 48.30 |
| RethinkMCTS | 15.60 | 53.29 |

### 16.5 Self-evaluation vs self-generated tests

Table 6:

| Method | APPS Intro Pass@1 | APPS Inter Pass@1 | APPS Comp Pass@1 | HumanEval |
|---|---:|---:|---:|---:|
| Direct self-evaluation | 59 | 49 | 28 | 94.51 |
| Self-generated tests | 59 | 44 | 28 | 93.29 |

Paper giải thích self-generated tests có thể tăng pass rate trên một số test tự sinh nhưng không
cải thiện pass@1, vì tests do LLM sinh có thể lệch hoặc sai, làm search đi sai hướng.

### 16.6 Token cost

Table 5 với GPT-4o-mini, average tokens/question:

| Method | APPS Intro Input | APPS Intro Output | APPS Cost | HumanEval Input | HumanEval Output | HumanEval Cost |
|---|---:|---:|---:|---:|---:|---:|
| ToT | 24799 | 7156 | 0.008 | 11687 | 7131 | 0.006 |
| LATS | 104634 | 17472 | 0.026 | 12690 | 7403 | 0.006 |
| PG-TD | 27827 | 5378 | 0.007 | 5959 | 3759 | 0.003 |
| LDB | 61112 | 1734 | 0.010 | 13161 | 480 | 0.002 |
| RethinkMCTS | 123207 | 17863 | 0.029 | 28479 | 8198 | 0.009 |

RethinkMCTS tốn token nhất, chủ yếu do block-level analysis chứa giá trị biến trước/sau mỗi block.

---

## 17. Limitations Paper Tự Nêu

1. **Chưa khai thác fine-tuning**  
   Framework tạo dữ liệu gồm thought steps, execution feedback và code; có thể dùng fine-tune LLM
   trong tương lai, nhưng paper chỉ tập trung inference.

2. **Khó generalize sang domain thiếu feedback chi tiết**  
   Code có executor/compiler feedback; math reasoning không luôn có feedback chi tiết tương đương.

3. **Refinement step chưa tinh vi**  
   Paper trực tiếp chọn **most recent step** để refine, chưa có cơ chế xác định thought nào thật sự
   là nguyên nhân gốc. Paper gợi ý dedicated verifier để chọn thought cần refine có thể tốt hơn.

Điểm 3 là gap rất liên quan tới đề tài hiện tại: trong competitive programming, lỗi TLE/complexity
có thể bắt nguồn từ thought rất sớm về thuật toán hoặc cấu trúc dữ liệu, không phải thought cuối.

---

## 18. Checklist Implement Lại Từ Paper

### Data structures

- [ ] Node/state lưu problem + accumulated thoughts.
- [ ] Action là một thought mới.
- [ ] Mỗi edge/action cần lưu `p(a|s)`/Reasonableness.
- [ ] Visit count cho state/node.
- [ ] `Q(s,a)` theo max reward.
- [ ] Mỗi node có thể lưu verbal feedback riêng.
- [ ] `program_dict` lưu mọi code đã generate và reward tương ứng.

### Selection

- [ ] Implement P-UCB đúng công thức.
- [ ] Dùng `c_base=10`, `c=4` làm default.
- [ ] Xử lý tie-breaking rõ ràng.
- [ ] Kiểm tra trường hợp `log(N(s)) = 0`.

### Expansion

- [ ] `k=3` default.
- [ ] Prompt không feedback khi node không có failed feedback.
- [ ] Prompt có feedback khi node có verbal feedback.
- [ ] Parse JSON/list dict robustly.
- [ ] Kiểm tra tổng Reasonableness; normalize nếu cần.
- [ ] Cấm code trong thought prompt.

### Evaluation

- [ ] Generate complete code từ accumulated thoughts.
- [ ] Chạy public tests.
- [ ] Tính `v_test`.
- [ ] Chỉ gọi LLM self-eval khi `v_test == 1`.
- [ ] Reward theo công thức Dual Evaluation.

### Verbal feedback

- [ ] Khi code fail public test, lấy failed case.
- [ ] Tạo CFG/basic blocks.
- [ ] Trace execution qua blocks.
- [ ] Thu giá trị biến trước/sau block.
- [ ] Prompt LLM phân tích block đúng/sai.
- [ ] Lưu feedback ở current node.

### Backpropagation

- [ ] Update reward/visit counts về root.
- [ ] Scalar reward lan ngược.
- [ ] Verbal feedback không lan ngược.

### Rethink

- [ ] Chỉ kích hoạt khi `v_test != 1`.
- [ ] Prompt dùng problem + thoughts + code + verbal feedback.
- [ ] Output chỉ là thought mới, không code.
- [ ] Replace thought hiện tại in-place.
- [ ] Re-generate/re-evaluate sau rethink theo Algorithm 1.
- [ ] Lưu code mới vào `program_dict`, không xóa code cũ.

### Final selection

- [ ] Trả code có reward cao nhất trong `program_dict`.
- [ ] Không chọn theo most visited path kiểu RAP.

---

## 19. Cần Xác Minh Khi Đọc/Chạy Repo Gốc

Các điểm paper chưa đủ rõ, cần đối chiếu code gốc trước khi implement lại:

1. **Evaluation sau Expansion đang evaluate node nào?**  
   Algorithm 1 tạo child rồi `GENERATE(node)`, không nói rõ chọn child nào để evaluate.

2. **`RETHINK_NEXT(node,k,f)` thật sự làm gì?**  
   Pseudocode gọi hàm này sau khi replace thought nhưng không giải thích tác động lên cây.

3. **Visit count khởi tạo thế nào?**  
   P-UCB có `log(N(s))`, nên cách khởi tạo `N(s)` ảnh hưởng trực tiếp tới rollout đầu.

4. **Q-value lưu trực tiếp max hay lưu list returns rồi lấy max?**  
   Paper mô tả `Q` là maximum reward, nhưng implementation có thể tổ chức dữ liệu khác.

5. **Rethink có giới hạn số lần trên mỗi node không?**  
   Paper không nêu giới hạn ngoài `max_rollouts`.

6. **Verbal feedback có bị cắt token/số failed tests không?**  
   Paper nói dùng block-level analysis nhưng không nêu policy cắt ngắn.

7. **APPS public/private split trong code gốc cụ thể ra sao?**  
   Tài liệu dataset của dự án ghi APPS không có public/private sẵn và repo tự chia; cần kiểm tra đúng hàm.

---

## 20. Liên Hệ Với Hướng Đề Tài

RethinkMCTS gốc là baseline nền:
- Thought-level MCTS.
- Binary/pass-rate-centric reward.
- Rethink sửa thought gần nhất.
- Feedback dựa trên output correctness/block-level runtime trace.

Hai hướng phát triển sau này của đề tài không nên làm ngay ở giai đoạn hiện tại, nhưng paper đã
chỉ ra khoảng trống:

1. **Reward 3 trạng thái Accepted / Wrong Answer / TLE-MLE**  
   Paper chưa phân biệt lỗi độ phức tạp/thời gian chạy. Public test nhỏ có thể không lộ TLE.

2. **Root-cause identification khi Rethink**  
   Paper tự thừa nhận chưa có verifier chọn thought cần refine; hiện chọn most recent step. Với
   competitive programming, root cause có thể nằm ở thought đầu về thuật toán.

Trong giai đoạn hiện tại, việc cần làm trước là chạy được RethinkMCTS gốc trên APPS/HumanEval
với rollout nhỏ, quan sát log cây/thought/code/rethink rồi mới quyết định implement biến thể riêng.
