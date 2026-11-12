# Bộ prompt

| Bộ | Được dùng bởi |
|---|---|
| `native_v3` | Protocol v3 (từ 11/2026, [configs/v3_7b](../configs/v3_7b/README.md)). Sửa các lỗi liệt kê dưới đây, bám prompt trong phụ lục bài báo (critic có thought, thang [-1, 1]; block analysis nhận xét từng block). Phần giao diện thực thi dùng chung `_interface.jinja`. Chạy với `prompts.strict_variables: true`: template dùng biến mà code không truyền sẽ báo lỗi. |
| `native_v2` | Mọi run 14B được báo cáo (APPS MCTS/Direct/BO3/tắt rethink/Iterative Repair, HumanEval). Hash từng file nằm trong `prompt_hashes` của manifest. |
| `compact_v1` | Các run pilot/tuning cũ (`runs/pilot_*`, `runs/tuning_*`), các config smoke/mock và config cũ. Không dùng cho kết quả chính. |

Không xóa hay sửa file trong `native_v2`: mọi manifest đều ghi hash của **tất cả** các file `*.jinja` trong bộ này. Kể cả các file `graph_*.jinja` (chỉ `GraphSolver` dùng), sửa bất kỳ file nào cũng làm manifest của các run cũ không còn khớp.

File nào phục vụ vai trò nào (`src/rethink_mcts/adapters/llm/semantic.py`):

| File | Vai trò | Biến code truyền vào |
|---|---|---|
| `expand.jinja` | expansion | `statement`, `active_thoughts`, `width`, `feedback_text` |
| `generate_code.jinja` | code | `statement`, `active_thoughts`, `mode`, `entry_point`, `public_examples` |
| `rethink.jinja` | rethink | `statement`, `parent_thoughts`, `erroneous_thought`, `candidate_code`, `feedback_text` |
| `self_eval.jinja` | critic | `statement`, `candidate_code`, `score_min`, `score_max` |
| `analyze_block.jinja` | block_analysis | `statement`, `candidate_code`, `facts_text`, `trace_text` |
| `repair_code.jinja` | Iterative Repair | `statement`, `candidate_code`, `feedback_text`, `entry_point` |
| `graph_*.jinja` | GraphSolver (thăm dò, không có trong báo cáo) | — |

## Template và code không khớp trong `native_v2` (đã xác minh trên requests.json ngày 11/11/2026; đã sửa trong `native_v3`)

Jinja thay mọi biến không được truyền vào bằng chuỗi rỗng, không báo lỗi. Hệ quả trong `native_v2`:

1. `rethink.jinja` không hiển thị `erroneous_thought`, tức suy nghĩ đang được sửa. Mục "Thoughts" chỉ có các suy nghĩ của nút cha, nên với nút ở độ sâu 1 nó là "(none)". Template cũng không nhận `mode`/`entry_point`, nên thiếu dòng mô tả giao diện thực thi.
2. `analyze_block.jinja` dùng `failed_test` nhưng code truyền `facts_text`, nên mục "Failed public test" luôn rỗng. Template yêu cầu JSON `{block, correct, explanation}`, còn parser tìm khóa `assessments`/`blocks`/`analysis`. Kết quả: **0/1.203 lần phân tích khối trong run MCTS được parse thành nhận định** (tương tự ở mọi run khác). Feedback gửi đi thực chất chỉ gồm thông tin thực thi và trace.
3. `expand.jinja` và `self_eval.jinja` không nhận `mode`/`entry_point`/`active_thoughts`. `self_eval.jinja` luôn yêu cầu điểm trong [-1, 1], kể cả khi config đặt critic là [0, 1].
