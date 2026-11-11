# Chương 4. Kết quả Thực nghiệm

Chương này trình bày kết quả của nhánh 14B (`Qwen/Qwen2.5-Coder-14B-Instruct`, phục vụ bằng vLLM trên Modal) trên APPS-300 và HumanEval-164. Kết quả nhánh 7B được đặt cạnh để tham khảo. Mọi con số đều trích từ artifact trong `runs/` (đường dẫn ghi ở từng bảng) hoặc từ báo cáo gốc của nhánh 7B trong [`docs/results/7b/`](../results/7b/).

Hai quy ước dùng xuyên suốt chương:

- **Pass@1** là tỷ lệ bài mà chương trình được chọn (`selected.py`) vượt qua mọi test trong tập chấm. Mẫu số là toàn bộ cohort; bài lỗi hoặc không có ứng viên được tính là không đạt.
- **Mean Pass Rate** là trung bình theo bài (macro average) của tỷ lệ test vượt qua.

Mỗi cấu hình chỉ chạy **một seed**. Các khoảng tin cậy dưới đây phản ánh biến thiên do mẫu bài toán, không phản ánh biến thiên do lấy mẫu của mô hình.

---

## 4.1. Nguồn số liệu và mức độ tin cậy

Không phải mọi run trong `runs/` đều có cùng mức kiểm chứng. Bảng 4.1 phân loại các run được dùng trong chương.

### Bảng 4.1. Phân loại các run thực nghiệm

| Run | Dữ liệu | Phương pháp | Manifest (schema 2) | Vai trò trong chương |
| :--- | :--- | :--- | :-: | :--- |
| [`benchmark_apps_14b_direct_300`](../../runs/benchmark_apps_14b_direct_300/summary.json) | APPS-300 | Direct | Có | **Kết quả chính** |
| [`benchmark_apps_14b_dual_unified`](../../runs/benchmark_apps_14b_dual_unified/summary.json) | APPS-300 | RethinkMCTS | Có, ở 15 run thành phần (10 batch + 5 lượt chạy lại, cùng cấu hình trừ URL endpoint); thư mục gộp không có manifest riêng | **Kết quả chính** |
| [`benchmark_apps_14b_bon3_300`](../../runs/benchmark_apps_14b_bon3_300/summary.json) | APPS, 160/300 bài | Best-of-3 | Có | Kết quả chính trên tập con 160 bài |
| [`humaneval_mcts_dual_14b`](../../runs/humaneval_mcts_dual_14b/summary.json) | HumanEval-164 | RethinkMCTS | Có | **Kết quả chính** |
| `humaneval_{direct,bon3,mcts}_14b` | HumanEval-164 | Direct / BoN-3 / MCTS | Không | Thăm dò (phiên bản code cũ) |
| `apps_intro_{direct,bon3,mcts}_14b` | 100 bài `apps_4000`–`4099` | Direct / BoN-3 / MCTS | Không | Thăm dò (khác cohort) |
| Báo cáo 7B | APPS-300, HumanEval-164 | Direct / MCTS Dual / Test-only | Codebase riêng | Tham khảo, không ghép cặp được |

Ba run APPS chính dùng cùng mã nguồn solver (`source_hash = 34544f8d08…` trong cả ba manifest), cùng prompt `native_v2`, cùng seed và cùng tập dữ liệu đã chuẩn bị. Vì vậy, so sánh giữa chúng là so sánh nội bộ đồng nhất.

Trong lượt chạy APPS-300 của RethinkMCTS, 80 bài gặp lỗi hạ tầng từ phía endpoint (tổng 81 lần lỗi: 79 `ModelNotFoundError` và 2 `ModelError`). Các bài này được chạy lại với cùng cấu hình và đều hoàn tất. Bản gộp cuối cùng có 300/300 bài hoàn tất, không có lỗi.

### Cấu hình hiệu lực của RethinkMCTS (trích từ manifest)

| Tham số | APPS-300 | HumanEval-164 |
| :--- | :--- | :--- |
| Độ rộng / độ sâu cây | 3 / 4 | 3 / 4 |
| P-UCB ($c_{\text{base}}$, $c$) | 10.0, 4.0 | 10.0, 4.0 |
| Số rethink tối đa mỗi nút | 2 | 2 |
| Phần thưởng $(a, b)$ | $(0.8,\ 0.2)$, critic trong $[-1, 1]$ | $(0.8,\ 0.2)$, critic trong $[0, 1]$ |
| Feedback | `block` (CFG + phân tích khối bằng LLM) | `block` |
| Dừng sớm | `public_all_passed` | `public_all_passed` |
| Ngân sách mỗi bài | 16 lần sinh code, 64 lời gọi, 65.536 token, 900 s | 16 lần sinh code, 64 lời gọi, 65.536 token, 600 s |
| Thực thi | `trusted_fixture`, 5 s/test | `trusted_fixture`, 4 s/test |
| Prompt, seed | `native_v2`, 0 | `native_v2`, 42 |

Trên APPS, public test là **2 test đầu tiên** của mỗi bài. Hidden suite là các test còn lại, sau khi đã loại các test trùng với public.

---

## 4.2. Kết quả chính trên APPS-300

Chúng tôi báo cáo hai cách chấm:

- **Chấm trên hidden** (protocol gốc của nhánh 14B): chỉ dùng các test không xuất hiện trong lúc tìm kiếm.
- **Chấm trên toàn bộ test** (public + hidden): một chương trình chỉ được coi là đúng khi vượt qua mọi test của bài. Đây cũng là cách chấm `all_tests` của nhánh 7B.

Kết quả chấm trên toàn bộ test được ghép từ kết quả public và hidden đã lưu của chương trình được chọn, không thực thi lại code ([`scripts/alltests_rejudge_offline.py`](../../scripts/alltests_rejudge_offline.py), kết quả tại `runs/*/all_tests_offline.json`).

### Bảng 4.2. Pass@1 và Mean Pass Rate của 14B trên APPS-300

| Phân tầng (100 bài) | Cách chấm | Direct Pass@1 | RethinkMCTS Pass@1 | Direct Pass Rate | RethinkMCTS Pass Rate |
| :--- | :--- | :-: | :-: | :-: | :-: |
| Introductory | Hidden | 42.00% | **53.00%** | 53.50% | **71.26%** |
| | Toàn bộ test | 38.00% | **50.00%** | 51.86% | **71.86%** |
| Interview | Hidden | 13.00% | **27.00%** | 31.48% | **50.13%** |
| | Toàn bộ test | 11.00% | **26.00%** | 30.49% | **52.93%** |
| Competition | Hidden | 21.00% | **28.00%** | 30.24% | **39.08%** |
| | Toàn bộ test | 8.00% | **23.00%** | 28.52% | **48.56%** |
| **Toàn bộ (300)** | **Hidden** | 25.33% (76) | **36.00% (108)** | 38.41% | **53.49%** |
| | **Toàn bộ test** | 19.00% (57) | **33.00% (99)** | 36.96% | **57.79%** |

### Bảng 4.3. Kiểm định ghép cặp RethinkMCTS so với Direct (300 bài)

| Cách chấm | Chỉ MCTS đúng | Chỉ Direct đúng | McNemar $\chi^2$ (hiệu chỉnh liên tục) | $p$ (chính xác) | $\Delta$ Pass@1 (bootstrap ghép cặp 95%) |
| :--- | :-: | :-: | :-: | :-: | :-: |
| Hidden | 42 | 10 | 18.48 | $9.1 \times 10^{-6}$ | **+10.67%** [+6.33; +15.33] |
| Toàn bộ test | 45 | 3 | 35.02 | $1.3 \times 10^{-10}$ | **+14.00%** [+10.00; +18.33] |

Bootstrap dùng 10.000 lần lấy mẫu lại theo bài, seed 2027.

**Nhận xét.**

1. RethinkMCTS vượt Direct ở cả ba phân tầng và theo cả hai cách chấm. Khác biệt có ý nghĩa thống kê, và khoảng tin cậy của $\Delta$ nằm hoàn toàn trên 0.
2. Khi chấm trên toàn bộ test, khoảng cách còn **rộng hơn** (+14.00% so với +10.67%). Lý do là 19 chương trình của Direct đạt hidden nhưng không qua chính các public test (13 trong số đó ở Competition), còn RethinkMCTS chỉ có 9 trường hợp như vậy. Direct không dùng public test để chọn hoặc sửa, nên dễ "đúng tình cờ" trên một hidden suite rất nhỏ (xem §4.4).
3. Mức tăng tuyệt đối lớn nhất nằm ở Interview: từ 13% lên 27% khi chấm trên hidden, từ 11% lên 26% khi chấm trên toàn bộ test.

---

## 4.3. So sánh với Best-of-3 trên tập con 160 bài

Run Best-of-3 dừng ở 160/300 bài (100 Introductory + 60 Interview đầu tiên) do hết credit. Tập con này không phải mẫu ngẫu nhiên của APPS-300: nó không có bài Competition. Vì vậy, kết quả chỉ so sánh trên chính 160 bài này.

### Bảng 4.4. Direct, Best-of-3 và RethinkMCTS trên cùng 160 bài

| Cách chấm | Direct | Best-of-3 | RethinkMCTS | $\Delta$ MCTS − BoN-3 (95%) | McNemar MCTS so với BoN-3 |
| :--- | :-: | :-: | :-: | :-: | :-: |
| Hidden | 29.38% (47) | 35.62% (57) | **40.00% (64)** | +4.38% [0.00; +9.38] | 11 so với 4, $p = 0.118$ |
| Toàn bộ test | 26.88% (43) | 30.62% (49) | **38.12% (61)** | +7.50% [+2.50; +12.50] | 14 so với 2, $p = 0.004$ |

Mean Pass Rate trên hidden: Direct 43.45%, BoN-3 49.85%, RethinkMCTS 63.45%.

**Nhận xét.** Best-of-3 tốt hơn Direct (hidden: 10 so với 0 bài, $p = 0.002$), tức là việc lấy thêm mẫu và chọn theo public test đã có ích. Khi chấm trên hidden, RethinkMCTS hơn Best-of-3 4.38 điểm nhưng chưa đạt ý nghĩa thống kê. Khi chấm trên toàn bộ test, khoảng cách là 7.50 điểm và có ý nghĩa ($p = 0.004$).

Hai phương pháp **không dùng cùng ngân sách**: Best-of-3 dùng trung bình 4.07 lời gọi/bài, RethinkMCTS dùng 13.6 lời gọi/bài trên cùng tập con. Kết quả này cho thấy MCTS tốt hơn BoN-3 ở mức chi phí tương ứng của mỗi phương pháp, chưa phải so sánh với cùng ngân sách.

---

## 4.4. Ảnh hưởng của kích thước hidden suite

Quy tắc "2 test đầu làm public, phần còn lại làm hidden" tạo ra hidden suite rất nhỏ ở nhiều bài, vì một số bài APPS chỉ có khoảng 3 test.

### Bảng 4.5. Phân bố kích thước hidden suite và số bài đạt (chấm trên hidden) theo phân tầng

| Phân tầng | Số hidden test | Số bài | Direct đạt | RethinkMCTS đạt |
| :--- | :-: | :-: | :-: | :-: |
| Introductory | 1 | 24 | 14 | 19 |
| | 2–5 | 21 | 10 | 12 |
| | > 5 | 55 | 18 | 22 |
| Interview | 1 | 13 | 5 | 7 |
| | 2–5 | 10 | 1 | 3 |
| | > 5 | 77 | 7 | 17 |
| Competition | 1 | **48** | **19** | **19** |
| | 2–5 | 11 | 1 | 4 |
| | > 5 | 41 | 1 | 5 |

**Nhận xét.**

1. Gần một nửa số bài Competition (48/100) chỉ có **một** hidden test. 19/21 bài Competition mà Direct giải được nằm trong nhóm này. Đây là lý do Direct đạt Pass@1 ở Competition (21%) cao hơn ở Interview (13%), trái với thứ tự độ khó.
2. Trên các bài Competition có hơn 5 hidden test, Direct đạt 1/41 và RethinkMCTS đạt 5/41. Năng lực thực sự của 14B ở các bài thi đấu thấp hơn nhiều so với con số 21–28%.
3. Mức tăng của RethinkMCTS tập trung ở các bài có hidden suite lớn hơn (Interview > 5 test: từ 7 lên 17 bài). Đây là bằng chứng mạnh hơn cho hiệu quả của tìm kiếm so với tổng Pass@1.

Do đó, Pass@1 theo phân tầng Competition chấm trên hidden **không nên** dùng làm bằng chứng chính. Chúng tôi khuyến nghị dùng cách chấm trên toàn bộ test (Bảng 4.2) khi so sánh giữa các phân tầng và khi đối chiếu với nhánh 7B.

---

## 4.5. Kết quả trên HumanEval-164

### Bảng 4.6. Kết quả 14B trên HumanEval-164

| Phương pháp | Pass@1 | Số bài đạt | Lời gọi TB/bài | Token TB/bài | Thời gian giải TB/bài | Mức tin cậy |
| :--- | :-: | :-: | :-: | :-: | :-: | :--- |
| **RethinkMCTS** ([`humaneval_mcts_dual_14b`](../../runs/humaneval_mcts_dual_14b/summary.json)) | **90.85%** | **149/164** | 4.64 | 3.218 | 25.3 s | Kết quả chính (schema 2) |
| Direct (`humaneval_direct_14b`) | 90.24% | 148/164 | 1.91 | — | 5.1 s | Thăm dò, code cũ |
| Best-of-3 (`humaneval_bon3_14b`) | 91.46% | 150/164 | 5.77 | — | 24.0 s | Thăm dò, code cũ |
| RethinkMCTS (`humaneval_mcts_14b`) | 93.29% | 153/164 | 4.55 | — | — | Thăm dò, code cũ, cấu hình không đồng nhất |

Ba run thăm dò được tạo trước khi có hệ thống manifest (schema 2), bằng phiên bản code cũ. Ở phiên bản đó, phần đếm lời gọi chưa tính block analysis và tổng token chưa được ghi.

Riêng run `humaneval_mcts_14b`: 11 bài đầu (`python_0`–`python_10`) được lấy từ một lượt chạy trước với cấu hình khác (khoảng 20 lời gọi và 8 lần sinh code mỗi bài), 153 bài còn lại chạy ở một lượt sau. Run này **có bật critic**: trong [`evaluations.jsonl`](../../runs/humaneval_mcts_14b/evaluations.jsonl), cả 232 đánh giá qua hết public test đều có `self_eval_status = evaluated` và phần thưởng 0.97–0.99, đúng với $(a, b) = (0.8, 0.2)$. Vì vậy, đây không phải kết quả Test-only, và nhánh 14B hiện chưa có run Test-only nào trên HumanEval. Chúng tôi **không** so sánh run này với run RethinkMCTS chính, và không quy chênh lệch 93.29% − 90.85% cho bất kỳ thành phần cụ thể nào.

**Nhận xét.**

- HumanEval gần chạm trần với 14B. Ứng viên đầu tiên đã qua hết public test ở 147/164 bài; chỉ 17 bài phải dùng đến rethink.
- Chênh lệch giữa các phương pháp chỉ 1–5 bài. Khi chưa chạy lại Direct và Best-of-3 bằng cùng phiên bản code, chưa thể kết luận phương pháp nào tốt hơn trên HumanEval.

---

## 4.6. Chi phí suy luận

### Bảng 4.7. Chi phí trung bình mỗi bài trên APPS-300 (14B)

| Phân tầng | Phương pháp | Lời gọi | Token | Thời gian giải | Lần sinh code | Lần rethink | Vòng lặp tìm kiếm |
| :--- | :--- | :-: | :-: | :-: | :-: | :-: | :-: |
| Introductory | Direct | 1.45 | 1.329 | 21.7 s | 1.00 | 0 | 0 |
| | RethinkMCTS | 11.18 | 25.540 | 80.7 s | 4.21 | 2.29 | 2.20 |
| Interview | Direct | 1.18 | 1.355 | 24.1 s | 1.00 | 0 | 0 |
| | RethinkMCTS | 17.73 | 42.788 | 119.7 s | 6.76 | 4.13 | 3.17 |
| Competition | Direct | 1.17 | 1.434 | 27.9 s | 1.00 | 0 | 0 |
| | RethinkMCTS | 16.96 | 43.811 | 125.6 s | 6.51 | 3.93 | 2.99 |
| **Toàn bộ** | Direct | 1.27 | 1.373 | 24.6 s | 1.00 | 0 | 0 |
| | **RethinkMCTS** | **15.29** | **37.759** | **108.7 s** | **5.83** | **3.45** | **2.79** |

Lời gọi của Direct lớn hơn 1 vì critic được gọi khi chương trình qua hết public test. Lời gọi này không ảnh hưởng đến việc chọn chương trình của Direct.

### Bảng 4.8. Phân rã lời gọi và token theo vai trò (RethinkMCTS, APPS-300)

| Vai trò | Lời gọi | Tỷ trọng lời gọi | Token vào | Token ra | Tổng token | Tỷ trọng token |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: |
| Mở rộng thought (expansion) | 405 | 8.8% | 402.222 | 75.738 | 477.960 | 4.2% |
| Sinh code | 1.748 | 38.1% | 1.264.598 | 974.962 | 2.239.560 | 19.8% |
| Phân tích khối CFG (block analysis) | 1.208 | 26.3% | 5.717.479 | 126.250 | 5.843.729 | **51.6%** |
| Rethink | 1.066 | 23.2% | 2.555.861 | 87.815 | 2.643.676 | 23.3% |
| Critic | 160 | 3.5% | 121.251 | 1.606 | 122.857 | 1.1% |
| **Tổng** | **4.587** | 100% | 10.061.411 | 1.266.371 | **11.327.782** | 100% |

Có 3 bài (`apps_3149`, `apps_3869`, `apps_3946`) với tổng cộng 6 lời gọi không nhận được số token từ server, nên tổng token là cận dưới.

**Nhận xét.**

1. RethinkMCTS tốn khoảng 12 lần lời gọi, 27.5 lần token và 4.4 lần thời gian so với Direct, để tăng Pass@1 thêm 10.67 điểm (chấm trên hidden).
2. Phân tích khối CFG chiếm hơn một nửa số token, chủ yếu là token đầu vào chứa trạng thái biến trước và sau mỗi khối. Điều này khớp với nhận xét của bài báo gốc về chi phí của block-level analysis.
3. **Ngân sách thực sự ràng buộc là token.** 161 bài dừng sớm vì đã qua hết public test. Trong 139 bài còn lại, 133 bài dừng vì chạm trần 65.536 token, chỉ 4 bài dừng vì đủ 16 lần sinh code (2 bài vì lý do khác). Số lần sinh code cao nhất ở một bài là 16, nhưng chương trình được chọn có thứ tự sinh cao nhất là 11.

Chúng tôi không báo cáo chi phí GPU bằng tiền, vì artifact không ghi lại thời gian GPU tính phí của từng run.

---

## 4.7. Hành vi tìm kiếm và vai trò của rethink

### 4.7.1. Ứng viên đầu tiên và loại lỗi

Trên APPS-300, ứng viên đầu tiên của RethinkMCTS qua hết public test ở 84/300 bài (28.0%). Ở 216 bài còn lại, lỗi trên public test đầu tiên thất bại phân bố như sau:

| Loại lỗi | Số bài | Tỷ lệ |
| :--- | :-: | :-: |
| Sai kết quả (WA) | 184 | 85.2% |
| Lỗi runtime (RE) | 30 | 13.9% |
| Quá thời gian (TLE) | 2 | 0.9% |
| Lỗi cú pháp (CE) | 0 | 0.0% |

Lỗi chủ yếu là lỗi logic, không phải lỗi cú pháp. Đây là loại lỗi mà feedback dựa trên trạng thái thực thi được thiết kế để hỗ trợ.

### 4.7.2. Nguồn gốc của các lời giải đúng

Trong 108 bài RethinkMCTS giải đúng (chấm trên hidden), chương trình được chọn có nguồn gốc như sau:

| Nguồn gốc chương trình được chọn | Introductory | Interview | Competition | Tổng |
| :--- | :-: | :-: | :-: | :-: |
| Sinh ra sau một lần rethink | 10 | 10 | 10 | **30 (27.8%)** |
| Sinh trực tiếp từ một nút thought (initial) | 43 | 17 | 18 | 78 (72.2%) |

Nhãn "initial" gồm cả ứng viên đầu tiên của bài và ứng viên ở các nhánh được mở rộng sau đó; các nhánh này cũng nhận feedback từ lần thất bại trước. Vì vậy, 30 bài là **cận dưới** của số bài mà rethink trực tiếp tạo ra lời giải, và không đo được đóng góp gián tiếp của rethink lên các nhánh khác.

Muốn kết luận rethink đóng góp bao nhiêu điểm Pass@1, cần thí nghiệm triệt tiêu với `max_rethinks_per_node = 0` (E4 trong [EXPERIMENT_CHECKLIST.md](EXPERIMENT_CHECKLIST.md)). Thí nghiệm này chưa được chạy.

### 4.7.3. Diễn biến theo số ứng viên đã sinh

Bảng 4.9 cho biết, nếu dừng tìm kiếm sau $k$ ứng viên, có bao nhiêu bài đã có ít nhất một ứng viên qua hết public test, và bao nhiêu bài có chương trình được chọn cuối cùng nằm trong $k$ ứng viên đầu và đạt hidden.

### Bảng 4.9. Số bài đạt theo số ứng viên $k$ (RethinkMCTS, APPS-300)

| $k$ | Bài đã có ứng viên qua hết public | Bài đạt hidden (cận dưới) | Pass@1 hidden (cận dưới) |
| :-: | :-: | :-: | :-: |
| 1 | 84 | 66 | 22.00% |
| 2 | 107 | 80 | 26.67% |
| 4 | 133 | 94 | 31.33% |
| 8 | 156 | 105 | 35.00% |
| Toàn bộ (≤ 16) | 161 | 108 | 36.00% |

Cột hidden là cận dưới, vì chỉ chương trình được chọn cuối cùng mới được chấm trên hidden. Nếu dừng sớm hơn, chương trình được chọn có thể là một ứng viên khác chưa từng được chấm.

Phần lớn mức tăng đến trong 8 ứng viên đầu. Ở giai đoạn sau, nhiều bài đã chạm trần token (§4.6), nên không thể kết luận về hiệu quả biên của ngân sách lớn hơn.

### 4.7.4. Tỷ lệ code hợp lệ trên cây

Có 161 trong 1.748 ứng viên (9.21%) qua hết public test. Chỉ số này **không so sánh được** với Table 4 của bài báo gốc (15.60% trên APPS Introductory, 53.29% trên HumanEval):

- Cơ chế dừng sớm kết thúc tìm kiếm ngay khi có ứng viên đầu tiên qua hết public test. Vì vậy, mỗi bài có tối đa một ứng viên như vậy, và tỷ lệ này bị giới hạn bởi cách dừng chứ không chỉ bởi chất lượng cây.
- Bài báo gốc chạy đủ 16 rollout và tính riêng cho APPS Introductory.

---

## 4.8. Vai trò của LLM critic

### 4.8.1. Critic không làm thay đổi chương trình được chọn

Phần thưởng kép dùng điểm critic $v_{\text{llm}}$ chỉ khi ứng viên qua hết public test. Trong cấu hình đã chạy, hai cơ chế khiến điểm này không ảnh hưởng đến kết quả:

1. **Dừng sớm:** tìm kiếm kết thúc ngay sau khi ứng viên đầu tiên qua hết public test và được critic chấm, nên điểm critic không còn được dùng để hướng dẫn tìm kiếm.
2. **Chọn cuối cùng theo phần thưởng lớn nhất:** với 2 public test, $v_{\text{test}} \in \{0;\ 0.5;\ 1\}$. Ứng viên qua hết public test có phần thưởng ít nhất $0.8 \cdot 1 + 0.2 \cdot (-1) = 0.6 > 0.5$, nên luôn được chọn dù bị critic chấm thấp.

Kiểm tra trên artifact cho thấy, ở **toàn bộ 161 bài APPS và 159 bài HumanEval có ứng viên qua hết public test**, chương trình được chọn đều là ứng viên đầu tiên đạt điều kiện đó. Các bài còn lại không có ứng viên nào để critic chấm. Như vậy, trong các run này, RethinkMCTS với phần thưởng kép tương đương về hành vi với phiên bản chỉ dùng test, khác ở chỗ tốn thêm 160 lời gọi critic (1.1% token).

Hệ quả cho thiết kế thí nghiệm: thí nghiệm triệt tiêu "Test-only" trên 14B với cấu hình này sẽ không đo được gì về vai trò của critic. Bài báo gốc chạy đủ 16 rollout, không dừng sớm, nên điểm critic tham gia vào việc chọn nhánh và chọn chương trình.

### 4.8.2. Điểm critic có mang tín hiệu về độ đúng

Dù không được dùng, điểm critic vẫn có liên hệ với kết quả trên hidden. Bảng 4.10 tính trên 161 chương trình được chọn đã qua hết public test.

### Bảng 4.10. Điểm critic của Qwen-14B và kết quả trên hidden (APPS-300)

| Điểm critic | Đạt hidden | Không đạt hidden | Tỷ lệ không đạt |
| :-: | :-: | :-: | :-: |
| 1.0 hoặc 0.8 (chấp nhận) | 84 | 40 | 32.3% |
| 0.0 hoặc −1.0 (không chấp nhận) | 15 | 22 | **59.5%** |
| **Tổng** | 99 | 62 | 38.5% |

Tương quan hạng Spearman giữa điểm critic và tỷ lệ hidden đạt là $\rho = 0.243$ ($p = 0.002$); tương quan point-biserial với việc đạt toàn bộ hidden là $r_{pb} = 0.239$ ($p = 0.002$) ([`runs/cross_critic_analysis_14b/summary.json`](../../runs/cross_critic_analysis_14b/summary.json)).

Khi critic không chấp nhận, xác suất chương trình sai trên hidden gần gấp đôi tỷ lệ nền. Đây là tín hiệu yếu đến vừa phải: critic vẫn chấp nhận 40/62 chương trình sai. Một hướng sử dụng tín hiệu này là chỉ cho dừng sớm khi critic chấp nhận (xem [EXPERIMENT_CHECKLIST.md](EXPERIMENT_CHECKLIST.md), mục 0).

### 4.8.3. So sánh với một critic khác mô hình (Codestral)

Chúng tôi cho `codestral-latest` (Mistral) chấm lại cùng 161 chương trình ([`scripts/cross_critic_benchmark.py`](../../scripts/cross_critic_benchmark.py)).

| Chỉ số | Qwen-14B (tự chấm, trong lúc tìm kiếm) | Codestral (chấm lại sau) |
| :--- | :-: | :-: |
| Spearman $\rho$ với tỷ lệ hidden đạt | **+0.243** ($p = 0.002$) | +0.033 ($p = 0.68$) |
| Point-biserial $r_{pb}$ với đạt toàn bộ hidden | **+0.239** ($p = 0.002$) | −0.042 ($p = 0.60$) |
| Tỷ lệ chấm 1.0 | 121/161 (75.2%) | 145/161 (90.1%) |
| Chấp nhận chương trình sai (trên 62) | 40 (64.5%) | 59 (95.2%) |
| Chấp nhận chương trình đúng (trên 99) | 84 (84.8%) | 92 (92.9%) |

Codestral gần như chấp nhận mọi chương trình đã qua public test, nên điểm của nó gần như không phân biệt được đúng sai.

**Giới hạn của so sánh này:** hai critic **không** nhận cùng đầu vào. Trong lúc tìm kiếm, prompt critic của Qwen không chứa chuỗi thought (mục "Reasoning path" hiển thị "(none)"). Trong khi đó, script chấm lại đưa chuỗi thought của nút vào prompt cho Codestral. Ngoài ra, Codestral chỉ được chạy một lần trên 161 chương trình. Kết quả vì vậy chỉ cho thấy Codestral, với prompt này, không phân biệt tốt hơn Qwen-14B tự chấm. Nó chưa đủ để kết luận về ưu thế chung của self-critic.

---

## 4.9. Đối chiếu với nhánh 7B (tham khảo)

Nhánh 7B (`qwen2.5-coder:7b-instruct`) dùng cùng cohort APPS-300 (đã kiểm tra trùng 300/300 ID) nhưng khác ở nhiều yếu tố ngoài kích thước mô hình:

| Yếu tố | Nhánh 7B | Nhánh 14B |
| :--- | :--- | :--- |
| Codebase | `external/ReThinkMCTS` | `src/rethink_mcts` |
| Public test trên APPS | Nửa đầu số test (`half`) | 2 test đầu |
| Tập chấm APPS | Toàn bộ test | Hidden (và toàn bộ test, Bảng 4.2) |
| Ngân sách tìm kiếm | 2 rollout (cộng các lần rethink) | Tối đa 16 lần sinh code, dừng sớm |
| Prompt HumanEval MCTS Dual | `native_v1` (run cũ) | `native_v2` |
| Dữ liệu từng bài trong repo | Không có | Có |

Vì vậy, bảng dưới đây chỉ mang tính mô tả. Chúng tôi dùng cách chấm trên toàn bộ test cho 14B để khớp tập chấm của 7B. Chênh lệch giữa hai cột không thể quy riêng cho kích thước mô hình.

### Bảng 4.11. Pass@1 trên APPS-300 khi chấm trên toàn bộ test

| Phân tầng | 7B Direct | 7B MCTS Dual | 7B MCTS Test-only | 14B Direct | 14B RethinkMCTS |
| :--- | :-: | :-: | :-: | :-: | :-: |
| Introductory | 31.00% | 38.00% | 41.00% | 38.00% | 50.00% |
| Interview | 7.00% | 14.00% | 18.00% | 11.00% | 26.00% |
| Competition | 4.00% | 5.00% | 9.00% | 8.00% | 23.00% |
| **Toàn bộ** | 14.00% | 19.00% | 22.67% | 19.00% | 33.00% |

Nguồn 7B: [benchmark-v2-all-tests.md](../results/7b/benchmark-v2-all-tests.md), [rethinkmcts-apps-native-v2-w4-retry.md](../results/7b/rethinkmcts-apps-native-v2-w4-retry.md), [rethinkmcts-test-only-v1.md](../results/7b/rethinkmcts-test-only-v1.md).

Trên HumanEval-164: 7B Direct 80.49%, 7B MCTS Dual 91.46% (prompt `native_v1`), 7B MCTS Test-only 89.63%. Phía 14B xem Bảng 4.6.

**Nhận xét mô tả.**

- Ở cả hai kích thước, tìm kiếm cây đều cải thiện so với Direct. Với 14B, mức cải thiện đã được kiểm định ghép cặp (Bảng 4.3). Với 7B, chưa kiểm định ghép cặp được vì không có dữ liệu từng bài trong repo.
- Khi chấm trên toàn bộ test, khoảng cách giữa 14B Direct và 7B Direct ở Competition thu hẹp còn 8% so với 4%. Phần lớn con số 21% trước đây đến từ các bài chỉ có một hidden test (§4.4).
- Trên 7B, Test-only cao hơn Dual (22.67% so với 19.00%). Báo cáo gốc của nhánh 7B lưu ý rằng hai run này khác nhau về độ phủ ứng viên và không nên quy chênh lệch riêng cho việc bỏ critic.

---

## 4.10. Tóm tắt

1. Trên APPS-300, RethinkMCTS với 14B tăng Pass@1 so với Direct: +10.67 điểm khi chấm trên hidden (36.00% so với 25.33%) và +14.00 điểm khi chấm trên toàn bộ test (33.00% so với 19.00%). Cả hai khác biệt đều có ý nghĩa thống kê theo kiểm định ghép cặp.
2. Trên 160 bài có Best-of-3, RethinkMCTS hơn Best-of-3 7.50 điểm khi chấm trên toàn bộ test ($p = 0.004$) và 4.38 điểm khi chấm trên hidden ($p = 0.118$), với chi phí lời gọi cao hơn khoảng 3 lần.
3. Chi phí của RethinkMCTS chủ yếu nằm ở phân tích khối CFG (51.6% token). Trần 65.536 token là ràng buộc thực tế ở 133/300 bài.
4. Trong cấu hình có dừng sớm, critic không làm thay đổi chương trình được chọn ở bất kỳ bài nào, dù điểm của nó có tương quan dương với độ đúng trên hidden.
5. Cách chia "2 test đầu làm public" để lại một hidden test duy nhất ở 48% bài Competition. Kết quả theo phân tầng Competition chấm trên hidden cần được diễn giải thận trọng.
6. HumanEval-164 gần chạm trần với 14B (RethinkMCTS 90.85%). Các run Direct và Best-of-3 trên HumanEval cần được chạy lại bằng cùng phiên bản code trước khi so sánh.
