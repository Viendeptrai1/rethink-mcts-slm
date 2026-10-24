# ReThinkMCTS

Đề tài: **Cải thiện khả năng suy luận của LLM trong sinh mã nguồn bằng Monte
Carlo Tree Search với phản hồi từ kiểm thử tự động**.

## Kết quả đã chạy

Ba benchmark dùng `qwen2.5-coder:7b-instruct`. APPS dùng Pass Rate và Pass@1;
HumanEval chỉ dùng Pass@1. Protocol và trường hợp thiếu
candidate được ghi trong [phần tham số](#tham-số-từng-benchmark) và báo cáo chi tiết.

### Direct-generation baseline

Cohort: APPS 100 Introductory + 100 Interview + 100 Competition; HumanEval 164.

| Nhóm | Pass Rate (%) | Pass@1 (%) |
|---|---:|---:|
| APPS Introductory | 45.84 | 31.00 |
| APPS Interview | 26.18 | 7.00 |
| APPS Competition | 19.52 | 4.00 |
| APPS Overall | 30.51 | 14.00 |
| HumanEval | N/A | 80.49 |

[Chi tiết baseline](docs/results/direct-baseline-benchmark-v2.md).

### RethinkMCTS (`dual`)

Cohort: APPS 100 Introductory + 100 Interview + 100 Competition; HumanEval 164.

| Nhóm | Pass Rate (%) | Pass@1 (%) |
|---|---:|---:|
| APPS Introductory | 56.70 | 38.00 |
| APPS Interview | 42.36 | 14.00 |
| APPS Competition | 30.07 | 5.00 |
| APPS Overall | 43.04 | 19.00 |
| HumanEval | N/A | 91.46 |

[Chi tiết APPS](docs/results/rethinkmcts-apps-native-v2-w4-retry.md) và
[HumanEval rejudge](outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_dual_humaneval_rejudge_20261006/qwen2.5-coder_7b-instruct/humaneval/benchmark_metrics.json).

### RethinkMCTS không dùng `v_llm` (`test_only`)

Cohort: APPS 100 Introductory + 100 Interview + 100 Competition; HumanEval 164.

| Nhóm | Pass Rate (%) | Pass@1 (%) |
|---|---:|---:|
| APPS Introductory | 61.14 | 41.00 |
| APPS Interview | 45.46 | 18.00 |
| APPS Competition | 29.42 | 9.00 |
| APPS Overall | 45.34 | 22.67 |
| HumanEval | N/A | 89.63 |

[Chi tiết `test_only`](docs/results/rethinkmcts-test-only-v1.md).

## Tham số từng benchmark

Các bảng dưới đây là cấu hình **đã chạy**. `max_tokens=null` trong cấu hình
MCTS không có nghĩa backend không giới hạn token.

### Direct-generation baseline

| Hạng mục | Giá trị |
|---|---|
| Cohort / model | `benchmark_v2` APPS 300 + HumanEval 164 / `qwen2.5-coder:7b-instruct` |
| Run / báo cáo | `qwen25_coder_7b_instruct_baseline_benchmark_v2_all_tests`; [chi tiết](docs/results/direct-baseline-benchmark-v2.md) |
| Nguồn code | Solution từ `qwen25_coder_7b_instruct_baseline_v1`, Ollama trên CKEY; lượt judge không gọi LLM |
| Generation | Prompt `v1`, `max_tokens=8192`, `temperature=0.2`, `top_p=0.95`; không dùng MCTS |
| Final judge | APPS: toàn bộ tests, 5 giây/test, `test_workers=1`; HumanEval: official harness, 5 giây/bài |
| Độ phủ | APPS 300/300 candidate, 42 pass; HumanEval 164/164, 132 pass |

### RethinkMCTS (`dual`)

| Hạng mục | Giá trị |
|---|---|
| Cohort / model | `benchmark_v2` APPS 300 + HumanEval 164 / `qwen2.5-coder:7b-instruct`; digest `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364` |
| Search run | `rethinkmcts_apps_interface_v2_half_w4`, Modal L40S, prompt `native_v2` |
| Search | 2 rollouts, width 3, seed 0, tối đa 2 rethink; `temperature=0.2`, `top_p=0.95`, `max_tokens=null` |
| Selection / reward | P-UCB `c_base=10`, `c=4`; dual reward `a=0.8`, `b=0.2` |
| Public tests | Nửa đầu APPS tests (`half`), 5 giây/test; tối đa 1 failed test trong feedback |
| Song song / giới hạn | 4 problem worker; tối đa 900 giây/problem |
| Final judge | Toàn bộ APPS tests, 5 giây/test, 2 CPU problem worker |
| Độ phủ | APPS 295/300 candidate, 57 pass; [lỗi và adjudication](docs/results/rethinkmcts-apps-native-v2-w4-retry.md) |
| HumanEval | Search run `rethinkmcts_qwen25_modal_v1` (`native_v1`, Modal L4), 164/164 candidate; official harness 5 giây/bài, 150 pass. Không cùng source/prompt với APPS `native_v2` |

### RethinkMCTS APPS và HumanEval (`test_only`)

| Hạng mục | Giá trị |
|---|---|
| Cohort / model | `benchmark_v2` APPS 300 + HumanEval 164 / `qwen2.5-coder:7b-instruct`; digest `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364` |
| Search runs | `rethinkmcts_apps_test_only_v1` và `rethinkmcts_humaneval_test_only_v1`; Modal L40S, prompt `native_v2` |
| Search | 2 rollouts, width 3, seed 0, tối đa 2 rethink; `temperature=0.2`, `top_p=0.95`, `max_tokens=null` |
| Selection / reward | P-UCB `c_base=10`, `c=4`; `reward=passed_public_tests/total_public_tests`, không gọi LLM self-evaluation |
| Public tests | APPS: nửa đầu tests (`half`); HumanEval: given tests; 5 giây/test |
| Song song / giới hạn | 4 problem worker, 1 APPS test worker/candidate; tối đa 900 giây/problem |
| Final judge | APPS: toàn bộ tests; HumanEval: official harness; 5 giây/test, 2 CPU problem worker |
| Độ phủ | APPS 297/300, pass hết 68; HumanEval 164/164, pass 147 |
| Lỗi và provenance | [Báo cáo `test_only`](docs/results/rethinkmcts-test-only-v1.md) |

Baseline và MCTS khác prompt, môi trường và ngân sách request; hai run MCTS
APPS cũng khác độ phủ candidate. Không quy chênh lệch kết quả riêng cho thuật
toán hoặc việc bỏ `v_llm`. Chi tiết từng bài nằm trong
`outputs/rethinkmcts/<run>/<model>/<dataset>/<problem_id>/search_summary.json`.

## Bắt đầu đọc

1. [docs/project-status.md](docs/project-status.md): trạng thái đã kiểm chứng và bước tiếp theo.
2. [docs/README.md](docs/README.md): bản đồ tài liệu và source of truth.
3. [docs/runbooks/baseline-full.md](docs/runbooks/baseline-full.md): các lệnh vận hành benchmark.
4. [docs/datasets.md](docs/datasets.md): phạm vi và quyết định về APPS/HumanEval.
5. [docs/theory-rethinkmcts.md](docs/theory-rethinkmcts.md): thuật toán nền tảng từ paper.
6. [rethinkmcts/README.md](rethinkmcts/README.md): thuật toán native từng bước, chi phí mỗi node và điểm khác paper.
7. [docs/rethinkmcts-implementation.md](docs/rethinkmcts-implementation.md): kiến trúc native, artifact và khác biệt với repo tác giả.
8. [docs/runbooks/rethinkmcts-smoke.md](docs/runbooks/rethinkmcts-smoke.md): kiểm thử offline và lệnh smoke test.
9. [docs/runbooks/benchmark-v2.md](docs/runbooks/benchmark-v2.md): danh sách cohort mới và lệnh đánh giá 300+164.
10. [docs/runbooks/remote-evaluation.md](docs/runbooks/remote-evaluation.md): đóng gói và chấm trên máy GPU thuê.
11. [docs/benchmark-results.md](docs/benchmark-results.md): nơi lưu bảng và tham số của từng run.
12. [docs/runbooks/gpu-generation.md](docs/runbooks/gpu-generation.md): tự kéo model Ollama trên GPU thuê trước generation, không mở API public.
13. [docs/runbooks/remote-mcts.md](docs/runbooks/remote-mcts.md): plan, bundle,
    smoke, resume và thu bảng RethinkMCTS trên máy thuê.
14. [docs/runbooks/modal-mcts.md](docs/runbooks/modal-mcts.md): dùng Modal GPU
    cho mọi request LLM, giữ chấm bài và artifact trên laptop.
15. [docs/results/rethinkmcts-apps-native-v2-w4-retry.md](docs/results/rethinkmcts-apps-native-v2-w4-retry.md): báo cáo APPS của run MCTS hiện hành.
16. [docs/runbooks/rethinkmcts-test-only-ablation.md](docs/runbooks/rethinkmcts-test-only-ablation.md): chạy ablation bỏ LLM self-evaluation khỏi reward, rồi chấm all-tests.

## Kiến trúc thư mục

```text
D:\ReThinkMCTS\
├── README.md                 # Điểm vào duy nhất của project
├── AGENTS.md                 # Quy ước cộng tác và ràng buộc giai đoạn
├── requirements.txt          # Dependency Python
├── .env.example              # Mẫu cấu hình, không chứa secret
│
├── docs/                     # Kiến thức dự án, lý thuyết, quyết định, runbook
├── RelativeWork/             # Paper tham khảo, gồm 2409.09584v2.pdf
├── data/                     # Dataset cục bộ và sample manifest cố định
│   ├── apps/raw/             # APPS train/test theo thư mục từng bài
│   ├── humaneval/arrow/      # HumanEval test ở định dạng Arrow
│   ├── humaneval/public_tests.jsonl  # Given tests cho MCTS search
│   ├── samples/              # Manifest sample, không bốc lại khi chạy lại
│   └── scripts/              # Script chuẩn bị dữ liệu
│
├── baselines/                # Sinh code direct và config prompt/model
├── pipelines/                # Điều phối generate/evaluate
├── Executors/                # Chạy candidate và tạo ExecutionReport
├── evaluation/               # Batch evaluation và benchmark judge
├── ChatModels/               # Adapter Ollama/Modal OpenAI-compatible
├── DataProcess/              # Loader đề bài, không đọc solution khi generate
├── vendor_rethinkmcts/       # Repo tác giả, pin commit để audit, không sửa
├── rethinkmcts/              # Native implementation của tree/search/reward
├── Models/                   # Reserved cho model/MCTS cũ
├── tests/                    # Unit test offline
├── tools/                    # Smoke/check script không thuộc pipeline chính
│
└── outputs/                  # Artifact sinh tự động, không sửa thủ công
    ├── baselines/
    │   ├── direct_generation/
    │   ├── batch_manifests/
    │   ├── evaluations/
    │   └── pipeline_logs/
    ├── rethinkmcts/           # Search artifacts theo run/model/dataset/problem
    ├── rethinkmcts_attempts/  # Attempt lỗi/timeout, không mất khi resume
    ├── remote_mcts/           # ZIP deployment/checkpoint/results
    └── benchmarks/            # Bảng và provenance khi đủ cohort
```

Quy ước quan trọng:

- `data/` là input; không sửa trực tiếp file raw hoặc Arrow.
- `data/samples/benchmark_v2/` là cohort chung cho các model và MCTS sau này.
- `outputs/` là output; mỗi run được tách theo `run/model/dataset`.
- Không dùng CodeContests trong phạm vi hiện tại.
- Native search không ghi artifact vào `outputs/baselines/`; hai namespace được tách độc lập.

## Môi trường

Luôn dùng virtual environment của project:

```powershell
cd D:\ReThinkMCTS
.\venv\Scripts\python.exe --version
```

Cài dependency nếu cần:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Provider, endpoint và model được lấy từ `.env`. Không commit `.env` và không ghi
secret vào log. Chi tiết xem [docs/llm-provider.md](docs/llm-provider.md).

## Workflow benchmark

### 1. Kiểm tra kế hoạch, không gọi LLM

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage generate `
  --dataset apps `
  --run-name <run_name> `
  --config baselines/direct_generation/configs/qwen25_coder_7b_instruct.json `
  --plan
```

### 2. Sinh code toàn bộ dataset

Generation full không dùng sample judge. Resume mặc định bỏ qua artifact đã hoàn chỉnh:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage generate `
  --dataset all `
  --run-name <run_name> `
  --config baselines/direct_generation/configs/qwen25_coder_7b_instruct.json `
  --generation-workers 1 `
  --delay 1 `
  --confirm-full-run
```

### 3. Đánh giá cohort cố định cho run mới

Dùng run name mới cho cohort 300+164. Generation vẫn sinh full, còn evaluation chọn theo
hai manifest dưới đây. Bảng APPS ở đầu README đã dùng cohort `benchmark_v2`.

APPS:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage evaluate `
  --dataset apps `
  --run-name <run_name> `
  --model <model> `
  --sample-file data/samples/benchmark_v2/apps_test_300.json `
  --workers 8 `
  --test-workers 4 `
  --evaluation-timeout 300 `
  --confirm-full-run
```

HumanEval:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage evaluate `
  --dataset humaneval `
  --run-name <run_name> `
  --model <model> `
  --sample-file data/samples/benchmark_v2/humaneval_test_164.json `
  --workers 8 `
  --evaluation-timeout 300 `
  --confirm-full-run
```

`--workers` chạy nhiều bài đồng thời. `--test-workers` chỉ áp dụng cho APPS và
chạy các test độc lập trong một bài đồng thời. Không chạy hai evaluator cùng lúc
trên một run/model vì chúng ghi chung artifact evaluation.

### 4. Tạo bảng benchmark

Chỉ chạy sau khi cả hai dataset đã có `results.jsonl` và `summary.json`:

```powershell
.\venv\Scripts\python.exe -m evaluation.benchmark_judge `
  --run-name <run_name> `
  --model <model>
```

### 5. Kiểm thử native RethinkMCTS offline

Lệnh dưới đây chỉ chạy fake LLM/executor trong unit test, không gọi provider:

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

Xem kế hoạch search của một bài mà không khởi tạo client:

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

Smoke provider thật chỉ được chạy sau khi duyệt output offline; xem
[docs/runbooks/rethinkmcts-smoke.md](docs/runbooks/rethinkmcts-smoke.md).

## Đọc kết quả

Kết quả chấm gốc nằm dưới `outputs/baselines/evaluations/<run>/<model>/`.
Với benchmark mới 300 APPS + 164 HumanEval, bảng đã khóa cùng tham số chạy,
cohort, hash dữ liệu/code và chỉ mục candidate nằm tại
`outputs/benchmarks/<run>/<model>/` (`run.json`, `candidates.csv`,
`benchmark_table.md`). Bảng đối chiếu nhiều run nằm trong
`outputs/benchmarks/comparisons/<name>/`; xem
[docs/benchmark-results.md](docs/benchmark-results.md).

```text
outputs/baselines/evaluations/<run>/<model>/
├── benchmark_table.md       # Bảng paper-style, dễ đọc
├── benchmark_table.csv      # Bảng để phân tích tiếp
├── benchmark_summary.json   # Metric + manifest + missing candidates
├── apps/
│   ├── results.csv/jsonl
│   ├── failures.csv/jsonl
│   ├── passed.jsonl
│   ├── summary.json
│   └── evaluation.log
└── humaneval/
    ├── results.csv/jsonl
    ├── failures.csv/jsonl
    ├── passed.jsonl
    ├── summary.json
    └── evaluation.log
```

Chi tiết expected/actual, lỗi runtime, timeout và test index nằm trong
`evaluation.json` cạnh artifact candidate:

```text
outputs/baselines/direct_generation/<run>/<model>/<dataset>/<problem_timestamp>/
├── solution.py
├── response.txt
├── metadata.json
├── problem.txt
└── evaluation.json
```

## Kiểm thử codebase

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Tài liệu tiếp theo

- [docs/executors.md](docs/executors.md): executor, timeout và schema report.
- [docs/pipeline-direct.md](docs/pipeline-direct.md): generate/evaluate song song.
- [docs/environment.md](docs/environment.md): Python environment.
- [docs/gpu/README.md](docs/gpu/README.md): GPU CKEY và Ollama.
- [docs/decisions.md](docs/decisions.md): các quyết định kiến trúc đã chốt.
- [docs/implementation-audit.md](docs/implementation-audit.md): phần paper/code còn cần đối chiếu.
- [docs/rethinkmcts-implementation.md](docs/rethinkmcts-implementation.md): native search và artifact.
