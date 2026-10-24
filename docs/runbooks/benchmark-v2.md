# Benchmark v2: APPS 300 + HumanEval 164

## Pham vi

- APPS: dung dung 300 ID cua [cohort nhom doi chieu](https://github.com/Viendeptrai1/rethink-mcts-slm/blob/main/data/cohorts/apps_benchmark_300.json), 100 bai moi muc kho.
- HumanEval: dung toan bo 164 bai `HumanEval/0..163`.
- Hai manifest co dinh nam tai `data/samples/benchmark_v2/`. Khong boc lai ID
  khi doi model hoac phuong phap. Dataset raw/Arrow va candidate cu khong bi sua.
- `evaluation_v1` la run lich su 100+100; bang ket qua do khong thuoc cohort nay.
- MCTS benchmark v2 da co bao cao adjudicated; xem `docs/results/rethinkmcts-modal-benchmark-v2-adjudicated.md`.
- APPS MCTS run lịch sử dùng prompt `native_v1`. Prompt `native_v2` đã sửa
  giao diện/feedback; thử nghiệm mới phải có run name mới. `half` theo repo
  tác giả, `half_min2` chỉ là policy riêng cho cohort ít test. Xem
  `docs/implementation-audit.md` và `docs/runbooks/modal-mcts.md`.
- Direct baseline cu da sinh du 300/300 APPS va 164/164 HumanEval solution trong cohort nay. Judge all-tests da chay xong 2026-10-04; ket qua o `docs/results/benchmark-v2-all-tests.md`.

## Direct baseline tren cung cohort MCTS

Khong goi LLM. Lay code tu generation run cu va ghi ket qua vao evaluation run rieng.
APPS final evaluation cham **toan bo** input/output cases; HumanEval
dung official harness. Timeout APPS 5 giay/test, HumanEval 5 giay/harness.
Chay tren may hien tai se dung CPU cua may hien tai.

```powershell
$source = "qwen25_coder_7b_instruct_baseline_v1"
$run = "qwen25_coder_7b_instruct_baseline_benchmark_v2"
$model = "qwen2.5-coder:7b-instruct"

.\venv\Scripts\python.exe -m evaluation --dataset apps `
  --source-run-name $source --run-name $run --model $model `
  --sample-file data/samples/benchmark_v2/apps_test_300.json `
  --apps-test-policy all --timeout 5 --workers 4 --plan

.\venv\Scripts\python.exe -m evaluation --dataset humaneval `
  --source-run-name $source --run-name $run --model $model `
  --sample-file data/samples/benchmark_v2/humaneval_test_164.json `
  --timeout 5 --workers 4 --plan
```

Kiem tra plan hien dung 300 va 164 candidate, roi chay lai dung hai lenh tren:
thay `--plan` bang `--confirm-full-run`. Neu ngat, chay lai cung lenh;
`evaluation.json` moi da xong se duoc skip. Doi timeout/test policy thi phai doi
`$run` de khong tron metric. Khong dung `--no-resume` khi tiep tuc.

Sau khi ca hai dataset da cham xong:

```powershell
.\venv\Scripts\python.exe -m evaluation.benchmark_judge `
  --run-name $run --model $model
```

Bang o `outputs/baselines/evaluations/<run>/<model>/benchmark_table.md`.
File `evaluation_config.json` ghi source run, test policy, timeout va hash cohort.
Day la bang paired cohort moi; khong so truc tiep voi bang baseline 100+100 cu.
Chay lai cung lenh se resume va skip 464 report da hoan tat.

## Truoc khi chay generation cho model khac

Doc `docs/llm-provider.md` va `docs/executors.md`; kiem tra model, provider,
worker, timeout va chi phi. Dung `--run-name` **moi** de tranh ghi de evaluation
100+100 cu. Neu can sinh code, generation full khong truyen `--sample-file`;
xem `docs/runbooks/baseline-full.md` cho stage generate.

## Danh gia

APPS:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage evaluate `
  --dataset apps `
  --run-name <run_moi> `
  --model <model> `
  --sample-file data/samples/benchmark_v2/apps_test_300.json `
  --workers 4 `
  --confirm-full-run
```

HumanEval:

```powershell
.\venv\Scripts\python.exe -m pipelines `
  --stage evaluate `
  --dataset humaneval `
  --run-name <run_moi> `
  --model <model> `
  --sample-file data/samples/benchmark_v2/humaneval_test_164.json `
  --workers 4 `
  --confirm-full-run
```

Chi sau khi **ca hai** evaluation hoan tat, tao bang tong hop. Judge dung
`benchmark_v2` theo mac dinh; chi doc ket qua, khong goi LLM hay chay code:

```powershell
.\venv\Scripts\python.exe -m evaluation.benchmark_judge `
  --run-name <run_moi> `
  --model <model>
```

Ket qua o `outputs/baselines/evaluations/<run_moi>/<model>/`. Judge tinh
`missing_candidate` vao denominator; khong coi bang v2 la hoan thanh neu con
candidate thieu. Run lich su can truyen ro `--apps-sample-file` va
`--humaneval-sample-file` cua `evaluation_v1` khi tong hop lai.

Khi chạy theo [workflow remote](remote-evaluation.md), runner còn tạo hồ sơ
`outputs/benchmarks/<run_moi>/<model>/` với cấu hình/hashes và bảng kết quả
bất biến; xem [schema](../benchmark-results.md). Chạy `benchmark_judge`
riêng lẻ không tự tạo hồ sơ này nếu không có `bundle.json` và kết quả đầy đủ.

## Luu y khi so voi nhom doi chieu

Trung ID chua du de so sanh metric. [Adapter APPS cua ho](https://github.com/Viendeptrai1/rethink-mcts-slm/blob/main/src/rethink_mcts/adapters/datasets/apps.py)
dung hai test dau lam public va phan con lai lam hidden (loai duplicate public).
Pipeline hien tai cua chung ta co policy public/private rieng. Can chot cung
test split, timeout va denominator truoc khi so sanh con so giua hai project.
