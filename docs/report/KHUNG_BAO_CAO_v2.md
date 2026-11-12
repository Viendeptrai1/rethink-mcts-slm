# Khung báo cáo v2 (bản nháp, cập nhật 12/11/2026)

Bản nháp này xác định lại vấn đề nghiên cứu và sườn báo cáo sau đợt review code ngày 11–12/11/2026, theo hướng **nhiều model mở 7–9B** ([D-006](../research/DECISION_LOG.md)). Chưa thay thế các chương `01`–`06`; khi khung được chốt, từng chương sẽ được viết lại theo đây.

Ký hiệu trạng thái (theo [README.md](README.md)): `✅` đã có số liệu dùng được · `🧮` chỉ cần phân tích offline, không tốn GPU · `⏳` cần chạy GPU · `❌` số liệu cũ không dùng được cho kết luận · `⚠️` chỉ tham khảo.

## 0. Vì sao phải viết lại khung

1. **Cài đặt v1 (14B) chưa chạy đúng hai cơ chế cốt lõi của RethinkMCTS.**
   - Kết quả block analysis bị bỏ hoàn toàn (0/1.203 lần vào feedback).
   - Prompt rethink không cho model thấy thought đang sửa.
   - Critic không có tác dụng vì search dừng ngay khi pass public.
   - Ngân sách tính cả rethink, nên cây chỉ sâu tối đa 2.

   Đã sửa trong code v3: [prompts/README.md](../../prompts/README.md), [configs/v3_7b/README.md](../../configs/v3_7b/README.md).
2. **So sánh chưa cùng chi phí.** MCTS được tới 16 lần sinh code, BO3 chỉ được 3.
3. **Một model, một seed** thì chỉ kết luận được cho đúng model đó.
4. **7B (nhánh HuyinCP) và 14B dùng protocol khác nhau** (2 rollout, chấm trên toàn bộ test), nên không so trực tiếp được.

## 1. Phát biểu lại vấn đề

**Tên đề tài (giữ nguyên theo [Proposal.md](../../Proposal.md)):** Cải thiện khả năng suy luận của LLM trong sinh mã nguồn bằng Monte Carlo Tree Search với phản hồi từ kiểm thử tự động.

**Vấn đề cụ thể:** Tái hiện và kiểm chứng RethinkMCTS (Li et al., arXiv:2409.09584) trên **ba model mã nguồn mở cỡ 7–9B thuộc ba thế hệ** (2024–2026), với đúng thiết lập của bài báo, và so với baseline **cùng ngân sách sinh code**.

| Vai trò | Model | Ra mắt |
|---|---|---|
| Chuyên code, thế hệ 2024 | Qwen2.5-Coder-7B-Instruct | 09/2024 |
| Chuyên code, thế hệ 2025 | Seed-Coder-8B-Instruct | 06/2025 |
| Đa dụng, thế hệ 2026, tắt thinking | Qwen3.5-9B (dự phòng: Granite-4.2-8B) | 02/2026 (08/2026) |

**Phạm vi:**
- Dữ liệu: APPS-300 (cohort đóng băng, seed 2027) và HumanEval-164.
- Một seed, temperature 0 theo bài báo.
- Suy luận bf16 trên vLLM (Modal L40S).
- Kết quả 14B v1 chỉ vào phụ lục. 14B v3 chỉ chạy nếu còn credit, làm điểm so quy mô với Qwen2.5-Coder-7B.

**Đóng góp dự kiến:**
1. Một bản cài đặt có kiểm thử, tách bạch public và hidden test, có manifest tái lập, bám prompt và thiết lập của bài báo.
2. Kết quả tái hiện trên ba model mở 7–9B, so sánh cùng chi phí.
3. Bằng chứng về câu hỏi: khi model nhỏ mạnh dần lên (2024 → 2026), search bên ngoài còn giúp bao nhiêu?
4. **Bài học tái hiện:** những sai lệch cài đặt nhỏ (biến prompt bị bỏ trống, parser sai khóa, dừng sớm) đủ làm mất tác dụng của cả cơ chế mà hệ thống không báo lỗi. Đây là phát hiện có thật từ v1, nên trình bày trung thực.

## 2. Câu hỏi nghiên cứu và giả thuyết

Các giả thuyết dưới đây là **giả thuyết cần kiểm chứng**, chưa phải kết luận.

| Mã | Câu hỏi | Giả thuyết | Thực nghiệm | Bảng/Hình |
|---|---|---|---|---|
| RQ1 | RethinkMCTS có tốt hơn Direct và Best-of-16 trên **cả ba model** không? | H1: MCTS > Best-of-16 trên APPS (ghép cặp), ở ít nhất 2/3 model. | E1–E4 | B4.2–B4.4, H4.1 |
| RQ2 | Mức cải thiện thay đổi thế nào giữa các thế hệ model và giữa model chuyên code với đa dụng? | H2: mức cải thiện của MCTS so với Direct giảm khi Direct đã mạnh. | E1–E4 | B4.2, H4.2 |
| RQ3a | Rethink có giúp ích không? (Qwen2.5-Coder-7B) | H3a: MCTS > MCTS tắt rethink. | E5 | B5.1 |
| RQ3b | Block feedback có tốt hơn chỉ dùng thông tin thực thi không? (Qwen2.5-Coder-7B) | H3b: `block` > `facts_only`. | E6 | B5.1 |
| RQ3c | Critic có chọn được lời giải tốt hơn Test-only không, và khác nhau giữa các model không? | H3c: Dual > Test-only khi có nhiều ứng viên pass public. | E1 (chọn lại offline) | B5.2 |
| RQ4 | Chi phí và đường cong hiệu năng theo ngân sách ra sao? | — (mô tả) | E1, E3 | B4.5, H4.1 |
| RQ5 | Cài đặt v1 lệch bài báo ở đâu, và ảnh hưởng thế nào? | — (mô tả, so v1 với v3 nếu có 14B v3) | v1 (+ E7) | B5.3, Phụ lục A |

## 3. Mục lục nháp

### Chương 1. Đặt vấn đề
- 1.1 Bối cảnh: sinh code bằng LLM, test-time search, execution feedback, sự trỗi dậy của model nhỏ.
- 1.2 RethinkMCTS và khoảng trống: bài báo dùng GPT-3.5/4o-mini; chưa có kết quả trên nhiều model mở cỡ nhỏ với so sánh cùng chi phí.
- 1.3 Câu hỏi nghiên cứu (mục 2 ở trên).
- 1.4 Phạm vi và đóng góp (mục 1 ở trên).
- **Bỏ khỏi bản cũ:**
  - "Critic Degradation ở 7B" chuyển thành giả thuyết H3c.
  - "51,6% token cho block analysis" chỉ giữ như số liệu của v1.

### Chương 2. Cơ sở lý thuyết và phương pháp
- 2.1 MCTS mức thought: P-UCB (Eq. 1–2), expansion, Max backup.
- 2.2 Rethink tại lá và block-level verbal feedback (CFG, trace biến).
- 2.3 Dual reward có điều kiện (Eq. 3), critic thang [-1, 1].
- 2.4 Các baseline: Direct, Best-of-N.
- 2.5 Kiến trúc cài đặt (ports & adapters), chống rò rỉ hidden test, manifest, kiểm tra biến template (`strict_variables`).

### Chương 3. Thiết lập thực nghiệm
- 3.1 Dữ liệu và cách chia test. Public là một nửa số test **khác nhau** (lấy phần nguyên), áp dụng cho mọi phương pháp. Ví dụ `apps_4349` có 10 test nhưng chỉ 5 test khác nhau. 85 bài chỉ có 3 test, chia thành 1 public và 2 hidden.
- 3.2 Model (ba model), phần cứng (Modal L40S, bf16, vLLM pin phiên bản), tắt thinking cho mọi phương pháp.
- 3.3 **Bảng đối chiếu "Bài báo, v3, v1"** (B3.1, lấy từ [configs/v3_7b/README.md](../../configs/v3_7b/README.md)).
- 3.4 Phương pháp so sánh và ablation, mỗi lần chỉ đổi một yếu tố.
- 3.5 Metric: Pass@1 trên hidden (chính), mean pass rate, token và lời gọi mỗi bài, $/bài.
- 3.6 Thống kê: McNemar ghép cặp, bootstrap 95% CI, hiệu chỉnh Holm cho các so sánh.
- 3.7 Quy trình: pilot trên 20 bài **ngoài** cohort, có tiêu chí đạt. Sau đó đóng băng commit, prompt và config (ghi vào [PROTOCOL.md](../research/PROTOCOL.md)), rồi mới chạy cohort.
- 3.8 Threats to validity cần nêu ngay: nhiễm dữ liệu (APPS và HumanEval đã công khai từ 2021, model càng mới càng dễ đã thấy), một seed, và việc temperature 0 trên vLLM không tất định tuyệt đối khi batch.

### Chương 4. Kết quả chính
- 4.1 Độ phủ và lỗi kỹ thuật của từng run (bài timeout, bài lỗi được tính 0, liệt kê ID).
- 4.2 APPS-300: Direct, Best-of-16, RethinkMCTS × 3 model, theo mức khó (B4.2).
- 4.3 Kiểm định ghép cặp trong từng model (B4.3).
- 4.4 HumanEval-164 (B4.4).
- 4.5 Chi phí theo vai trò (B4.5), đường cong theo ngân sách (H4.1), so sánh giữa các model (H4.2).

### Chương 5. Phân tích
- 5.1 Ablation thành phần trên Qwen2.5-Coder-7B: rethink, feedback (B5.1); critic trên cả 3 model (B5.2).
- 5.2 Hành vi search: độ sâu đạt được, số ứng viên, nguồn gốc lời giải đúng (ban đầu, rethink hay mở rộng sâu), và phương án dừng sớm tính lại offline.
- 5.3 Bài học tái hiện: v1 so với v3 (B5.3).
- 5.4 Phân loại lỗi và case study. **Chỉ chọn case từ run v3.** Case `apps_1055` của bản cũ không đứng được.
- 5.5 Tham khảo: nhánh 7B của HuyinCP và 14B v1, đặt ở bảng riêng và nêu rõ protocol khác.

### Chương 6. Hạn chế và hướng phát triển
- Một seed; mức khó Competition có nhiều bài chỉ còn 2 hidden test; nhiễm dữ liệu; giới hạn thời gian 3600 giây; sandbox là subprocess.
- Hướng phát triển.

### Phụ lục
- A. Kết quả v1 (14B, có lỗi đã biết), giữ để minh bạch, không dùng cho kết luận.
- B. Prompt, config và manifest hash của các run v3.
- C. Kết quả pilot (chỉ để minh bạch quy trình, không phải kết quả).

## 4. Danh sách bảng và hình

| ID | Nội dung | Run/nguồn | Trạng thái |
|---|---|---|---|
| B3.1 | Bài báo, v3 và v1: tham số và điểm lệch | [configs/v3_7b/README.md](../../configs/v3_7b/README.md) | ✅ (chốt sau pilot) |
| B3.2 | Phân bố số public và hidden test theo mức khó | `prepared/apps_half` | 🧮 |
| B4.1 | Độ phủ, timeout, lỗi kỹ thuật mỗi run | E1–E4 | ⏳ |
| B4.2 | APPS-300 Pass@1 và pass rate theo mức khó: Direct, Best-of-16, MCTS × 3 model | E1–E3 | ⏳ |
| B4.3 | McNemar và bootstrap: MCTS so với từng baseline, trong từng model | E1–E3 | ⏳ |
| B4.4 | HumanEval-164: Direct, Best-of-16, MCTS × 3 model | E4 | ⏳ |
| B4.5 | Token, lời gọi và $/bài theo vai trò | E1–E4 | ⏳ |
| H4.1 | Pass@1 theo số lần sinh code: MCTS so với Best-of-k (k = 1…16), từng model | E1, E3 | ⏳ |
| H4.2 | Mức cải thiện (MCTS − Direct) theo thế hệ model | E1–E3 | ⏳ |
| B5.1 | Ablation trên Qwen2.5-Coder-7B: tắt rethink, `facts_only` | E5, E6 | ⏳ |
| B5.2 | Dual và Test-only (chọn lại offline) × 3 model | E1 | 🧮 sau E1 |
| B5.3 | v1 và v3 | v1 (+ E7) | 🧮 / ⏳ |
| B5.4 | Độ sâu cây, nguồn gốc lời giải đúng, dừng sớm offline | E1 | 🧮 sau E1 |
| B5.5 | Tham khảo: 7B HuyinCP, 14B v1 | [docs/results/7b](../results/7b/rethinkmcts-apps-native-v2-w4-retry.md), [runs/analysis_extra_14b](../../runs/analysis_extra_14b/summary.json) | ⚠️ |

## 5. Ma trận thực nghiệm

| Mã | Thực nghiệm | Model | Dữ liệu | Ưu tiên | GPU |
|---|---|---|---|---|---|
| E0 | Sửa code v3 và viết test | — | — | **Xong** (12/11/2026) | Không |
| P1–P4 | Pilot (xem [configs/v3_7b/README.md](../../configs/v3_7b/README.md)) | 3 model | 20 bài APPS ngoài cohort | Bắt buộc | Ít |
| E1 | RethinkMCTS v3 | 3 model | APPS-300 | Bắt buộc | Nhiều nhất |
| E2 | Direct v3 (temperature 0) | 3 model | APPS-300, HE-164 | Bắt buộc | Ít |
| E3 | Best-of-16 v3 (lưu đủ 16 mẫu, tính Best-of-k offline) | 3 model | APPS-300, HE-164 | Bắt buộc | Vừa |
| E4 | RethinkMCTS v3 | 3 model | HE-164 | Bắt buộc | Vừa |
| E5 | MCTS v3 tắt rethink | Qwen2.5-Coder-7B | APPS (300 hoặc tập con 150) | Nếu còn tiền | Nhiều |
| E6 | MCTS v3 `facts_only` | Qwen2.5-Coder-7B | Như E5 | Nếu còn tiền | Nhiều |
| E7 | MCTS v3 cho 14B (so quy mô) | Qwen2.5-Coder-14B | APPS-300 | Nếu còn tiền | Nhiều |

Direct và Best-of-N v1 dùng prompt `native_v2` và cách chia 2 public test, nên không dùng lại cho v3. Với model 7B, chạy lại Direct rất rẻ.

## 6. Các nhận định trong bản cũ cần gỡ hoặc sửa

| Nhận định cũ | Vị trí | Vấn đề | Xử lý |
|---|---|---|---|
| Feedback dùng block-level CFG analysis | ch.2, ch.4 | Ở v1 kết quả phân tích không vào feedback | Mô tả v1 là facts + trace; v3 kiểm chứng lại |
| Case study `apps_1055` giải cứu nhờ block analysis | 5.7.1 | Như trên | Bỏ, chọn case từ v3 |
| Critic không đổi chương trình được chọn ở 14B | 4.8.1 | Nguyên nhân là dừng sớm, không phải tính chất của critic | Ghi rõ nguyên nhân, kiểm lại ở B5.2 |
| Critic Degradation ở 7B (Test-only 22,67% > Dual 19,00%) | 1.3, 5.2.1 | 7B chạy 2 rollout, không kiểm định ghép cặp | Chuyển thành giả thuyết H3c |
| MCTS 7B vượt Direct 14B trên HumanEval | CURRENT_STATE | Khác protocol; HumanEval 7B là run `native_v1` | Bỏ so sánh chéo |
| Timeout 5 giây/test | ch.3 | Thực tế 4 giây (APPS) và 3 giây (HumanEval) | Sửa |
| Cấu hình tương ứng bài báo | 2.5, 3.2 | v1 lệch ở nhiều điểm | Thay bằng B3.1 |
| Kết quả chính là 14B | ch.1, ch.4 | Đã chuyển sang 3 model 7–9B | Viết lại ch.4; 14B v1 vào phụ lục |

## 7. Quyết định

**Đã chốt (D-006, 12/11/2026):**
- 3 model 7–9B, tắt thinking.
- Modal L40S, bf16, không nén trọng số.
- Thiết lập bài báo: 16 rollout, 1 rethink, không dừng sớm, temperature 0, critic [-1, 1].
- Public là một nửa số test khác nhau. Baseline Direct và Best-of-16.

**Còn mở:**
1. Temperature của Best-of-16 (đề xuất 0,8).
2. Ablation E5/E6 chạy trên 300 bài hay tập con phân tầng 150 bài, tùy ước tính chi phí sau pilot.
3. Nhánh 7B của HuyinCP: chỉ tham khảo, hay chạy lại theo v3 và chia model giữa hai thành viên?
4. Có chạy E7 (14B v3) không.
