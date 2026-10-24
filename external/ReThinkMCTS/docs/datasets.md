# Dataset của dự án

## Benchmark cohort cho cac lan chay moi

Dataset goc khong doi: APPS test 5.000 bai, HumanEval test 164 bai. Cohort
`benchmark_v2` duoc khoa cho model/MCTS va judge tu nay ve sau:

| Dataset | Manifest | Quy mo | Cach chon |
|---|---|---:|---|
| APPS test | `data/samples/benchmark_v2/apps_test_300.json` | 300 | Dung 100 ID moi muc kho tu cohort cua nhom doi chieu |
| APPS evaluator pilot | `data/samples/benchmark_v2/apps_test_30_external_evaluator_pilot.json` | 30 | 10 ID/muc kho rut co dinh tu benchmark_v2; chi bao cao pilot n=30 |
| HumanEval test | `data/samples/benchmark_v2/humaneval_test_164.json` | 164 | Toan bo `HumanEval/0` den `HumanEval/163` |

APPS duoc lay tu [manifest goc](https://github.com/Viendeptrai1/rethink-mcts-slm/blob/main/data/cohorts/apps_benchmark_300.json)
va [script chon mau](https://github.com/Viendeptrai1/rethink-mcts-slm/blob/main/scripts/sample_apps_300_stratified.py):
loc `len(inputs) >= 3` va `len(inputs) == len(outputs)`, sau do lay mau ngau
nhien phan tang khong hoan lai, seed `2027`, 100 bai moi muc introductory,
interview, competition. Nguon HumanEval la [processed.jsonl](https://github.com/Viendeptrai1/rethink-mcts-slm/blob/main/data/humaneval/processed.jsonl)
du 164 `Python/0..163`; ID so duoc doi chieu voi `HumanEval/0..163` cuc bo.

`evaluation_v1` (100 APPS + 100 HumanEval) la benchmark **da chay truoc day**;
giu nguyen manifest va ket qua de truy vet, khong so truc tiep voi cohort moi.
`baseline_v1` con cu hon va cung duoc giu de truy vet. Generation full khong
truyen `--sample-file`. Khong dung `--limit` thay cho manifest vi no chi lay
nhung ID dau, khong giu dung cohort.

Xem thêm [báo cáo dữ liệu](dataset-report.md) để biết số liệu kiểm tra cục bộ,
phân bố cohort và chính sách test. File này ghi quyết định cấp dự án. Cấu trúc
file, schema chi tiết và ví dụ đọc dữ liệu nằm tại
[../data/README.md](../data/README.md).

## Phạm vi đã chốt

Dự án sử dụng đúng hai dataset:

| Dataset | Vai trò | Biểu diễn cục bộ | Trạng thái |
|---|---|---|---|
| APPS | Baseline chính theo độ khó | `data/apps/raw` | Đủ 5.000 train + 5.000 test |
| HumanEval | Benchmark hàm Python | `data/humaneval/arrow` + `public_tests.jsonl` | Đủ 164 test |

**Không sử dụng CodeContests** trong phạm vi hiện tại.

## Lý do chọn biểu diễn

- APPS giữ bản raw theo từng bài vì cấu trúc này phù hợp loader của repo
  RethinkMCTS gốc. Không giữ thêm bản Arrow trùng dữ liệu.
- HumanEval giữ bản Arrow vì dữ liệu nhỏ, schema ổn định và có thể load trực tiếp
  bằng Hugging Face `datasets`.

## Nguyên tắc public/private tests

Paper dùng public tests cho search và private tests để đo khả năng tổng quát.
APPS raw hiện tại không có cột public/private. Đã đối chiếu repo gốc:
`get_test_cases(..., "half")` lấy `len(inputs)//2` test đầu làm public,
phần còn lại làm private. Đây cũng là mặc định native. Tùy chọn nghiên cứu
`half_min2` lấy `max(2, len(inputs)//2)` test đầu làm public, có kiểm tra còn
ít nhất một test giữ lại; phải dùng run mới và ghi rõ policy. Đây là thay đổi
protocol so với repo tác giả. Chi tiết ở `implementation-audit.md`.

HumanEval Arrow chứa official harness trong cột `test`, nhưng không có
`given_tests`. Search native dùng 164 hàng `given_tests` đã pin tại
`data/humaneval/public_tests.jsonl`; `public_tests_source.json` ghi commit và
SHA-256 của [nguồn đối chiếu](https://github.com/Viendeptrai1/rethink-mcts-slm/blob/fabdc43ac2ae281262271aad2aadad488c76d667/data/humaneval/processed.jsonl).
ID, prompt và entry point được đối chiếu với Arrow cục bộ; 164/164 hàng có
1-8 assertions. Official harness chỉ chạy cho candidate cuối, không dùng làm
reward trong search. APPS search lấy nửa đầu mỗi bộ test làm public; đây là
policy native, không phải split có sẵn trong dữ liệu gốc. Final evaluation
chạy toàn bộ APPS tests, gồm public tests và phần còn lại.

Trong đúng cohort APPS 300 của `benchmark_v2`, 85 bài chỉ có 3 test; policy
`half` cho search nhìn thấy 1 public test ở mỗi bài này. Trung bình cohort
có 19,86 test/bài. Việc chuyển sang `half_min2` chỉ tăng public coverage
ở 85 bài đó và không thay ID, schema hoặc nội dung file dữ liệu.

## Kiểm tra trước mỗi thử nghiệm

- APPS có đúng 5.000 thư mục ở mỗi split.
- Mỗi bài APPS có `question.txt`, `solutions.json`, `input_output.json` và
  `metadata.json`; `starter_code.py` là tùy chọn.
- HumanEval load được 164 dòng và đủ năm cột chuẩn; file public tests có
  đúng 164 hàng, mỗi hàng có ít nhất một assertion.
- Đường dẫn cấu hình trỏ tới dữ liệu cục bộ, không vô tình tải lại dataset.
- Không log toàn bộ lời giải tham khảo vào prompt hoặc artifact công khai.

## Quy tắc cập nhật

Mọi thay đổi nguồn, split, schema, số lượng, định dạng hoặc đường dẫn phải cập nhật
đồng thời file này, `data/README.md`, `project-status.md` và các script liên quan.

