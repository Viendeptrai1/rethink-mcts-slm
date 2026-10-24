# APPS 0395: pilot prompt native_v2

Trạng thái: một bài smoke thật, không phải benchmark cohort. Chạy ngày
2026-10-04 bằng `qwen2.5-coder:7b-instruct` trên Modal L40S. Trước khi chạy,
`model_info` trả digest
`dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`.

## Cấu hình

- Run mới: `rethinkmcts_apps_0395_prompt_v2_smoke`.
- APPS test ID `0395`; stdin/stdout, 53 tests (26 public theo `half`, 27
  còn lại). Final evaluation chấm đủ 53 tests.
- `rollouts=2`, `width=3`, `max_rethink_times=2`, `seed=0`, temperature
  `0.2`, top_p `0.95`, timeout `5` giây mỗi test. Khớp search config của
  run APPS L40S lịch sử cho bài này.
- Prompt version trong events: `native_v2`; 9 LLM requests và 13.579 tokens.

## Kết quả

| Run | Best candidate | Public tests | Final tests | Reward |
|---|---|---:|---:|---:|
| APPS L40S lịch sử (`native_v1`) | `candidate_0001` | 0/26 | 0/53 | 0 |
| Pilot `native_v2` | `candidate_0002` | 26/26 | 53/53 | 1 |

Run lịch sử chấm private 0/27; full rejudge trước đó chấm toàn bộ 0/53.
Pilot mới có 3 candidates. Candidate đầu in `NO` nhưng sai thuật toán,
pass 12/26 public tests; sau Rethink, candidate thứ hai có stdin/stdout
driver và kiểm tra các tổ hợp ba người, pass 26/26 public và 53/53 final.
Candidate cuối nằm tại
`outputs/rethinkmcts/rethinkmcts_apps_0395_prompt_v2_smoke/qwen2.5-coder_7b-instruct/apps/0395/final_solution.py`.

## Phát hiện thêm

Feedback LLM của candidate đầu lại khẳng định code "không có print",
trong khi source có `print(...)` và executor thu được `NO`. Đây là nhận
định sai của LLM. Sau pilot đã thêm guard trong `rethinkmcts/search.py`:
nếu stdout thực tế không rỗng mà feedback gán lỗi `interface`, thay bằng
chẩn đoán `output_mismatch` và giữ raw response ở `discarded_analysis`.
Guard này đã qua test offline nhưng **chưa được dùng trong pilot đã chạy**;
pilot không được dùng làm bằng chứng về hiệu quả của guard.

Một bài từ 0/53 lên 53/53 xác nhận interface fix hoạt động ở ví dụ này.
Không suy rộng thành cải thiện Pass Rate/Pass@1 cho cohort 300 bài trước
khi chạy một run MCTS mới trên toàn bộ cohort với cùng protocol.
