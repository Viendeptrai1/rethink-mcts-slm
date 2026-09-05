# RethinkMCTS: Tối ưu hoá Suy Luận và Tự Chỉnh Sửa Mã Nguồn bằng Monte Carlo Tree Search cho Mô Hình Nhỏ (7B–14B)

Dự án nghiên cứu Tiểu luận Chuyên ngành / Luận văn Tốt nghiệp: Triển khai thuật toán **RethinkMCTS** (*arXiv:2409.09584v2*) với kiến trúc **Modular Monolith + Ports & Adapters**, tối ưu hóa và tinh chỉnh cho phân khúc mô hình nhỏ ($\le$ 14B như `Qwen2.5-Coder-7B/14B-Instruct`).

Tài liệu đặc tả kỹ thuật chi tiết: [docs/rethinkmcts_small_model_spec.md](docs/rethinkmcts_small_model_spec.md).

---

## 1. Cấu trúc Dự án

```text
TLCN/
├── docs/
│   └── rethinkmcts_small_model_spec.md   # Bản đặc tả kỹ thuật chuẩn và kế hoạch di trú
├── configs/
│   ├── smoke_mock.yaml                   # Cấu hình kiểm thử nhanh không phụ thuộc GPU
│   ├── ollama_7b.yaml                    # Cấu hình phục vụ Ollama Qwen2.5-Coder-7B cục bộ
│   ├── remote_14b.yaml                   # Cấu hình phục vụ Remote Endpoint 14B (vLLM/Modal)
│   └── paper_reference.yaml              # Cấu hình đối chiếu bài báo gốc (APPS/HumanEval)
│
├── src/rethink_mcts/                     # Kiến trúc Core mới (Modular Monolith + Ports/Adapters)
│   ├── domain/                           # Thực thể bất biến: Problem, Candidate, Tree, Feedback, Budget
│   ├── ports/                            # Abstractions: Models, Execution, Datasets, Storage
│   ├── application/                      # Use Cases: SearchEngine, CandidateEvaluator, FeedbackService, Judge, Baselines
│   ├── policies/                         # Thuật toán: PUCBSelector, MaxBackup, PriorPolicy, DualReward, FinalSelection
│   ├── adapters/                         # Implementations:
│   │   ├── llm/                          # HttpModelGateway, SemanticPromptedLLM, ScenarioMockLLM, Parsing
│   │   ├── execution/                    # TrustedFixtureExecutor, DockerExecutor, Bytecode CFG, Tracing
│   │   ├── datasets/                     # CodeContests, APPS, HumanEval, JSONL
│   │   └── storage/                      # FileSystemRunStore, EvaluationCache
│   ├── config.py                         # Pydantic v2 strict configuration & validation
│   ├── bootstrap.py                      # Factory kết nối toàn bộ dependency injection
│   └── cli.py                            # Giao diện dòng lệnh chính thức: `rethink <subcommand>`
│
├── prompts/
│   └── compact_v1/                       # Jinja2 prompt templates tối ưu cho mô hình 7B-14B
│
├── tests/
│   ├── unit/                             # U01–U18: Kiểm tra toán P-UCB, Q=max, Dual Reward, Parsers
│   ├── contracts/                        # I01–I24: Kiểm tra CFG, Tracing, Leaf Revision, Anti-Leakage
│   ├── acceptance/                       # Scenarios A, B, C, D (Watermelon, Anti-Oracle, Swap, Resume)
│   └── fixtures/                         # Fixtures tách biệt public và hidden
│
├── deploy/
│   └── sandbox/Dockerfile                # Docker worker cô lập (rethink-worker:py311)
├── pyproject.toml                        # Cấu hình đóng gói Python chuẩn
└── README.md
```

---

## 2. Cài đặt & Chuẩn bị Môi trường

Cài đặt package ở chế độ phát triển (editable mode):
```bash
pip install -e .
```

---

## 3. Chạy Kiểm Thử Tự Động (Test Suite)

Chạy toàn bộ 34 bài kiểm thử đơn vị, hợp đồng và kịch bản nghiệm thu:
```bash
pytest -v
```

Hoặc chạy theo từng nhóm kiểm thử:
```bash
# Kiểm tra công thức toán học P-UCB, Q=max, Dual Reward (U01-U18)
pytest tests/unit -v

# Kiểm tra hợp đồng CFG, Tracing và chống rò rỉ dữ liệu (I01-I24)
pytest tests/contracts -v

# Kiểm tra các kịch bản nghiệm thu end-to-end (Scenario A-D)
pytest tests/acceptance -v
```

---

## 4. Hướng dẫn Sử dụng CLI (`rethink`)

Hệ thống cung cấp công cụ dòng lệnh `rethink` với các lệnh sau:

### 1. Kiểm tra cấu hình và môi trường (`doctor`)
Kiểm tra tính hợp lệ của file cấu hình YAML, kết nối endpoint và trình thực thi sandbox:
```bash
rethink doctor --config configs/smoke_mock.yaml
rethink doctor --config configs/ollama_7b.yaml
```

### 2. Tìm kiếm lời giải cho bài toán (`solve`)
Chạy thuật toán RethinkMCTS trên bài toán công khai:
```bash
# Chạy demo ngoại tuyến với Scenario Mock
rethink solve \
  --config configs/smoke_mock.yaml \
  --problem tests/fixtures/watermelon_public.json \
  --output-dir runs/demo_watermelon

# Chạy với Ollama Qwen2.5-Coder-7B cục bộ
rethink solve \
  --config configs/ollama_7b.yaml \
  --problem tests/fixtures/watermelon_public.json \
  --output-dir runs/ollama_run

# Chạy với Endpoint Remote (vLLM / Modal / Cloud GPU)
rethink solve \
  --config configs/remote_14b.yaml \
  --endpoint "https://<your-remote-endpoint>/v1" \
  --model "Qwen/Qwen2.5-Coder-14B-Instruct" \
  --problem tests/fixtures/watermelon_public.json \
  --output-dir runs/remote_run
```

### 3. Đánh giá lời giải độc lập trên tập test ẩn (`judge`)
Chấm điểm lời giải đã được đóng băng sau quá trình tìm kiếm với tập test ẩn:
```bash
rethink judge \
  --run runs/demo_watermelon \
  --hidden tests/fixtures/watermelon_hidden.json
```

### 4. Xuất báo cáo thực nghiệm (`report`)
Tổng hợp kết quả Pass@1, pass rate, lượng token tiêu thụ và thời gian chạy thành `summary.json` và `summary.md`:
```bash
rethink report --run runs/demo_watermelon
```
