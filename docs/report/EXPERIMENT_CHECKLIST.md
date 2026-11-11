# Checklist Thực nghiệm & Phân tích Toàn diện (Chuẩn hóa Full 300 bài APPS & 164 bài HumanEval)

> **Quyết định thiết kế thực nghiệm:** Toàn bộ các phép so sánh Baseline và Ablation trên APPS đều chạy trên **trọn vẹn 300 bài chuẩn hóa (`data/cohorts/apps_benchmark_300.json` — chia 10 batch $\times$ 30 bài tại `data/batches/batch_01..10.json`)** thông qua `scripts/run_benchmark_batch.py` và gom kết quả bằng `scripts/merge_apps_batches.py`. Không dùng tập con 60 bài để đảm bảo mọi bảng số liệu trong báo cáo đều đồng nhất tuyệt đối trên mẫu số **300/300 bài**.

Ký hiệu:
- `[x]` Đã hoàn thành · `[ ]` Chưa làm
- `🧮` **Phân tích Offline trên dữ liệu sẵn có trong máy (0 tốn GPU)**
- `⏳` **Cần gọi LLM / chạy GPU (Full 300 bài APPS hoặc 164 bài HumanEval)**

---

## 0. Kế hoạch chạy bổ sung sau kiểm tra artifact (07/11/2026) — chờ tài khoản Modal mới

Kết luận kiểm tra: kết quả chính 14B APPS-300 (MCTS so với Direct) đã đủ vững, **không cần chạy lại**. Những mục dưới đây chỉ chạy khi có credit mới. Chi phí ước tính bằng `solve_wall_seconds` thực tế × giá L40S $1.95/giờ, chỉ để tham khảo.

**Đã làm offline (0 GPU):**
- [x] Chấm lại 14B APPS trên toàn bộ test (public + hidden), khớp protocol `all_tests` của 7B: [`scripts/alltests_rejudge_offline.py`](../../scripts/alltests_rejudge_offline.py) → `runs/*/all_tests_offline.json`.

**Nên chạy (rẻ, làm sạch bảng chính):**
- [ ] HumanEval-164 Direct và BoN-3 bằng code schema 2 hiện tại (các run cũ `runs/humaneval_{direct,bon3}_14b/` không có manifest). ~$1–3.
- [ ] BoN-3 cho 140 bài APPS còn lại (40 Interview + 100 Competition) để đủ 300/300. ~$5.

**Đáng chạy nhất nếu còn ngân sách:**
- [ ] E4: không rethink (`--set search.max_rethinks_per_node=0`) trên APPS-300. Đây là cách duy nhất chứng minh đóng góp của rethink. ~$10–18.

**Tùy chọn (có thể thành đóng góp riêng):**
- [ ] Dừng sớm có điều kiện critic: chỉ dừng khi pass hết public và critic không chấm −1. Cần thêm chế độ `early_stop` mới. Chỉ 35 bài critic chấm −1 bị ảnh hưởng, nên có thể chạy riêng 35 bài này (chọn theo thông tin có lúc search, không dùng hidden).

**Cần có để trả lời các RQ đã cam kết (chương 1 §1.4, Proposal §5.2–5.3):**
- [ ] E5: Iterative Repair trên APPS-300 (RQ1, Proposal §5.2). Chưa có số đo chi phí.
- [ ] E6: `--set feedback.mode=facts_only` trên APPS-300 (RQ2b, Proposal Ablation 1: CFG so với traceback thô); `trace` là tùy chọn. Tối đa ~$18/run.
- [ ] E10: `--set search.backup=mean` trên APPS-300 (RQ2c, Proposal Ablation 2), hoặc bỏ mục này khỏi RQ2 và ghi rõ chưa thực hiện. Dự đoán "cây quá nhỏ nên không khác biệt" (2.79 vòng lặp/bài) chưa được đo. Tối đa ~$18.
- [ ] Trọng số reward (Proposal Ablation 4): phải chạy với chế độ dừng khác `public_all_passed`, vì dưới chế độ này critic không ảnh hưởng đến lựa chọn.
- [ ] Chạy 7B qua cùng pipeline `src/rethink_mcts` (RQ3). Đây là cách duy nhất để so sánh 7B và 14B mà không lẫn codebase, ngân sách và cách chia test.
- [ ] 🧮 Đường cong theo $k$ chính xác (RQ4, chỉ tốn CPU): `candidates.json` có lưu code của mọi ứng viên, nên có thể chấm hidden cho ứng viên được chọn tại từng $k$ thay vì dùng cận dưới.

**Không nên chạy:**
- ~~E3 Test-only 14B với cấu hình hiện tại~~: với `early_stop=public_all_passed` và 2 public test, critic không làm đổi lựa chọn ở bài nào, nên kết quả sẽ trùng Dual.

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
  - **14B APPS-300 (MCTS vs Direct):** $\chi^2 = 18.4808, p = 1.72 \times 10^{-5} \ll 0.001$, Bootstrap 95% CI $\Delta = +10.67\%$ ($[+3.67\%, +18.00\%]$). Cứu 42 bài.
  - **14B HumanEval-164 (MCTS Test-only vs Direct):** $\Delta = +3.05\%$, cứu 9 bài Direct sai.
  - **14B APPS Intro (MCTS vs Direct):** $\chi^2 = 4.9231, p = 0.0265 < 0.05$, Bootstrap 95% CI $\Delta = +9.00\%$ ($[+3.00\%, +16.00\%]$).
  - Chi tiết tại [Chương 4 §4.5](04_ket_qua_thuc_nghiem.md).
- [x] **A3. 🧮 Phân loại Lỗi, Tỷ lệ Cứu vãn nhờ Rethink & Tỷ lệ Code Hợp lệ trên Cây (Paper Table 4):**
  - Đã trích xuất xong từ 300 bài 14B: 216 bài kích hoạt Rethink; cứu thành công 77 bài pass public (35.6%) và **38 bài pass hidden (17.6%)**; đóng góp 35.2% tổng số bài giải đúng của 14B. Tree Effective Code Rate = **9.21%** (161/1,748 code). Lỗi lần đầu: 85.2% WA, 13.9% RE, 0.9% TLE, 0% CE. Chi tiết tại [Chương 5 §5.5](05_phan_tich_thao_luan.md).
- [x] **A5. 🧮 Phân tích Tương quan & Kiểm định Thống kê Quy mô 7B vs 14B (Chi-Square & Odds Ratio):**
  - Đã tính toàn bộ kiểm định $\chi^2$ (hiệu chỉnh Yates) và Odds Ratio đối đầu giữa 7B và 14B trên APPS-300 và HumanEval-164:
    - APPS Direct: $\chi^2 = 11.4881, p = 7.00 \times 10^{-4} < 0.001$, Odds Ratio = 2.08.
    - APPS MCTS Dual: $\chi^2 = 20.8986, p = 4.84 \times 10^{-6} \ll 0.001$, Odds Ratio = 2.40.
    - Phân tầng Competition: $\chi^2 = 17.5649, p = 2.78 \times 10^{-5} \ll 0.001$, Odds Ratio = **7.39 $\times$** (bước nhảy vọt từ 5% lên 28%).
    - HumanEval Direct: $\chi^2 = 5.4911, p = 0.0191 < 0.05$, Odds Ratio = 2.24.
    - Chi tiết tại [Chương 4 §4.9](04_ket_qua_thuc_nghiem.md).
- [x] **A6. 🧮 Đường cong Mở rộng theo Ngân sách (Test-Time Scaling Curve — Proposal Ablation 3 & Paper Fig. 5):**
  - Đã dựng xong đường cong Pass@1 theo $k \in \{1, 2, 4, 8, 16\}$ trên 300 bài 14B: $k=1$ (22.00%) $\to$ $k=2$ (26.67%) $\to$ $k=4$ (31.33%) $\to$ $k=8$ (35.00%) $\to$ $k=16$ (36.00%). Tăng trưởng đơn điệu hàm logarit. Chi tiết tại [Chương 5 §5.6](05_phan_tich_thao_luan.md).
- [x] **A7. 🧮 Trích xuất 3 Case Studies Điển hình & Ví dụ Trace (Paper Table 13 & 14):**
  - Đã trích xuất và phân tích chi tiết 3 bài: `apps_1055` (sửa lỗi đệ quy vô hạn Thanos sort bằng CFG + rethink), `apps_3019` (bứt phá phân tầng Competition nhờ sàng nguyên tố), và `apps_1029` (thất bại do quá khớp test công khai). Chi tiết tại [Chương 5 §5.7](05_phan_tich_thao_luan.md).
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

- [x] **E2. ⏳ 14B Best-of-3 (`--solver best_of_n --samples-n 3`) trên APPS (160 bài: 100 Intro + 60 Inter) — ĐÃ HOÀN TẤT:**
  - **Kết quả:** Pass@1 = **35.62%** (57/160), Mean Hidden Pass Rate = **49.85%**.
    - Phân tầng Introductory (100/100 bài trọn vẹn): Pass@1 = **50.00%** (50/100), Mean Hidden = **60.94%**.
    - Phân tầng Interview (60/100 bài): Pass@1 = **11.67%** (7/60), Mean Hidden = **31.36%**.
  - **So sánh trên cùng 160 bài:** Direct (29.38%) < BoN-3 (35.62%) < MCTS Dual (**40.00%**).
  - **Artifact:** `runs/benchmark_apps_14b_bon3_300/summary.json` (Dừng an toàn tại ngưỡng $29.10 credit, bảo toàn $0.00 hóa đơn).

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

- [x] **E9. ⏳ 14B RethinkMCTS Dual Reward trên Full HumanEval-164 (164 bài) — ĐÃ HOÀN TẤT:**
  - **Kết quả:** Pass@1 = **90.85%** (149/164 bài), 4.64 calls/bài, 3,217 tokens/bài, 25.26s/bài.
  - **So sánh trên HumanEval 14B:** Direct (90.24%) < Dual Reward (90.85%) < BoN-3 (91.46%) < Test-only (93.29%). Chi tiết tại [Chương 4 §4.2](04_ket_qua_thuc_nghiem.md).
  - **Artifact:** `runs/humaneval_mcts_dual_14b/summary.json`

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
