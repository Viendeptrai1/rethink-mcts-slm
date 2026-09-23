# BÁO CÁO TỔNG HỢP THỰC NGHIỆM BENCHMARK TRÊN TẬP DỮ LIỆU HUMANEVAL
## Đề tài: Tối Ưu Hóa Tìm Kiếm Suy Luận Cho Mô Hình Ngôn Ngữ Nhỏ Trong Lập Trình (TLCN)

- **Ngày hoàn thành thực nghiệm**: 10/09/2026
- **Mô hình thử nghiệm**: `Qwen/Qwen2.5-Coder-14B-Instruct` (14.7B parameters, bfloat16, Trọng số CỐ ĐỊNH - Frozen Weights)
- **Hạ tầng tính toán**: NVIDIA H200 SXM (141GB VRAM) trên Modal Cloud (vLLM v0.29.0, FlashAttention-3)
- **Bộ dữ liệu**: HumanEval (164 bài toán, đánh giá độc lập qua Hidden Judge)

---

## 1. Tóm Tắt Kết Quả Thực Nghiệm Cốt Lõi

| Chỉ số (Metric) | 1. Direct Baseline (Greedy) | 2. Best-of-3 Baseline | 3. RethinkMCTS (Đề xuất) |
| :--- | :---: | :---: | :---: |
| **Tỷ lệ Pass@1 (100% Test Ẩn)** | **90.24%** | **91.46%** | **93.29%** 🏆 |
| **Số bài Giải Đúng** | 148 / 164 | 150 / 164 | **153 / 164** |
| **Số bài Giải Sai** | 16 | 14 | **11** |
| **Tổng Số Lượt Gọi Mô Hình** | 314 | 947 | **747** *(Ít hơn Bon3 200 calls)* |
| **Hiệu quả Mẫu (Avg Calls/Bài)** | 1.91 | 5.77 | **4.55** |
| **Mức Tăng Trưởng so với Direct** | Mốc chuẩn (Baseline) | +1.22% (+2 bài) | **+3.05% (+5 bài)** |
| **Tỷ lệ Sửa Lỗi Thành Công** | 0% | 3 / 16 bài (18.8%) | **9 / 16 bài (56.2%)** 🎯 |

---

## 2. Phân Tích Ý Nghĩa Học Thuật & Đóng Góp Của Đề Tài

### 2.1. Tính Vượt Trội Của Tìm Kiếm Có Cấu Trúc So Với Lấy Mẫu Ngẫu Nhiên (Sample Efficiency)
- **Best-of-3 (Lấy mẫu ngẫu nhiên)**: Sinh độc lập 3 lời giải ngẫu nhiên rồi chọn lời giải có điểm public test cao nhất. Phương pháp này tiêu tốn tới **947 lượt gọi mô hình**, nhưng chỉ tăng thêm được **2 bài đúng** so với Direct (từ 148 lên 150 bài).
- **RethinkMCTS (Cây ý nghĩ + Tự phản tỉnh)**: Xây dựng không gian tìm kiếm ở cấp độ ý nghĩ (Thought-Level Tree), kết hợp cơ chế tự sửa sai (Leaf Revision) dựa trên thông tin phản hồi từ test case công khai. Phương pháp này đạt **153 bài đúng** (+5 bài so với Direct), nhưng chỉ tiêu tốn **747 lượt gọi mô hình**.
- **Kết luận quan trọng**: RethinkMCTS vừa đạt **độ chính xác cao hơn (+1.83% so với Best-of-3)**, vừa **tiết kiệm hơn 21% chi phí tính toán** nhờ cơ chế dừng sớm thông minh khi đã đạt kết quả tối ưu.

### 2.2. Phân Loại Khả Năng Sửa Lỗi Trên 16 Bài Toán Direct Giải Sai
Trong 16 bài toán mà Direct Baseline thất bại:
- **Best-of-3 sửa được**: 3 bài (`python_59`, `python_89`, `python_124`)
- **RethinkMCTS sửa được**: 9 bài (`python_59`, `python_83`, `python_89`, `python_108`, `python_110`, `python_124`, `python_129`, `python_149`, `python_163`)
- **Số bài ĐỘC QUYỀN chỉ RethinkMCTS sửa được (Best-of-3 bất lực)**: **6 bài** (`python_83`, `python_108`, `python_110`, `python_129`, `python_149`, `python_163`)
- **Số bài cả 3 phương pháp chưa vượt qua**: 7 bài (`python_65`, `python_127`, `python_130`, `python_132`, `python_134`, `python_145`, `python_160`)

### 2.3. Minh Chứng Thực Nghiệm Cơ Chế "Rethink" (Case Study: `python_163`)
Bài toán yêu cầu sinh danh sách các chữ số chẵn nằm giữa hai số $a$ và $b$ theo thứ tự tăng dần.
1. **Lần sinh ban đầu**: Mô hình hiểu nhầm là sinh toàn bộ các số chẵn (kể cả số có 2 chữ số như 10, 12...), dẫn đến kiểm thử công khai thất bại (`0/3 passed`).
2. **Phản hồi lỗi thực thi**: Hệ thống phát hiện sai lệch đầu ra (`AssertionError`).
3. **Ý nghĩ phản tỉnh từ cơ chế Rethink**:
   > *"The previous approach generated all even numbers within the specified range, including multi-digit numbers, which is incorrect based on the test cases expecting only single-digit even numbers. The corrected strategy should focus on generating only the single-digit even numbers (0 through 8)..."*
4. **Tái sinh mã nguồn**: Mã nguồn mới được sinh ra theo đúng ý nghĩ đã sửa đổi, vượt qua **100% test ẩn chính thức**.
*Nhận xét*: Với Best-of-3, cả 3 mẫu sinh ngẫu nhiên đều mắc cùng một định kiến hiểu nhầm. Chỉ có cơ chế phản tỉnh từ thông tin phản hồi lỗi (Feedback-guided Rethink) mới giúp mô hình tự nhận thức và khắc phục được sai lầm.

---

## 3. Bảng Chi Tiết Kết Quả Của Toàn Bộ 164 Bài Toán

| STT | Mã Bài Toán | Direct (Greedy) | Best-of-3 | RethinkMCTS | Model Calls (Dir / Bon / MCTS) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | `python_0` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 20 |
| 2 | `python_1` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 20 |
| 3 | `python_2` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 19 |
| 4 | `python_3` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 20 |
| 5 | `python_4` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 20 |
| 6 | `python_5` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 20 |
| 7 | `python_6` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 19 |
| 8 | `python_7` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 20 |
| 9 | `python_8` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 20 |
| 10 | `python_9` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 20 |
| 11 | `python_10` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 18 |
| 12 | `python_11` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 13 | `python_12` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 14 | `python_13` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 15 | `python_14` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 16 | `python_15` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 17 | `python_16` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 18 | `python_17` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 19 | `python_18` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 20 | `python_19` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 21 | `python_20` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 22 | `python_21` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 23 | `python_22` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 24 | `python_23` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 25 | `python_24` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 26 | `python_25` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 27 | `python_26` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 28 | `python_27` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 29 | `python_28` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 30 | `python_29` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 31 | `python_30` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 32 | `python_31` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 33 | `python_32` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 34 | `python_33` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 35 | `python_34` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 36 | `python_35` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 37 | `python_36` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 38 | `python_37` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 39 | `python_38` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 5 |
| 40 | `python_39` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 41 | `python_40` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 42 | `python_41` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 43 | `python_42` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 44 | `python_43` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 45 | `python_44` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 46 | `python_45` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 47 | `python_46` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 48 | `python_47` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 49 | `python_48` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 50 | `python_49` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 51 | `python_50` | ✅ PASS | ✅ PASS | ❌ FAIL | 2 / 6 / 3 |
| 52 | `python_51` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 53 | `python_52` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 54 | `python_53` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 55 | `python_54` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 56 | `python_55` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 57 | `python_56` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 58 | `python_57` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 59 | `python_58` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 60 | `python_59` | ❌ FAIL | ✅ PASS | ✅ PASS | 1 / 4 / 5 |
| 61 | `python_60` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 62 | `python_61` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 63 | `python_62` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 64 | `python_63` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 65 | `python_64` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 66 | `python_65` | ❌ FAIL | ❌ FAIL | ❌ FAIL | 1 / 3 / 14 |
| 67 | `python_66` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 68 | `python_67` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 69 | `python_68` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 70 | `python_69` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 71 | `python_70` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 72 | `python_71` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 73 | `python_72` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 74 | `python_73` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 75 | `python_74` | ✅ PASS | ❌ FAIL | ✅ PASS | 2 / 6 / 3 |
| 76 | `python_75` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 77 | `python_76` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 78 | `python_77` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 79 | `python_78` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 80 | `python_79` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 81 | `python_80` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 82 | `python_81` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 83 | `python_82` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 84 | `python_83` | ❌ FAIL | ❌ FAIL | ✅ PASS | 1 / 3 / 5 |
| 85 | `python_84` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 86 | `python_85` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 87 | `python_86` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 88 | `python_87` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 89 | `python_88` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 90 | `python_89` | ❌ FAIL | ✅ PASS | ✅ PASS | 1 / 4 / 3 |
| 91 | `python_90` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 92 | `python_91` | ✅ PASS | ✅ PASS | ❌ FAIL | 2 / 6 / 3 |
| 93 | `python_92` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 94 | `python_93` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 5 |
| 95 | `python_94` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 96 | `python_95` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 97 | `python_96` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 98 | `python_97` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 99 | `python_98` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 100 | `python_99` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 101 | `python_100` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 102 | `python_101` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 103 | `python_102` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 104 | `python_103` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 105 | `python_104` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 106 | `python_105` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 107 | `python_106` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 108 | `python_107` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 109 | `python_108` | ❌ FAIL | ❌ FAIL | ✅ PASS | 1 / 3 / 3 |
| 110 | `python_109` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 111 | `python_110` | ❌ FAIL | ❌ FAIL | ✅ PASS | 1 / 3 / 5 |
| 112 | `python_111` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 113 | `python_112` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 114 | `python_113` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 115 | `python_114` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 116 | `python_115` | ✅ PASS | ✅ PASS | ❌ FAIL | 2 / 6 / 3 |
| 117 | `python_116` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 118 | `python_117` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 119 | `python_118` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 120 | `python_119` | ✅ PASS | ✅ PASS | ❌ FAIL | 2 / 6 / 3 |
| 121 | `python_120` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 122 | `python_121` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 123 | `python_122` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 124 | `python_123` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 125 | `python_124` | ❌ FAIL | ✅ PASS | ✅ PASS | 1 / 5 / 3 |
| 126 | `python_125` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 127 | `python_126` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 128 | `python_127` | ❌ FAIL | ❌ FAIL | ❌ FAIL | 1 / 3 / 14 |
| 129 | `python_128` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 130 | `python_129` | ❌ FAIL | ❌ FAIL | ✅ PASS | 2 / 6 / 3 |
| 131 | `python_130` | ❌ FAIL | ❌ FAIL | ❌ FAIL | 1 / 4 / 14 |
| 132 | `python_131` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 133 | `python_132` | ❌ FAIL | ❌ FAIL | ❌ FAIL | 1 / 5 / 3 |
| 134 | `python_133` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 135 | `python_134` | ❌ FAIL | ❌ FAIL | ❌ FAIL | 1 / 3 / 14 |
| 136 | `python_135` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 137 | `python_136` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 138 | `python_137` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 139 | `python_138` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 140 | `python_139` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 141 | `python_140` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 4 / 5 |
| 142 | `python_141` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 143 | `python_142` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 144 | `python_143` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 145 | `python_144` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 146 | `python_145` | ❌ FAIL | ❌ FAIL | ❌ FAIL | 1 / 3 / 14 |
| 147 | `python_146` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 148 | `python_147` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 149 | `python_148` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 150 | `python_149` | ❌ FAIL | ❌ FAIL | ✅ PASS | 2 / 6 / 3 |
| 151 | `python_150` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 152 | `python_151` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 153 | `python_152` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 154 | `python_153` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 155 | `python_154` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 156 | `python_155` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 157 | `python_156` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 158 | `python_157` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 159 | `python_158` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 160 | `python_159` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 161 | `python_160` | ❌ FAIL | ❌ FAIL | ❌ FAIL | 1 / 3 / 6 |
| 162 | `python_161` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 163 | `python_162` | ✅ PASS | ✅ PASS | ✅ PASS | 2 / 6 / 3 |
| 164 | `python_163` | ❌ FAIL | ❌ FAIL | ✅ PASS | 1 / 3 / 5 |
