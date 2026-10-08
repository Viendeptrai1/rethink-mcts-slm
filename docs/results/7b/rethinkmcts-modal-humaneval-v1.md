# RethinkMCTS trên HumanEval 164 - Modal L4

Trạng thái: **HumanEval hoàn tất; benchmark APPS + HumanEval chưa hoàn tất**.
Kiểm tra artifact ngày 2026-10-04. Đây là kết quả native RethinkMCTS, không phải
direct-generation baseline hay bảng benchmark tổng hợp đã đóng băng.

## Kết quả

| Metric | Giá trị |
|---|---:|
| ID trong manifest / artifact hoàn chỉnh | 164 / 164 |
| Pass official HumanEval harness | 150 |
| Fail official harness | 14 |
| Pass@1 (%) | 91.46 |
| Pass Rate (%) | N/A |
| Wrong answer / runtime error / timeout | 11 / 3 / 0 |
| Candidate đã chấm trong search | 398 |
| Số lần Rethink | 70 |
| Request LLM | 1,207 |
| Prompt / completion / tổng token | 716,330 / 92,706 / 809,036 |

Pass@1 = `150 / 164 * 100`; mỗi bài chỉ lấy `final_solution.py` của search
và chấm một lần bằng official harness. `given_tests` chỉ dùng trong search,
không dùng làm kết quả benchmark cuối. Một số bài có `best_reward=1` theo
public tests nhưng vẫn fail official harness, đúng với giới hạn của public tests.

Các ID fail: `HumanEval/10`, `26`, `32`, `38`, `50`, `75`, `91`, `127`, `130`,
`132`, `141`, `145`, `160`, `163`. Trong đó `38`, `50`, `130` là runtime error;
các ID còn lại là wrong answer. Không có timeout official harness.

## Cấu hình và provenance

| Thuộc tính | Giá trị |
|---|---|
| Run | `rethinkmcts_qwen25_modal_v1` |
| Method | Native RethinkMCTS, LangGraph workflow |
| Model | `qwen2.5-coder:7b-instruct` |
| Model digest | `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364` |
| LLM runtime | Private Modal Function, NVIDIA L4 23 GB, Ollama 0.35.1 |
| Judge runtime | Local Windows Python 3.14.5; subprocess, không phải security sandbox |
| Cohort | `data/samples/benchmark_v2/humaneval_test_164.json` |
| Sample ID | `humaneval_full_164_v2` |
| Manifest SHA-256 | `509c7721d598a402d73e8e9e83ea30a7e1bf7796001d37ed399c1f42ea8713fe` |
| Test data SHA-256 | `565825b94c3a726bfcfb1223969ca1817adc81cdc187379f4203bfa521d461d0` |
| Source SHA-256 | `16a14f301ca9c8a5f301fb25d0cff97e831b5fa3f979b8f90602f6515366503a` |
| Modal inference source SHA-256 | `3f26352db0f4d6826f4a86cd977f8160ebca535c0a065064d47da9b082c87adc` |

Search: `rollouts=2`, `width=3`, `seed=0`, `max_rethink_times=2`,
`c_base=10`, `exploration_weight=4`, reward weights `0.8/0.2`,
`temperature=0.2`, `top_p=0.95`, không gửi `max_tokens`, public tests từ
`given_tests`, timeout mỗi test `5s`, timeout mỗi problem `900s`, 1 batch worker.
Seed chỉ điều khiển tie-break cục bộ; output LLM không được khẳng định là tất định.

## Truy vết và giới hạn

- Cấu hình gốc: `outputs/rethinkmcts/rethinkmcts_qwen25_modal_v1/qwen2.5-coder_7b-instruct/run_config.json`.
- Mỗi bài: cùng thư mục, dưới `humaneval/HumanEval_<id>/search_summary.json`,
  `final_solution.py`, `events.jsonl` và `candidates/`.
- Lượt HumanEval/83 đầu tiên fail vì response Expansion không phải JSON hợp lệ;
  attempt được giữ tại `outputs/rethinkmcts_attempts/`. Chạy resume chỉ gọi lại
  bài 83 và hoàn tất. Không sửa candidate của bài đã xong.
- APPS mới hoàn tất bài smoke `2408`; lượt APPS full được dừng theo yêu cầu khi
  `4005` đang chạy. Attempt dở được giữ, không tính là artifact hoàn chỉnh.
- Chưa có `outputs/benchmarks/<run>/<model>/benchmark_table.md`: finalizer yêu
  cầu đủ cả 300 APPS và 164 HumanEval. Không so 91.46% này như một bảng đầy đủ
  với baseline direct 100+100 lịch sử (khác cohort và protocol).

Resume APPS sau này theo [runbook Modal](../runbooks/modal-mcts.md); batch sẽ
skip artifact đã hoàn chỉnh và chạy lại bài dở từ đầu.
