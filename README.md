# Cải thiện khả năng suy luận của LLM trong sinh mã nguồn bằng MCTS với phản hồi từ kiểm thử tự động

Dự án nghiên cứu Tiểu luận Chuyên ngành / Luận văn Tốt nghiệp: Kết hợp tìm kiếm cây tư duy (RethinkMCTS), Học hành trình (Journey Learning) và Học tăng cường từ phản hồi kiểm chứng (GRPO) trên mô hình phân khúc $\le$ 14B.

---

## 1. Cấu trúc Dự án

```text
TLCN/
├── Proposal.md                     # Đề cương nghiên cứu chi tiết đã thống nhất
├── Agentic_AI.md                   # Cơ sở lý thuyết Agentic AI & RL (Ch. 7, 12, 13)
├── RAP.pdf                         # Paper tham khảo: Reasoning via Planning (MCTS + World Model)
├── Rethink.pdf                     # Paper tham khảo: RethinkMCTS (Thought search + Rethink)
│
├── configs/
│   └── config.yaml                 # Cấu hình MCTS (rollouts, c_base, c, timeout, rewards)
│
├── data/
│   ├── schemas.py                  # Pydantic models (Problem, TestCase, ExecutionResult)
│   └── loader.py                   # Data loader hỗ trợ deepmind/code_contests & bài mẫu offline
│
├── sandbox/
│   ├── executor.py                 # Subprocess runner an toàn (stdin/stdout, timeout=2.0s, AC/WA/TLE/RE)
│   └── analyzer.py                 # Trích xuất verbal feedback chẩn đoán lỗi cho Rethink
│
├── models/
│   ├── modal_vllm.py               # Kịch bản triển khai vLLM Server trên GPU bằng Modal Labs
│   └── client.py                   # OpenAI-compatible API client & Mock client cho kiểm thử
│
├── mcts/
│   ├── node.py                     # Cấu trúc MCTSNode & công thức tính điểm P-UCB
│   ├── rethink.py                  # Cơ chế Rethink tinh chỉnh nút tư duy lỗi tại nút lá
│   └── search.py                   # Động cơ RethinkMCTSEngine (Selection, Expansion, Evaluation, Backprop)
│
├── scripts/
│   ├── test_sandbox.py             # Unit tests kiểm tra toàn bộ tính năng của sandbox
│   └── run_mvp.py                  # Kịch bản chạy thử nghiệm end-to-end MVP
│
├── requirements.txt
└── README.md
```

---

## 2. Hướng dẫn Cài đặt & Chạy Thử nghiệm (Quickstart)

### Bước 1: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 2: Chạy kiểm thử đơn vị cho Sandbox
Xác nhận bộ thực thi Python an toàn bắt đúng các mã lỗi `AC`, `WA`, `TLE`, `RE`:
```bash
python3 scripts/test_sandbox.py
```

### Bước 3: Chạy thử nghiệm MVP ngoại tuyến (Offline Demonstration)
Chạy thuật toán RethinkMCTS trên bài toán mẫu Competitive Programming (Codeforces 4A - Watermelon) với `MockLLMClient` để quan sát cơ chế tự sửa sai:
```bash
python3 scripts/run_mvp.py
```
*Bạn sẽ quan sát thấy:*
1. Lượt 1: Mô hình đưa ra tư duy ngây thơ (`w % 2 == 0`) $\to$ Thất bại ở test case $w=2$.
2. Cơ chế **Rethink** được kích hoạt: phân tích lỗi và thay thế nút tư duy tại chỗ (`w % 2 == 0 and w > 2`).
3. Sinh lại mã mới $\to$ Vượt qua 100% test công khai và 100% test ẩn (*Private Tests*).

---

## 3. Triển khai Mô hình trên Cloud GPU bằng Modal Labs

Hệ thống được thiết kế sẵn kịch bản phục vụ mô hình `Qwen/Qwen2.5-Coder-7B-Instruct` qua vLLM Server trên Modal:

### 1. Đăng nhập Modal (nếu chưa cấu hình)
```bash
modal setup
```

### 2. Triển khai vLLM Server
```bash
# Chạy ở chế độ tạm thời để kiểm thử
modal serve models/modal_vllm.py

# Hoặc triển khai cố định (Production endpoint)
modal deploy models/modal_vllm.py
```

Sau khi deploy thành công, Modal sẽ cấp cho bạn một đường dẫn URL HTTPS (ví dụ: `https://<workspace>--qwen-coder-vllm-serve.modal.run`).

### 3. Chạy MCTS với vLLM trên Modal
```bash
python3 scripts/run_mvp.py \
    --use-modal \
    --api-base "https://<workspace>--qwen-coder-vllm-serve.modal.run/v1" \
    --model-name "Qwen/Qwen2.5-Coder-7B-Instruct" \
    --rollouts 4
```

---

## 4. Sử dụng Dataset `deepmind/code_contests`

Để tải và chạy thử nghiệm trực tiếp trên bài toán từ bộ dữ liệu `deepmind/code_contests` (Google DeepMind):
```bash
python3 scripts/run_mvp.py --from-dataset
```
*Lưu ý:* Hệ thống sử dụng chế độ `streaming=True` qua HuggingFace Datasets để nạp nhanh bài toán mà không cần tải trước toàn bộ 13,328 bài tập.
