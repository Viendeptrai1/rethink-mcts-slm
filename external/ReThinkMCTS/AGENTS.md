# Bối cảnh dự án

Đây là dự án tiểu luận chuyên ngành: **"Cải thiện khả năng suy luận của LLM trong sinh mã nguồn
bằng Monte Carlo Tree Search với phản hồi từ kiểm thử tự động"**.

Xem chi tiết đầy đủ trong thư mục `docs/`:
- `docs/README.md` — bản đồ tài liệu và source of truth
- `docs/project-status.md` — trạng thái đã kiểm chứng và bước tiếp theo
- `docs/plan.md` — kế hoạch 15 tuần, giai đoạn hiện tại, đóng góp dự kiến
- `docs/theory-rethinkmcts.md` — lý thuyết chi tiết RethinkMCTS (paper nền tảng chính)
- `docs/theory-rap.md` — lý thuyết RAP (paper tham khảo, để so sánh)
- `docs/datasets.md` — thông tin APPS và HumanEval
- `docs/executors.md` — cách chạy/chấm code và schema báo cáo
- `docs/pipeline-direct.md` — pipeline generation trước, parallel evaluation sau
- `docs/implementation-audit.md` — đối chiếu paper với code và các điểm cần xác minh
- `docs/decisions.md` — các quyết định phạm vi/kiến trúc đã chốt
- `docs/rethinkmcts-implementation.md` — kiến trúc native và khác biệt với repo tác giả
- `docs/runbooks/rethinkmcts-smoke.md` — kiểm thử offline và smoke test native

**LUÔN đọc các file trong `docs/` trước khi thực hiện bất kỳ task nào liên quan đến thuật toán,
dataset, hoặc kế hoạch — không tự suy đoán lại từ đầu.**

Với task thông thường, đọc `docs/README.md`, `docs/project-status.md` và file chuyên đề
liên quan; không cần nạp lại mọi tài liệu nếu source of truth đã rõ.

## Giai đoạn hiện tại (quan trọng — đọc kỹ trước khi hành động)

**Đang ở bước: RETHINKMCTS MODAL BENCHMARK - HUMANEVAL DONE, APPS PAUSED.**

Benchmark tương lai đã chốt tại `data/samples/benchmark_v2/`: APPS 300 ID
(100 mỗi mức khó theo cohort nhóm đối chiếu) và HumanEval đủ 164 ID. Kết quả
baseline 100+100 thuộc `evaluation_v1` là lịch sử, không đổi nhãn hoặc ghi đè.

Mục tiêu ngay bây giờ:
1. Giữ nguyên kết quả HumanEval 164/164 của run Modal; xem
   `docs/results/rethinkmcts-modal-humaneval-v1.md`.
2. Khi người dùng yêu cầu, resume APPS 300 theo `docs/runbooks/modal-mcts.md`.
3. Chỉ đóng băng bảng benchmark khi cả APPS 300 và HumanEval 164 hoàn tất.

**Chưa làm ở giai đoạn này** (xem `docs/plan.md`):
- Không tự tiếp tục APPS khi người dùng đang tạm dừng run.
- Pilot riêng Dual + evaluator `qwen2.5-coder:14b-instruct` đã được chuẩn bị
  nhưng chưa deploy/chạy; không tự gọi Modal hoặc phát sinh chi phí. APPS pilot
  30 dùng manifest riêng và không thay thế cohort benchmark 300.
- Chưa thêm reward TLE-aware.
- Chưa thêm root-cause identification.
- Không sử dụng CodeContests trong phạm vi dự án hiện tại.

## Quy ước làm việc

- Giải thích và trao đổi bằng **tiếng Việt**. Code, tên biến, comment ngắn có thể tiếng Anh.
- Khi giải thích thuật toán, **trích đúng công thức/thuật ngữ đã ghi trong `docs/theory-*.md`**,
  không tự bịa công thức khác hoặc đổi ký hiệu.
- Khi chạy thử nghiệm với API (OpenAI/Codex), luôn giới hạn số bài + rollout thấp trước
  (để tránh tốn phí ngoài ý muốn) trừ khi được yêu cầu rõ ràng chạy full.
- LLM runtime sử dụng provider OpenAI-compatible được cấu hình từ `.env` theo
  `docs/llm-provider.md`; benchmark mới dự kiến dùng Ollama trên GPU thuê CKEY.
  Không hard-code hoặc ghi log token/secret.
- Luôn dùng Python/pip tại `D:\ReThinkMCTS\venv` theo `docs/environment.md`; không
  cài package vào môi trường global.
- Nếu phát hiện điểm nào trong `docs/` có vẻ sai/thiếu so với hành vi thực tế của code gốc,
  báo rõ ra (không tự âm thầm sửa) để cập nhật lại tài liệu.

### Đồng bộ tài liệu khi thay đổi dữ liệu

- Mọi thay đổi liên quan đến dataset đều phải cập nhật các file Markdown liên quan ngay
  trong cùng task. Thay đổi liên quan bao gồm: thêm/xóa dataset, đổi nguồn tải, đổi schema,
  đổi split hoặc số lượng mẫu, đổi định dạng lưu trữ, đổi cấu trúc thư mục và đổi tên script.
- `data/README.md` là tài liệu phản ánh cấu trúc dữ liệu thực tế trong workspace và luôn
  phải được cập nhật khi nội dung dưới `data/` thay đổi.
- `docs/datasets.md` là tài liệu cấp dự án. Nếu file này tồn tại, phải cập nhật các quyết
  định, phạm vi và thông tin dataset tương ứng; không để nó mâu thuẫn với `data/README.md`.
- Nếu thay đổi cấu trúc thư mục dữ liệu, phải cập nhật cả cây thư mục trong `AGENTS.md`,
  đường dẫn trong code/script, ví dụ lệnh chạy và `.gitignore` nếu có liên quan.
- Sau khi cập nhật, phải tìm toàn workspace để phát hiện đường dẫn hoặc tên cũ còn sót lại,
  đồng thời kiểm tra lại số lượng mẫu, split, schema và khả năng load dữ liệu.
- Không ghi vào tài liệu rằng dữ liệu đã đầy đủ hoặc hợp lệ nếu chưa kiểm tra trực tiếp.

## Cấu trúc thư mục dự kiến

```
rethinkmcts-project/
├── AGENTS.md                    (file này)
├── docs/
│   ├── README.md
│   ├── project-status.md
│   ├── plan.md
│   ├── theory-rethinkmcts.md
│   ├── theory-rap.md
│   ├── datasets.md
│   ├── baseline-direct.md
│   ├── executors.md
│   ├── pipeline-direct.md
│   ├── environment.md
│   ├── implementation-audit.md
│   ├── benchmark-results.md
│   ├── llm-provider.md
│   ├── decisions.md
│   ├── rethinkmcts-implementation.md
│   ├── gpu/
│   │   └── README.md
│   └── runbooks/
│       ├── README.md
│       ├── baseline-full.md
│       ├── benchmark-v2.md
│       ├── remote-evaluation.md
│       ├── remote-mcts.md
│       └── rethinkmcts-smoke.md
├── vendor_rethinkmcts/          (repo tác giả, pin commit để audit; không sửa)
├── rethinkmcts/                  (implementation native: tree, search, feedback, runner)
├── baselines/
│   ├── generate_apps.py
│   ├── generate_humaneval.py
│   ├── run_apps_benchmark.py
│   ├── run_humaneval_benchmark.py
│   ├── batch_generation.py
│   └── direct_generation/
│       ├── configs/
│       ├── cli.py
│       └── pipeline.py
├── Executors/
│   ├── APPSExecutor.py
│   ├── HumanevalExecutor.py
│   ├── common.py
│   └── cli.py
├── evaluation/
│   └── batch_evaluation.py
├── pipelines/
│   └── direct_baseline.py
├── data/
│   ├── README.md
│   ├── scripts/
│   │   └── prepare_humaneval_public_tests.py
│   ├── samples/
│   │   ├── baseline_v1/
│   │   │   ├── apps_test_100.json
│   │   │   └── humaneval_test_100.json
│   │   ├── evaluation_v1/
│   │   │   ├── apps_test_100.json
│   │   │   └── humaneval_test_100.json
│   │   └── benchmark_v2/
│   │       ├── apps_test_300.json
│   │       ├── apps_test_30_external_evaluator_pilot.json
│   │       └── humaneval_test_164.json
│   ├── apps/
│   │   └── raw/
│   └── humaneval/
│       ├── arrow/
│       ├── public_tests.jsonl
│       └── public_tests_source.json
├── tools/                       (smoke/check script ngoài pipeline)
│   ├── trace_viewer/            (local read-only MCTS tree/event playback)
│   ├── gpu/                     (SSH tunnel, tự pull Ollama cho direct generation)
│   ├── remote_evaluation/       (đóng gói cohort và runner Docker máy thuê)
│   └── remote_mcts/             (đóng gói, smoke, batch MCTS, thu kết quả)
└── notebooks/                   (thử nghiệm nhanh, quan sát log)
```
