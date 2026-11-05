# Chương 5. Phân tích & Thảo luận Chuyên sâu

> Bám sát các mục phân tích của bài báo gốc ([Rethink_extracted.md §6 & Appendix B](../../Rethink_extracted.md)) và 4 nghiên cứu triệt tiêu trong [Proposal.md §5.3](../../Proposal.md).

## 5.1. Hiệu ứng Mở rộng Quy mô Mô hình (Model Scaling: 7B vs 14B — RQ3)

- **Trên HumanEval-164:**
  - `Qwen2.5-Coder-7B` khi gắn RethinkMCTS Dual đạt **91.46% (150/164)**, vượt qua `Qwen2.5-Coder-14B` chạy Direct (**90.24%, 148/164**).
  - `Qwen2.5-Coder-14B` khi gắn RethinkMCTS đạt **93.29% (153/164)** chỉ với trung bình **4.55 lời gọi/bài** (ít hơn cả Best-of-3: 5.77 lời gọi/bài).
- **Trên APPS-300 (Đặc biệt ở mức độ Competition):**
  - Bài báo gốc nhận xét trên GPT-3.5 vs GPT-4o-mini rằng mô hình yếu hơn hưởng lợi nhiều hơn từ RethinkMCTS.
  - Tuy nhiên, ở phân khúc **mô hình nhỏ $\le$ 14B**, kết quả thực nghiệm chỉ ra một quy luật bổ sung quan trọng: **Ở mức độ khó Competition, mô hình 7B chạm trần kiến thức thuật toán** (Direct 4.00% $\to$ MCTS Dual 5.00% $\to$ Test-only 9.00%), trong khi **14B MCTS Dual nhảy vọt lên 28.00%** (ngang bằng con số 28% của GPT-4o-mini trong Table 1 bài báo gốc!).
  - *Cần bổ sung:* Số liệu **14B Direct trên APPS-300** ([E1](EXPERIMENT_CHECKLIST.md)) để tách biệt chính xác phần đóng góp của bản thân trọng số 14B và phần đóng góp của tìm kiếm MCTS trên 14B.

---

## 5.2. Vai trò của LLM Critic & Hiện tượng *Critic Degradation* (Ablation 1 — RQ3)

- **Bằng chứng trên 7B:** Trên APPS-300, cấu hình **Test-only (22.67%)** vượt **Dual Reward (19.00%)** tới **+3.67% Pass@1**. Ngược lại, trên HumanEval-164 (nơi chỉ có rất ít `given_tests`), 7B Dual (**91.46%**) lại cao hơn 7B Test-only (**89.63%**).
- **Giải thích gắn với lý thuyết bài báo gốc (Paper §6, trang 6):**
  - Bài báo gốc chỉ ra Dual Evaluation đặc biệt quan trọng khi số lượng public tests ít (như HumanEval).
  - Khi số lượng public tests nhiều hơn (như cấu hình `half` của 7B trên APPS), bản thân $v_{\text{test}}$ đã đủ tính phân loại; lúc này điểm tự chấm $v_{\text{llm}}$ của mô hình nhỏ 7B bị nhiễu sẽ làm lệch thứ tự chọn ứng viên.
- **Trên 14B (Cần hoàn tất [A1](EXPERIMENT_CHECKLIST.md) & [E3](EXPERIMENT_CHECKLIST.md)):**
  - Trong run 14B Dual APPS-300, `prepared/apps` chỉ cấp **2 public tests/bài**, dẫn đến **160/300 bài** có ứng viên vượt qua toàn bộ public tests và kích hoạt Critic (`self_eval_raw`).
  - **Phân tích Offline A1 (Không tốn GPU):** Trích xuất `self_eval_raw` từ 300 file `evaluations.json` để kiểm tra:
    1. Trong 160 bài gọi Critic, có bao nhiêu bài có $\ge 2$ ứng viên cùng đạt $v_{\text{test}} = 1.0$ mà điểm Critic đã giúp phân định thắng thua?
    2. Hệ số tương quan (Point-biserial / Spearman) giữa điểm `self_eval_raw` và `hidden_pass_rate` là dương hay âm?

---

## 5.3. Nghiên cứu Triệt tiêu các Thành phần Tìm kiếm (Component Ablations — RQ2)

Đối chiếu với **Figure 3 & 6, Table 4** của bài báo gốc và **Mục 5.3 của Đề cương (`Proposal.md`)**:

| Mã Ablation | Cấu hình so sánh (Full 300 bài APPS) | Nguồn trong Paper / Proposal | Trạng thái |
| :--- | :--- | :--- | :--- |
| **Ablation 1: Critic** | Dual $(0.8, 0.2)$ vs Test-only $(1.0, 0.0)$ | Paper Fig. 3 (`w/o selfEval`), Proposal §5.3 | ✅ Có trên 7B; ⏳ Full 300 bài 14B ([E3](EXPERIMENT_CHECKLIST.md)) |
| **Ablation 2: Rethink** | Có Rethink (`max_rethinks=2`) vs Không Rethink (`max_rethinks=0`) | Paper Fig. 3 (`w/o rethink`) & Table 4 | ⏳ Full 300 bài ([E4](EXPERIMENT_CHECKLIST.md)) |
| **Ablation 3: Mức Feedback** | `block` (CFG) vs `trace` (`w/o blockInfo`) vs `facts_only` | Paper Fig. 3, Proposal §5.3 (Ablation 1), RQ1 | ⏳ Full 300 bài ([E6](EXPERIMENT_CHECKLIST.md)) |
| **Ablation 4: Backup Policy** | Max Backup ($Q = \max$) vs Mean Backup (`search.backup=mean`) | Proposal §5.3 (Ablation 2) | ⏳ Full 300 bài ([E10](EXPERIMENT_CHECKLIST.md)) |

> **Chỉ số bổ sung không tốn GPU (Paper Table 4 — [A3](EXPERIMENT_CHECKLIST.md)):**
> Ngoài Pass@1 trên tập ẩn, bài báo gốc (Table 4) còn đo **tỷ lệ ứng viên mã hợp lệ trên toàn bộ cây tìm kiếm** (số candidate đạt $v_{\text{test}} = 1.0$ chia tổng số candidate sinh ra). Chỉ số này trích xuất được ngay từ `evaluations.json` của 300 bài 14B!

---

## 5.4. RethinkMCTS vs Sửa lỗi Tuần tự (Iterative Repair / Reflection — Paper Table 2)

- Trong bài báo gốc (Table 2), thay thế *Rethink* bằng *Reflection* làm giảm Pass@1 và làm tăng mạnh lượng token tiêu thụ do tích lũy lịch sử lỗi.
- Trong báo cáo của ta:
  - Chạy `--solver iterative_repair` trên toàn bộ **300 bài APPS** ([E5](EXPERIMENT_CHECKLIST.md)).
  - Đo **tỷ lệ lặp lại mã lỗi (`duplicate code_hash`)** và **tỷ lệ tụt lùi (`pass_rate regression`)** giữa các bước sửa ([A4](EXPERIMENT_CHECKLIST.md)).

---

## 5.5. Phân tích Loại Lỗi & Động học Sửa lỗi (Error Taxonomy & Repair Dynamics — [A3](EXPERIMENT_CHECKLIST.md))

Trích xuất trực tiếp từ 300 bài của `runs/benchmark_14b_batch_*` (không tốn GPU):
1. **Phân phối lỗi ở ứng viên đầu tiên (Rollout 0, trước khi Rethink):**
   - Bao nhiêu % bài pass ngay ở lần sinh đầu tiên (không cần rethink)?
   - Bao nhiêu % gặp `SyntaxError / CompilationError`, `RuntimeError`, `TimeLimitExceeded`, `WrongAnswer`?
2. **Xác suất cứu vãn thành công (Rethink Recovery Rate):**
   - Trong số các bài thất bại ở ứng viên đầu tiên nhưng kích hoạt `rethink` (trung bình 3.45 lần/bài), có bao nhiêu bài chuyển từ `Fail` $\to$ `Pass Public` và `Pass Hidden`?
   - Loại lỗi nào được CFG Block Analysis + Rethink sửa hiệu quả nhất?
3. **Hiện tượng Quá khớp Kiểm thử Công khai (Public Overfitting Gap):**
   - Trong **160/300 bài** vượt qua 100% public tests (2 test đầu) trên 14B, chỉ có **108/300 bài** vượt qua 100% hidden tests $\to$ **52 bài (32.5% số bài pass public)** bị overfit hoặc thiếu trường hợp biên ẩn! Đây là con số cực kỳ thuyết phục để bàn luận trong Chương 5.

---

## 5.6. Đường cong Mở rộng tại Thời điểm Suy luận (Test-Time Scaling Curve — Proposal Ablation 3 & Paper Fig. 5)

- **Cách dựng đường cong ngay từ dữ liệu sẵn có ([A6](EXPERIMENT_CHECKLIST.md) — Không tốn GPU!):**
  Trong mỗi bài của `runs/benchmark_14b_batch_*`, file `candidates.jsonl` và `evaluations.json` lưu thứ tự thời gian của từng ứng viên mã sinh ra ($k = 1, 2, \dots, 16$). Ta có thể vẽ đường cong **Pass@1 và Public Pass Rate theo ngân sách số lần sinh mã $k \in \{1, 2, 4, 8, 16\}$** (Any-time Performance Curve), chứng minh sự tăng trưởng ổn định khi cấp thêm ngân sách tìm kiếm!

---

## 5.7. Nghiên cứu Tình huống Điển hình (Qualitative Case Studies — Paper Appendix C.5 & C.6)

Chọn từ dữ liệu thật trong `runs/benchmark_14b_batch_*` ([A7](EXPERIMENT_CHECKLIST.md)):
1. **Case Study 1 (Thành công nhờ Block Analysis + Rethink):** 1 bài toán mà ứng viên đầu tiên bị `WrongAnswer` hoặc `IndexError`, CFG trace chỉ ra đúng biến bị sai trong vòng lặp, bước `rethink` sửa lại tư duy tại lá và ứng viên tiếp theo đạt 100% hidden tests (kèm ảnh chụp cây từ **Trace Viewer**).
2. **Case Study 2 (Thành công nhờ 14B vượt 7B ở bài Competition):** 1 bài Competition mà 7B thất bại nhưng 14B phân rã đúng thuật toán quy hoạch động / đồ thị.
3. **Case Study 3 (Thất bại điển hình — Public Overfitting):** 1 trong 52 bài pass cả 2 public tests nhưng trượt hidden test (ví dụ do TLE với input lớn hoặc thiếu corner case $N=0$), minh họa giới hạn của bộ kiểm thử công khai ít mẫu.
