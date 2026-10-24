# Repair APPS 1684 va 3702

Kiem tra ngay 2026-10-05. Day la hai repair run rieng, khong ghi de run
`rethinkmcts_apps_interface_v2_half_w4` goc (295/300 candidate).

## Nguyen nhan

Ca hai attempt goc deu fail sau khi model sinh Python sai cu phap. APPS
executor da tra ve loi, nhung `collect_trace()` lai goi `ast.parse(source)`
tren cung source khong hop le. `1684` nem `SyntaxError: unmatched ']'`;
`3702` nem `IndentationError: unexpected indent`. Exception thoat khoi
LangGraph search, nen khong co `search_summary.json` va `final_solution.py`.

## Sua va kiem thu

- `rethinkmcts/feedback/trace.py` gio bat `SyntaxError` (gom ca
  `IndentationError`) va tra `TraceResult(status="syntax_error", error=...)`
  de verbal feedback/Rethink xu ly, khong lam crash ca search.
- Batch/Modal wrapper co `--problem-ids` de chon ID trong cohort da khoa;
  khong can chay lai 295 bai da co.
- APPS search co `--apps-test-workers` (mac dinh 1) de cham cac test cua
  mot candidate song song. `3702` co 52 public test, nen dung 2 test worker
  va gioi han tong 1.800 giay o run rieng; van cham cung tap test va cung
  timeout 5 giay/test.
- 85/85 unit test pass. Khong sua solution da sinh trong run goc.

## Ket qua that

| ID | Repair search run | Source SHA256 | Search | All-tests final judge |
|---|---|---|---|---|
| `1684` | `rethinkmcts_apps_ast_repair_v1` | `f94d14511156299a054fd819e3d30433978e17dc68c187fcc62563ac9abb285d` | 1 test worker, 900 giay, completed | 6/13, wrong answer |
| `3702` | `rethinkmcts_apps_3702_parallel_tests_v1` | `063b4b6b100d946a623dd18e6f5949e0d79785f414b92780f30601328c40a127` | 2 test worker, 1.800 giay, completed | 0/104, timeout |

Ca hai run dung model `qwen2.5-coder:7b-instruct`, digest
`dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`,
public policy `half`, 2 rollouts, width 3 va Modal L40S. Final judge dung
toan bo APPS tests voi 5 giay/test. Report nam tai:

- `outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_apps_ast_repair_v1_all_tests/qwen2.5-coder_7b-instruct/apps/`
- `outputs/rethinkmcts_evaluations/evaluations/rethinkmcts_apps_3702_parallel_tests_v1_all_tests/qwen2.5-coder_7b-instruct/apps/`

Neu **ghep de quan sat** 295 report goc voi hai repair report (khong trung ID),
do phu la 297/300; APPS overall macro Pass Rate 43,20%, Pass@1 19,00%.
Con `1033`, `1634`, `3698` chua co candidate va dong gop 0. Day **khong
phai benchmark dong nhat source/config**: `1684` dung source sau fix AST,
`3702` dung them parallel test va timeout tong dai hon. Bang chinh cua run
goc van la 295/300 o [bao cao sau retry](rethinkmcts-apps-native-v2-w4-retry.md).
