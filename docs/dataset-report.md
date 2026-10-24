# Báo cáo dữ liệu APPS và HumanEval

Kiểm tra trực tiếp dữ liệu tại `D:\ReThinkMCTS\data` ngày 2026-10-07. Báo cáo
này mô tả **dữ liệu đầu vào và cohort benchmark**, không phải kết quả model.
Schema đầy đủ và cách đọc file nằm ở [data/README.md](../data/README.md);
quyết định phạm vi nằm ở [datasets.md](datasets.md).

## Tổng quan

| Dataset | Split cục bộ | Quy mô gốc | Cohort `benchmark_v2` | Đơn vị bài toán |
|---|---|---:|---:|---|
| APPS | `train`, `test` | 5.000 bài/split | 300 bài từ `test` | Sinh chương trình Python hoàn chỉnh hoặc hàm theo giao diện đề bài |
| HumanEval | `test` | 164 bài | Toàn bộ 164 bài | Hoàn thiện hàm Python từ chữ ký và docstring |

Dự án không dùng CodeContests. `baseline_v1` và `evaluation_v1` là các sample
100+100 lịch sử; benchmark hiện tại dùng riêng manifest `benchmark_v2`.
Generation full APPS có thể đi qua 5.000 bài `test`, nhưng các bảng benchmark
trong README dùng **cùng 300 ID cố định**; HumanEval dùng đủ 164 ID.

## APPS

### Vị trí, ID và schema

Mỗi bài ở `data/apps/raw/<split>/<id_4_chữ_số>/`. Ví dụ `test/0000` và
`train/0000` thuộc hai split khác nhau; ID số chỉ phân biệt bài **trong
split**, không phải ID duy nhất toàn dự án. Kiểm tra cục bộ thấy đúng 5.000
thư mục ở mỗi split, ID `0000` đến `4999`, không thiếu bốn file bắt buộc.

| File | Nội dung | Kiểu/ý nghĩa |
|---|---|---|
| `question.txt` | Đề bài, mô tả đầu vào/đầu ra, ràng buộc | Văn bản UTF-8 |
| `input_output.json` | Test case | JSON object có `inputs` và `outputs` là hai danh sách cùng vị trí; có thể có `fn_name` |
| `solutions.json` | Lời giải tham khảo | JSON array; không đưa vào prompt sinh code |
| `metadata.json` | Mức khó và nguồn | JSON object với `difficulty`, `url` |
| `starter_code.py` | Code khởi tạo | Tùy chọn; có ở 3.350 bài `train` và 54 bài `test` |

Nếu `fn_name` có giá trị, executor gọi hàm/phương thức (call-based); nếu
không, chương trình đọc `stdin` và ghi `stdout`. Kiểu của từng phần tử
`inputs`/`outputs` phụ thuộc giao diện, không được giả định luôn là chuỗi.
Trong cohort 300 bài, **298 bài stdin/stdout** và **2 bài call-based**.
Loader lấy `question.txt` cùng `starter_code.py` nếu có; file lời giải tham
khảo không được loader bài toán đọc.

Phân bố mức khó trên toàn split đã kiểm tra:

| Split | Introductory | Interview | Competition | Tổng |
|---|---:|---:|---:|---:|
| `train` | 2.639 | 2.000 | 361 | 5.000 |
| `test` | 1.000 | 3.000 | 1.000 | 5.000 |

### Cohort và test

Manifest `data/samples/benchmark_v2/apps_test_300.json` chứa 300 ID duy
nhất, `sample_id=apps_benchmark_300_stratified_seed2027`, `seed=2027`, và
`difficulty_by_problem_id`. Theo metadata trong manifest, cohort của nhóm
đối chiếu lọc bài có **ít nhất 3 test** và
`len(inputs) == len(outputs)`, rồi lấy mẫu không hoàn lại theo ba tầng độ
khó: **100 Introductory, 100 Interview, 100 Competition**. Kiểm tra dữ liệu
cục bộ xác nhận cả 300 bài đáp ứng hai điều kiện trên; không bốc lại ID
cho model hay phương pháp khác.

300 bài có tổng **5.959 test**: ít nhất 3, trung vị 12, trung bình 19,86,
nhiều nhất 134 test/bài. **85 bài có đúng 3 test**.

APPS raw **không đánh dấu sẵn public/private**. Search MCTS với policy
`half` lấy `floor(n/2)` test đầu làm public, phần còn lại làm private theo
quy ước của dự án. Trên cohort này là **2.896 public** và **3.063 private**
test; mỗi bài 3 test chỉ có 1 public test. Đây là phép chia theo thứ tự
trong file, không phải hai tập public/hidden độc lập do nguồn APPS công bố.
Final judge của benchmark chạy **tất cả test** trong `input_output.json`,
gồm cả hai phần. Tên `private` trong search không nên được hiểu là một
hidden test set bên ngoài dataset.

## HumanEval

HumanEval nằm ở `data/humaneval/arrow/`, được lưu bằng Hugging Face
`DatasetDict.save_to_disk()`; dữ liệu thực ở shard Arrow của split `test`.
Kiểm tra `load_from_disk()` đọc được đúng **164 hàng** và năm cột kiểu string:

| Cột | Nội dung |
|---|---|
| `task_id` | `HumanEval/0` đến `HumanEval/163` |
| `prompt` | Chữ ký hàm, docstring và mô tả để model hoàn thiện |
| `canonical_solution` | Thân hàm tham khảo; không đưa vào prompt |
| `test` | Mã Python của official harness |
| `entry_point` | Tên hàm cần gọi/chấm |

Manifest `data/samples/benchmark_v2/humaneval_test_164.json` giữ đủ các ID
số `0..163`; loader ánh xạ chúng sang `HumanEval/0..163`. Không lấy mẫu
ngẫu nhiên và không có nhãn độ khó như APPS.

`data/humaneval/public_tests.jsonl` là file **phụ trợ cho MCTS search**,
không phải cột của Arrow. File có 164 dòng JSONL, mỗi dòng gồm `task_id`,
`entry_point`, `given_tests` (danh sách 1-8 câu `assert`); 164 ID duy nhất.
`public_tests_source.json` ghi commit nguồn và SHA-256 để truy vết. Search
chạy các `given_tests`; final judge dùng cột `test` của official harness.
HumanEval tại đây không có một bộ hidden/private độc lập, nên báo cáo
**Pass@1**, không báo Pass Rate theo từng hidden test.

## Quy tắc tái lập

- Dùng nguyên hai manifest trong `data/samples/benchmark_v2/`; không dùng
  `--limit` thay cho cohort vì nó chỉ lấy các ID đầu.
- Giữ `split=test`, thứ tự test APPS và policy `half` khi tái chạy MCTS;
  đổi public policy là một thí nghiệm khác.
- Không đưa `solutions.json`, `canonical_solution` hoặc official `test`
  vào prompt sinh code hay reward trong search.
- Ghi rõ số candidate thiếu và quy tắc mẫu số khi lập bảng; thiếu candidate
  không đồng nghĩa lời giải sai trên các test chưa từng chạy.
