# Khung báo cáo v2 (bản nháp, cập nhật 13/11/2026)

Bản nháp này xác định lại vấn đề nghiên cứu và sườn báo cáo sau đợt review code ngày 11–12/11/2026, theo hướng **nhiều model mở 7–9B** ([D-006](../research/DECISION_LOG.md)). Các chương cũ (viết theo số liệu v1) đã gỡ ngày 13/11/2026; báo cáo được viết lại theo khung này. Nguồn số liệu duy nhất là [BENCHMARK_LEDGER.md](../results/BENCHMARK_LEDGER.md).

Ký hiệu trạng thái (theo [README.md](README.md)): `✅` đã có số liệu dùng được · `🧮` chỉ cần phân tích offline, không tốn GPU · `⏳` cần chạy GPU · `❌` số liệu cũ không dùng được cho kết luận · `⚠️` chỉ tham khảo.

## 0. Vì sao phải viết lại khung

1. **Cài đặt cũ (v1) chưa chạy đúng hai cơ chế cốt lõi của RethinkMCTS.**
   - Kết quả block analysis bị bỏ hoàn toàn (0/1.203 lần vào feedback).
   - Prompt rethink không cho model thấy thought đang sửa.
   - Critic không có tác dụng vì search dừng ngay khi pass public.
   - Ngân sách tính cả rethink, nên cây chỉ sâu tối đa 2.

   Đã sửa trong code v3: [prompts/README.md](../../prompts/README.md), [configs/v3_7b/README.md](../../configs/v3_7b/README.md).
2. **So sánh chưa cùng chi phí.** MCTS được tới 16 lần sinh code, BO3 chỉ được 3.
3. **Một model, một seed** thì chỉ kết luận được cho đúng model đó.

## 1. Phát biểu lại vấn đề

**Tên đề tài (giữ nguyên theo [Proposal.md](../../Proposal.md)):** Cải thiện khả năng suy luận của LLM trong sinh mã nguồn bằng Monte Carlo Tree Search với phản hồi từ kiểm thử tự động.

**Vấn đề cụ thể:** Tái hiện và kiểm chứng RethinkMCTS (Li et al., arXiv:2409.09584) trên **ba model mã nguồn mở cỡ 7–9B thuộc ba thế hệ** (2024–2026), với đúng thiết lập của bài báo, và so với baseline **cùng ngân sách sinh code**.

| Vai trò | Model | Ra mắt |
|---|---|---|
| Chuyên code, thế hệ 2024 | Qwen2.5-Coder-7B-Instruct | 09/2024 |
| Chuyên code, thế hệ 2025 | Seed-Coder-8B-Instruct | 06/2025 |
| Đa dụng, thế hệ 2026, tắt thinking | Qwen3.5-9B (dự phòng: Granite-4.2-8B) | 02/2026 (08/2026) |

**Cách đặt vấn đề trong báo cáo (thống nhất 14/11/2026):** mở đầu bằng một bài toán tổng quát là *giải bài với bộ kiểm chứng một phần* (yêu cầu $x$, lời giải thực thi được $y$, kiểm chứng lúc giải $V_{pub}$ có phản hồi nhưng không đầy đủ, kiểm chứng ẩn $V_{hid}$, ngân sách $B$). **Text-to-SQL** là bài toán ứng dụng dùng làm ví dụ xuyên suốt; **sinh mã nguồn** là trường hợp được thực nghiệm, vì có sẵn public/hidden test và benchmark chuẩn. Không chạy thực nghiệm Text-to-SQL; phần kết luận quay lại bài toán này (điều kiện áp dụng: chất lượng bộ kiểm chứng, critic chưa đủ tin cậy). Lưu ý: bài báo **có** baseline Base(16) và bảng token; khoảng trống là chỉ có hai mô hình đóng, một lần chạy, chưa có kiểm định ghép cặp và chưa đặt độ chính xác cạnh chi phí trên LLM mở cỡ nhỏ.

**Phạm vi:**
- Dữ liệu: APPS-300 (cohort đóng băng, seed 2027) và HumanEval-164.
- Một seed, temperature 0 theo bài báo.
- Suy luận bf16 trên vLLM 0.31.0, GPU A100-SXM4-40GB (Colab, Modal).
- Không dùng kết quả của cài đặt cũ (v1); chỉ mô tả các lỗi của nó (RQ5).

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
| RQ5 | Cài đặt cũ (v1) lệch bài báo ở đâu, và vì sao các lệch đó làm mất tác dụng của cơ chế? | — (mô tả, không dùng số liệu v1) | Review code 11–12/11/2026 ([D-006](../research/DECISION_LOG.md)) | B5.3 |

## 3. Mục lục nháp

### Chương 1. Đặt vấn đề
- 1.1 Bối cảnh: sinh code bằng LLM, test-time search, execution feedback, sự trỗi dậy của model nhỏ.
- 1.2 RethinkMCTS và khoảng trống: bài báo dùng GPT-3.5/4o-mini; chưa có kết quả trên nhiều model mở cỡ nhỏ với so sánh cùng chi phí.
- 1.3 Câu hỏi nghiên cứu (mục 2 ở trên).
- 1.4 Phạm vi và đóng góp (mục 1 ở trên).

### Chương 2. Cơ sở lý thuyết và phương pháp
- 2.1 MCTS mức thought: P-UCB (Eq. 1–2), expansion, Max backup.
- 2.2 Rethink tại lá và block-level verbal feedback (CFG, trace biến).
- 2.3 Dual reward có điều kiện (Eq. 3), critic thang [-1, 1].
- 2.4 Các baseline: Direct, Best-of-N.
- 2.5 Kiến trúc cài đặt (ports & adapters), chống rò rỉ hidden test, manifest, kiểm tra biến template (`strict_variables`).

### Chương 3. Thiết lập thực nghiệm
- 3.1 Dữ liệu và cách chia test. Public là một nửa số test **khác nhau** (lấy phần nguyên), áp dụng cho mọi phương pháp. Ví dụ `apps_4349` có 10 test nhưng chỉ 5 test khác nhau. 85 bài chỉ có 3 test, chia thành 1 public và 2 hidden.
- 3.2 Model (ba model), phần cứng (A100-SXM4-40GB trên Colab và Modal, bf16, vLLM 0.31.0), tắt thinking cho mọi phương pháp. Nêu rõ: Qwen3.5-9B chạy phần lớn trên Modal; gate trên hai nền tảng khớp 12/13 bài.
- 3.3 **Bảng đối chiếu "Bài báo, v3, cài đặt cũ"** (B3.1, lấy từ [configs/v3_7b/README.md](../../configs/v3_7b/README.md)).
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
- 5.3 Bài học tái hiện: các lệch của cài đặt cũ và cách v3 sửa (mô tả, B5.3).
- 5.4 Phân loại lỗi và case study. **Chỉ chọn case từ run v3.** Case `apps_1055` của bản cũ không đứng được.

### Chương 6. Hạn chế và hướng phát triển
- Một seed; mức khó Competition có nhiều bài chỉ còn 2 hidden test; nhiễm dữ liệu; giới hạn thời gian 3600 giây; sandbox là subprocess.
- Hướng phát triển.

### Phụ lục
- A. Prompt, config và manifest hash của các run v3.
- B. Kết quả pilot (chỉ để minh bạch quy trình, không phải kết quả).

## 4. Danh sách bảng và hình

| ID | Nội dung | Run/nguồn | Trạng thái |
|---|---|---|---|
| B3.1 | Bài báo, v3 và cài đặt cũ: tham số và điểm lệch | [configs/v3_7b/README.md](../../configs/v3_7b/README.md) | ✅ (chốt sau pilot) |
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
| B5.3 | Lệch của cài đặt cũ và cách v3 sửa (mô tả, không số liệu) | Review code, D-006 | ✅ |
| B5.4 | Độ sâu cây, nguồn gốc lời giải đúng, dừng sớm offline | E1 | 🧮 sau E1 |

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

## 6. Không lặp lại các nhận định của bản cũ

Khi viết lại các chương, không dùng các nhận định sau của bản cũ:
- "Feedback dùng block-level CFG analysis" (ở v1 kết quả phân tích không vào feedback) và case study `apps_1055`. Chỉ chọn case từ run v3.
- Các nhận định về critic của bản cũ (critic không có tác dụng vì dừng sớm). Dùng kết quả chọn lại offline của v3 (B5.2).
- Mọi so sánh chéo giữa các protocol hoặc nhánh khác nhau.
- "Timeout 5 giây/test": thực tế là 4 giây với APPS và 3 giây với HumanEval.
- "Cấu hình tương ứng bài báo": thay bằng bảng B3.1.

## 7. Quyết định

**Đã chốt (D-006, D-007, D-008; 12–13/11/2026):**
- 3 model 7–9B, tắt thinking.
- A100-SXM4-40GB (Colab, Modal), bf16, vLLM 0.31.0, không nén trọng số.
- Thiết lập bài báo: 16 rollout, 1 rethink, không dừng sớm, temperature 0, critic [-1, 1].
- Public là một nửa số test khác nhau. Baseline Direct và Best-of-16 (temperature 0,8, top_p 0,95).
- Không chạy 14B (bỏ E7, 13/11/2026); không dùng nhánh 7B cũ.

**Còn mở:**
1. Ablation E5/E6 chạy trên 300 bài hay tập con phân tầng 150 bài, tùy credit còn lại.
