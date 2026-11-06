# Checklist Thực nghiệm & Phân tích Toàn diện (Chuẩn hóa Full 300 bài APPS & 164 bài HumanEval)

> **Quyết định thiết kế thực nghiệm:** Toàn bộ các phép so sánh Baseline và Ablation trên APPS đều chạy trên **trọn vẹn 300 bài chuẩn hóa (`data/cohorts/apps_benchmark_300.json` — chia 10 batch $\times$ 30 bài tại `data/batches/batch_01..10.json`)** thông qua `scripts/run_benchmark_batch.py` và gom kết quả bằng `scripts/merge_apps_batches.py`. Không dùng tập con 60 bài để đảm bảo mọi bảng số liệu trong báo cáo đều đồng nhất tuyệt đối trên mẫu số **300/300 bài**.

Ký hiệu:
- `[x]` Đã hoàn thành · `[ ]` Chưa làm
- `🧮` **Phân tích Offline trên dữ liệu sẵn có trong máy (0 tốn GPU)**
- `⏳` **Cần gọi LLM / chạy GPU (Full 300 bài APPS hoặc 164 bài HumanEval)**

---

## I. Những hạng mục ĐÃ CÓ SẴN (Không cần chạy lại)

- [x] **7B APPS-300 (`seed=2027`):** Direct (`14.00%`), MCTS Dual (`19.00%`), MCTS Test-only (`22.67%`) — [docs/results/7b/](../results/7b/)
- [x] **7B HumanEval-164:** Direct (`80.49%`), MCTS Test-only (`89.63%`), MCTS Dual (`91.46%`)
- [x] **14B APPS-300 (`seed=2027`):** MCTS Dual (`36.00%`, 108/300 bài) — `runs/benchmark_apps_14b_dual_unified/`
- [x] **14B HumanEval-164:** Direct (`90.24%`), Best-of-3 (`91.46%`), MCTS Test-only (`93.29%`) — `runs/humaneval_*_14b/`
- [x] **Bảng phân rã Token & Model Calls theo 5 vai trò trên 14B APPS-300:** Đã trích xuất xong tại [Chương 4 §4.4](04_ket_qua_thuc_nghiem.md).

---

## II. Nhóm A — Phân tích Offline làm được NGAY (🧮 0 tốn GPU)

- [x] **A1. 🧮 Phân tích sâu LLM Critic trên 14B APPS-300 (Paper Table 3 & RQ3):**
  - Đã tính trên 161 lượt gọi Critic của 14B: Pearson $r = +0.170$ ($p = 0.031$), Spearman $\rho = +0.243$ ($p = 0.0019$), Point-biserial $r = +0.239$ ($p = 0.0023$). Bắt đúng 22 bài overfit. Chi tiết tại [Chương 5 §5.2](05_phan_tich_thao_luan.md).
- [x] **A2. 🧮 Kiểm định Ý nghĩa Thống kê (McNemar's Test & Bootstrap 95% CI):**
  - Đã tính cho cặp **14B MCTS Dual vs 14B Direct trên Full APPS-300**: $\chi^2 = 18.4808, p = 1.72 \times 10^{-5}$, Bootstrap 95% CI: Direct $[20.67\%, 30.33\%]$ vs MCTS $[30.67\%, 41.67\%]$, $\Delta = +10.67\%$ (95% CI: $[3.67\%, 18.00\%]$). MCTS cứu được 42 bài Direct sai. Còn cặp HumanEval và 7B APPS.
- [x] **A3. 🧮 Phân loại Lỗi, Tỷ lệ Cứu vãn nhờ Rethink & Tỷ lệ Code Hợp lệ trên Cây (Paper Table 4):**
  - Đã trích xuất xong từ 300 bài 14B: 216 bài kích hoạt Rethink; cứu thành công 77 bài pass public (35.6%) và **38 bài pass hidden (17.6%)**; đóng góp 35.2% tổng số bài giải đúng của 14B. Tree Effective Code Rate = **9.21%** (161/1,748 code). Lỗi lần đầu: 85.2% WA, 13.9% RE, 0.9% TLE, 0% CE. Chi tiết tại [Chương 5 §5.5](05_phan_tich_thao_luan.md).
- [ ] **A5. 🧮 Đồng bộ Kết quả Theo Bài & Chi phí của Nhánh 7B:**
  - Lấy kết quả chi tiết từng bài của 7B để chạy kiểm định cặp McNemar trên 300 bài APPS.
- [x] **A6. 🧮 Đường cong Mở rộng theo Ngân sách (Test-Time Scaling Curve — Proposal Ablation 3 & Paper Fig. 5):**
  - Đã dựng xong đường cong Pass@1 theo $k \in \{1, 2, 4, 8, 16\}$ trên 300 bài 14B: $k=1$ (22.00%) $\to$ $k=2$ (26.67%) $\to$ $k=4$ (31.33%) $\to$ $k=8$ (35.00%) $\to$ $k=16$ (36.00%). Tăng trưởng đơn điệu hàm logarit. Chi tiết tại [Chương 5 §5.6](05_phan_tich_thao_luan.md).
- [ ] **A7. 🧮 Trích xuất 3 Case Studies Điển hình & Ví dụ Trace (Paper Table 13 & 14):**
  - Xuất 2 bài thành công nhờ `block_analysis` + `rethink` và 1 bài thất bại do overfit public tests để đưa vào Chương 2 & Chương 5.7.
- [x] **A8. 🧮 Thí nghiệm Đối đầu Self-Critic (Qwen2.5-Coder-14B) vs Cross-Critic (Mistral Codestral):**
  - Đã chạy thẩm định chéo trên toàn bộ 161 ứng viên mã đạt $v_{\text{test}} = 1.0$ của APPS-300 bằng mô hình `codestral-latest`.
  - Kết quả: Self-Critic ($\rho = +0.243, p = 0.0019$) vượt trội hoàn toàn so với Cross-Critic Codestral ($\rho = +0.033, p = 0.68$). Codestral bị bão hòa trần 90.1% và bỏ sót 95.16% bài overfit. Chi tiết tại [Chương 5 §5.2.2](05_phan_tich_thao_luan.md). Nguồn: `runs/cross_critic_analysis_14b/`.

---

## III. Nhóm S — Chuẩn bị Kỹ thuật trước khi chạy 10-GPU Batch

- [ ] **S1. Đồng bộ `prompts.bundle: native_v2` trong `configs/benchmark_apps_14b_test_only.yaml`:**
  - Đổi `bundle: compact_v1` thành `bundle: native_v2` để đồng nhất 100% với `configs/batches/batch_01..10.yaml`.
- [ ] **S2. Khởi động các Endpoint vLLM 14B trên Modal:**
  - Dùng `bash scripts/deploy_10gpu.sh` (hoặc số lượng endpoint tương ứng) và kiểm tra kết nối trước khi chạy.
- [ ] **S3. Kiểm tra bằng `--dry-run`:**
  - `scripts/run_benchmark_batch.py` đã hỗ trợ đọc trực tiếp `@data/cohorts/apps_benchmark_300.json` hoặc từng batch `@data/batches/batch_01.json`..`batch_10.json`.

---

## IV. Nhóm E — Các Đợt Chạy Full 300 Bài APPS & 164 Bài HumanEval trên GPU (⏳)

Với kiến trúc **10 GPU song song** (30 bài/batch tại `configs/batches/batch_01..10.yaml`), thời gian chạy thực tế cho cả 300 bài rất ngắn:

### 🔴 Ưu tiên 1: Hoàn thiện Bảng So sánh Chính (Main Results — Bảng 4.1 & 4.2)

- [x] **E1. ⏳ 14B Direct Baseline trên Full APPS-300 (300 bài) — ĐÃ HOÀN TẤT:**
  - **Kết quả:** Pass@1 = **25.33%** (76/300), Mean Hidden Pass Rate = **38.41%**. Intro: 42.00%, Inter: 13.00%, Comp: 21.00%. Tổng 380 calls, 411,815 tokens.
  - **So sánh với MCTS Dual (36.00%):** $\Delta = +10.67\%$ (McNemar $\chi^2 = 18.48, p = 1.72 \times 10^{-5} \ll 0.001$, Bootstrap 95% CI: $[3.67\%, 18.00\%]$).
  - **Artifact:** `runs/benchmark_apps_14b_direct_300/summary.json`

- [ ] **E2. ⏳ 14B Best-of-3 (`--solver best_of_n --samples-n 3`) trên Full APPS-300 (300 bài, ~10–15 phút trên 10 GPU):**
  - **Mục đích:** Chứng minh trên cả 300 bài APPS rằng tìm kiếm có hướng dẫn (RethinkMCTS) vượt xa việc lấy mẫu ngẫu nhiên độc lập nhiều lần.
  - **Lệnh chạy (cho từng batch `01..10` rồi merge bằng `scripts/merge_apps_batches.py`):**
    ```bash
    python3 scripts/run_benchmark_batch.py \
      --config configs/batches/batch_01.yaml \
      --dataset apps \
      --solver best_of_n --samples-n 3 \
      --output-dir runs/bon3_14b_batch_01 \
      --problem-ids @data/batches/batch_01.json
    ```

- [ ] **E5. ⏳ 14B Iterative Repair (`--solver iterative_repair`) trên Full APPS-300 (300 bài, kèm phân tích lặp code A4):**
  - **Mục đích:** Đối chứng trực diện với phương pháp sửa lỗi tuần tự không dùng cây tư duy (Paper Table 2 & Proposal §5.2).
  - **Lệnh chạy (trên từng batch `01..10`):**
    ```bash
    python3 scripts/run_benchmark_batch.py \
      --config configs/batches/batch_01.yaml \
      --dataset apps \
      --solver iterative_repair \
      --output-dir runs/iter_repair_14b_batch_01 \
      --problem-ids @data/batches/batch_01.json
    ```

- [ ] **E9. ⏳ 14B RethinkMCTS Dual Reward trên Full HumanEval-164 (164 bài):**
  - **Mục đích:** Bổ sung mảnh ghép còn thiếu ở Bảng 4.2 (vì `runs/humaneval_mcts_14b` hiện tại là Test-only `llm_weight=0.0`).
  - **Lệnh chạy:**
    ```bash
    python3 scripts/run_benchmark_batch.py \
      --config configs/benchmark_humaneval_14b.yaml \
      --dataset humaneval \
      --solver mcts \
      --output-dir runs/humaneval_mcts_dual_14b \
      --set prompts.bundle=native_v2 \
      --set reward.test_weight=0.8 \
      --set reward.llm_weight=0.2 \
      --set search.c=4.0 \
      --set search.max_rethinks_per_node=2
    ```

---

### 🟡 Ưu tiên 2: Các Nghiên cứu Triệt tiêu trên Full APPS-300 (Ablation Studies — Chương 5)

Tất cả các cấu hình dưới đây đều chạy trên `configs/batches/batch_01..10.yaml` (300 bài chia 10 GPU, khoảng ~45–55 phút/đợt) và chỉ thay đổi **đúng 1 tham số (`--set`)** so với 14B MCTS Dual (`36.00%`):

- [ ] **E3. ⏳ Ablation 1 — 14B RethinkMCTS Test-only (`w/o selfEval`) trên Full APPS-300:**
  - **Tham số:** `--set reward.test_weight=1.0 --set reward.llm_weight=0.0`
  - **Mục đích:** Đối chiếu trực tiếp với 14B Dual (`36.00%`) và 7B Test-only (`22.67%`) để chứng minh vai trò của LLM Critic khi tăng quy mô từ 7B lên 14B.
- [ ] **E4. ⏳ Ablation 2 — 14B MCTS Không Rethink (`w/o Rethink`) trên Full APPS-300:**
  - **Tham số:** `--set search.max_rethinks_per_node=0`
  - **Mục đích:** Chứng minh cơ chế sửa tư duy tại lá (*Leaf Revision / Rethink*) là nhân tố quyết định giúp cây tìm kiếm hội tụ (Paper Fig. 3 & Table 4).
- [ ] **E6. ⏳ Ablation 3 — Mức độ Phản hồi Thực thi (`Feedback Granularity`) trên Full APPS-300:**
  - **Tham số:**
    - Chạy `facts_only` (chỉ có thông báo lỗi thô): `--set feedback.mode=facts_only`
    - Chạy `trace` (`w/o blockInfo` — có vết biến nhưng tắt phân tích block bằng LLM): `--set feedback.mode=trace`
  - **Mục đích:** Chứng minh hiệu quả của phân tích CFG + trạng thái biến (`mode=block`) so với traceback thô (Proposal §5.3 Ablation 1 & RQ1).
- [ ] **E10. ⏳ Ablation 4 — Chính sách Lan truyền (`Mean Backup` vs `Max Backup`) trên Full APPS-300:**
  - **Tham số:** `--set search.backup=mean`
  - **Mục đích:** Chứng minh chính sách $Q = \max$ bảo vệ nhánh tiềm năng tốt hơn trung bình cộng $Q = \text{mean}$ của MCTS truyền thống (Proposal §5.3 Ablation 2).
