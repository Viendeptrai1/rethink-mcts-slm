# Dataset: APPS và HumanEval

## Sample benchmark cố định

Dữ liệu gốc gồm 5.000 APPS test và 164 HumanEval test. Project giữ hai loại
manifest cố định với mục đích khác nhau:

```text
data/samples/baseline_v1/apps_test_100.json
data/samples/baseline_v1/humaneval_test_100.json
data/samples/evaluation_v1/apps_test_100.json
data/samples/evaluation_v1/humaneval_test_100.json
data/samples/benchmark_v2/apps_test_300.json
data/samples/benchmark_v2/apps_test_30_external_evaluator_pilot.json
data/samples/benchmark_v2/humaneval_test_164.json
```

`baseline_v1` và `evaluation_v1` là sample lịch sử; kết quả baseline 100+100
đã công bố nội bộ gắn với `evaluation_v1`, không đổi hoặc gán lại số liệu.
`benchmark_v2` là cohort cho **các lần chạy mới**: APPS 300 ID phân tầng
(100 introductory, 100 interview, 100 competition; seed 2027) lấy đúng từ
[manifest của nhóm đối chiếu](https://github.com/Viendeptrai1/rethink-mcts-slm/blob/main/data/cohorts/apps_benchmark_300.json),
và HumanEval toàn bộ 164 ID từ `0` đến `163`. Repo đối chiếu dùng tiền tố
`apps_` và `Python/`; loader cục bộ dùng ID số và `HumanEval/` tương ứng.
Không bốc lại ID khi đổi model hoặc phương pháp. Cohort `benchmark_v2` đã được
chấm cho baseline và RethinkMCTS; kết quả nằm ở `README.md` cấp dự án.

`apps_test_30_external_evaluator_pilot.json` là cohort pilot cố định được rút
không hoàn lại từ 300 ID trên bằng seed `20261018`, đúng 10 ID mỗi mức khó.
Metric phải ghi rõ `n=30` (và `n=10` theo mỗi mức); tuyệt đối không gán hoặc
ngoại suy thành APPS 300. HumanEval của thử nghiệm này vẫn dùng manifest đủ 164 bài.

Mỗi manifest có `sample_id`, `dataset`, `split`, `seed`, `population_size`,
`sample_size` và `problem_ids`. Manifest APPS còn có `difficulty_by_problem_id`
để tạo nhóm Intro./Inter./Comp.

Tài liệu này mô tả hai bộ dữ liệu đang được sử dụng trong dự án:

- **APPS**: bài toán lập trình theo dạng chuẩn vào/ra hoặc gọi hàm.
- **HumanEval**: bài toán hoàn thiện hàm Python từ mô tả và chữ ký hàm.

Dự án **không sử dụng CodeContests**.

## 1. Tổng quan dữ liệu hiện có

| Dataset | Split | Số mẫu | ID |
|---|---:|---:|---|
| APPS | `train` | 5.000 | `0` đến `4999` |
| APPS | `test` | 5.000 | `0` đến `4999` |
| HumanEval | `test` | 164 | `HumanEval/0` đến `HumanEval/163` |

APPS được giữ ở cấu trúc raw mà repo RethinkMCTS gốc sử dụng. HumanEval được lưu
bằng `datasets.Dataset.save_to_disk()` ở định dạng Apache Arrow.

## 2. Cấu trúc thư mục

```text
data/
├── README.md
├── samples/
│   ├── baseline_v1/
│   │   ├── apps_test_100.json
│   │   └── humaneval_test_100.json
│   ├── evaluation_v1/
│   │   ├── apps_test_100.json
│   │   └── humaneval_test_100.json
│   └── benchmark_v2/
│       ├── apps_test_300.json
│       ├── apps_test_30_external_evaluator_pilot.json
│       └── humaneval_test_164.json
├── scripts/
│   ├── prepare_apps.py
│   ├── prepare_humaneval.py
│   └── prepare_humaneval_public_tests.py
├── apps/
│   └── raw/                        # APPS dạng thư mục mà repo gốc sử dụng
│       ├── train/
│       │   ├── 0000/
│       │   ├── 0001/
│       │   └── .../4999/
│       └── test/
│           ├── 0000/
│           ├── 0001/
│           └── .../4999/
└── humaneval/
    ├── public_tests.jsonl          # 164 bộ given_tests cho search
    ├── public_tests_source.json    # commit, URL và SHA-256 nguồn đã pin
    └── arrow/                      # HumanEval dạng Hugging Face Arrow
        ├── dataset_dict.json
        └── test/
            ├── data-00000-of-00001.arrow
            ├── dataset_info.json
            └── state.json
```

### Ý nghĩa các file do Hugging Face tạo

| File | Ý nghĩa |
|---|---|
| `dataset_dict.json` | Khai báo các split có trong `DatasetDict`. |
| `data-*.arrow` | Dữ liệu thực tế ở định dạng Apache Arrow; một split có thể gồm nhiều shard. |
| `dataset_info.json` | Schema, kiểu dữ liệu, số mẫu và metadata của dataset. |
| `state.json` | Danh sách shard cùng trạng thái cần để `load_from_disk()` khôi phục dataset. |

Không nên sửa trực tiếp các file `.arrow`, `state.json` hoặc `dataset_info.json`.

## 3. APPS

### 3.1 Nguồn và cách lưu

Script `scripts/prepare_apps.py` tải các file Parquet thuộc cấu hình `all` của
`codeparrot/apps` vào bộ nhớ, sau đó chuyển đổi trực tiếp sang `data/apps/raw`.
Đây là biểu diễn APPS duy nhất được giữ trên đĩa vì loader của repo RethinkMCTS
gốc làm việc theo cấu trúc thư mục từng bài.

### 3.2 Schema dữ liệu nguồn

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `problem_id` | `int64` | ID số của bài trong split, từ `0` đến `4999`. |
| `question` | `string` | Đề bài, mô tả input/output, ràng buộc và ví dụ nếu có. |
| `solutions` | `string` | Chuỗi JSON chứa danh sách lời giải tham khảo. Cần `json.loads()` trước khi sử dụng như danh sách. |
| `input_output` | `string` | Chuỗi JSON mô tả các test case. Cần `json.loads()` trước khi truy cập `inputs`, `outputs` hoặc `fn_name`. |
| `difficulty` | `string` | Mức độ khó: `introductory`, `interview` hoặc `competition`. |
| `url` | `string` | URL nguồn của bài toán, nếu dataset cung cấp. |
| `starter_code` | `string` | Code khởi tạo/chữ ký hàm; có thể là chuỗi rỗng. |

Lưu ý quan trọng: dù `solutions` và `input_output` chứa JSON, kiểu cột của chúng
vẫn là `string`, không phải `list` hay `dict`.

Các cột nguồn được ánh xạ sang file raw như mô tả ở mục 3.4. Ví dụ đọc một mẫu
đã chuyển đổi:

```python
import json
from pathlib import Path

problem_dir = Path("data/apps/raw/test/0000")
question = (problem_dir / "question.txt").read_text(encoding="utf-8")
solutions = json.loads((problem_dir / "solutions.json").read_text(encoding="utf-8"))
test_spec = json.loads((problem_dir / "input_output.json").read_text(encoding="utf-8"))
```

### 3.3 Schema của `input_output`

APPS có hai kiểu bài:

#### Standard input/output

Chương trình đọc từ `stdin` và ghi kết quả ra `stdout`.

```json
{
  "inputs": ["1 2\n", "10 20\n"],
  "outputs": ["3\n", "30\n"]
}
```

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `inputs` | `list` | Danh sách chuỗi đầu vào truyền qua `stdin`. |
| `outputs` | `list` | Danh sách kết quả mong đợi, cùng vị trí với `inputs`. |

#### Call-based

Executor gọi trực tiếp hàm hoặc phương thức thay vì chạy theo `stdin/stdout`.

```json
{
  "fn_name": "solve",
  "inputs": [[1, 2], [10, 20]],
  "outputs": [3, 30]
}
```

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `fn_name` | `string` | Tên hàm/phương thức cần gọi; sự hiện diện của trường này xác định bài call-based. |
| `inputs` | `list` | Danh sách bộ tham số cho từng test case. Cấu trúc phần tử phụ thuộc chữ ký hàm. |
| `outputs` | `list` | Giá trị trả về mong đợi cho từng test case. |

Không nên giả định mọi phần tử của `inputs` và `outputs` đều là chuỗi. Với bài
call-based, chúng có thể là số, chuỗi, danh sách hoặc cấu trúc JSON lồng nhau.

### 3.4 Cấu trúc APPS raw

Mỗi bài nằm trong một thư mục ID gồm bốn file bắt buộc và một file tùy chọn:

```text
0000/
├── question.txt
├── solutions.json
├── input_output.json
├── metadata.json
└── starter_code.py       # chỉ có khi starter_code không rỗng
```

| File | Bắt buộc | Nội dung | Nguồn từ cột Arrow |
|---|---:|---|---|
| `question.txt` | Có | Đề bài dạng UTF-8. | `question` |
| `solutions.json` | Có | Mảng JSON chứa các lời giải tham khảo. | `solutions` |
| `input_output.json` | Có | Object JSON chứa test case. | `input_output` |
| `metadata.json` | Có | Object JSON gồm `difficulty` và `url`. | `difficulty`, `url` |
| `starter_code.py` | Không | Code khởi tạo khi bài có cung cấp. | `starter_code` |

Ví dụ `metadata.json`:

```json
{
  "difficulty": "interview",
  "url": "https://codeforces.com/problemset/problem/1101/B"
}
```

Số lượng `starter_code.py` ít hơn số bài là bình thường:

| Split | Số bài | Có `starter_code.py` |
|---|---:|---:|
| `train` | 5.000 | 3.350 |
| `test` | 5.000 | 54 |

## 4. HumanEval

### 4.1 Nguồn và cách lưu

Script `scripts/prepare_humaneval.py` tải `openai/openai_humaneval` và lưu bằng
`save_to_disk()` tại `data/humaneval/arrow`. Dataset chỉ có split `test` gồm 164 bài.

Khác với APPS, HumanEval giữ dữ liệu gốc bằng Arrow và public tests phụ trợ
bằng JSONL; không có bản raw theo thư mục từng bài.

Bản Arrow không có cột `given_tests`. Search RethinkMCTS dùng
`public_tests.jsonl`, 164 dòng JSONL gồm `task_id`, `entry_point` và
`given_tests` (list các câu lệnh `assert`), lấy từ `processed.jsonl` của
[nhóm đối chiếu](https://github.com/Viendeptrai1/rethink-mcts-slm/blob/fabdc43ac2ae281262271aad2aadad488c76d667/data/humaneval/processed.jsonl).
Script `data/scripts/prepare_humaneval_public_tests.py` xác minh SHA-256 nguồn,
ID, prompt và entry point với Arrow cục bộ trước khi ghi; provenance lưu trong
`public_tests_source.json`. Đã kiểm tra 164/164 bài có 1-8 assertions.
Không trích `>>>` từ prompt nếu thiếu file; loader sẽ dừng. Official `test` trong
Arrow chỉ dùng sau search để chấm candidate cuối.

### 4.2 Schema

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `task_id` | `string` | ID bài, có dạng `HumanEval/0` đến `HumanEval/163`. |
| `prompt` | `string` | Phần đầu mã Python gồm chữ ký hàm, docstring và mô tả cần hoàn thiện. |
| `canonical_solution` | `string` | Phần thân hàm của lời giải tham khảo. |
| `test` | `string` | Mã Python định nghĩa test/reference check cho bài. |
| `entry_point` | `string` | Tên hàm cần được sinh và kiểm thử. |

Một chương trình tham khảo hoàn chỉnh có thể được ghép bằng:

```python
reference_program = sample["prompt"] + sample["canonical_solution"]
```

Khi đánh giá code được mô hình sinh, executor thường ghép code ứng viên với nội
dung trong `test`, sau đó gọi hàm kiểm tra bằng `entry_point`. Việc thực thi phải
được cô lập và có timeout vì trường `test` là mã Python có thể chạy.

Ví dụ đọc dataset:

```python
from datasets import load_from_disk

humaneval = load_from_disk("data/humaneval/arrow")
sample = humaneval["test"][0]

print(sample["task_id"])
print(sample["entry_point"])
print(sample["prompt"])
```

## 5. So sánh hai dataset

| Đặc điểm | APPS | HumanEval |
|---|---|---|
| Đơn vị sinh mã | Thường là chương trình hoàn chỉnh; một số bài yêu cầu hoàn thiện hàm/lớp. | Phần thân của một hàm Python. |
| Giao diện kiểm thử | `stdin/stdout` hoặc call-based. | Gọi hàm theo `entry_point`. |
| Test case | Nằm trong JSON của `input_output`. | Nằm trong mã Python của cột `test`. |
| Lời giải tham khảo | Danh sách nhiều lời giải trong `solutions`. | Một `canonical_solution`. |
| Mức độ khó | Có ba nhãn độ khó. | Không có cột độ khó. |
| Split hiện có | `train`, `test`. | Chỉ `test`. |
| Biểu diễn cục bộ | Raw theo từng bài. | Arrow. |

## 6. Kiểm tra nhanh dữ liệu cục bộ

```python
from pathlib import Path
from datasets import load_from_disk

apps_root = Path("data/apps/raw")
humaneval = load_from_disk("data/humaneval/arrow")

assert len(list((apps_root / "train").iterdir())) == 5000
assert len(list((apps_root / "test").iterdir())) == 5000
assert len(humaneval["test"]) == 164

print(humaneval)
```

Các script tải dữ liệu hiện tại sẽ bỏ qua bước ghi nếu thư mục đích đã tồn tại.
Do đó, nếu thay đổi quy trình tải hoặc chuyển đổi trong tương lai, cần kiểm tra tính
toàn vẹn thay vì chỉ dựa vào việc thư mục có tồn tại hay không.

## 7. Quy ước bảo trì tài liệu

### Public test của APPS trong MCTS

`input_output.json` không đánh dấu public/private. `rethinkmcts.runner`
chọn nửa đầu (`half`, giống repo tác giả) để search; tùy chọn `half_min2`
giữ ít nhất 2 public test nếu còn private test. Manifest `benchmark_v2`
có 85 bài với 3 test, vì vậy `half` chỉ dùng 1 public test ở những bài này.
Final evaluation dùng toàn bộ test trong file, bất kể search policy nào.
Đổi public policy phải dùng run name mới; file dữ liệu gốc không thay đổi.

Khi thêm, xóa hoặc thay đổi dataset, cần cập nhật đồng thời:

- File này (`data/README.md`): cấu trúc thực tế, schema, split, số lượng và cách load.
- `docs/datasets.md` nếu file tồn tại: phạm vi và quyết định sử dụng dataset của dự án.
- `AGENTS.md`: cây thư mục dự kiến và các ràng buộc theo giai đoạn.
- Các script, ví dụ đường dẫn và `.gitignore` có liên quan.

Sau mỗi thay đổi, cần tìm tên/đường dẫn cũ trên toàn workspace và xác minh trực tiếp
số mẫu, split, schema cùng khả năng đọc dữ liệu trước khi kết luận tài liệu đã đồng bộ.
