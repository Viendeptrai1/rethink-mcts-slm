# BÁO CÁO TỔNG HỢP THỰC NGHIỆM BENCHMARK TRÊN TẬP DỮ LIỆU APPS (INTRODUCTORY)
## Đề tài: Tối Ưu Hóa Tìm Kiếm Suy Luận Cho Mô Hình Ngôn Ngữ Nhỏ Trong Lập Trình (TLCN)

- **Ngày hoàn thành thực nghiệm**: 13/09/2026
- **Mô hình thử nghiệm**: `Qwen/Qwen2.5-Coder-14B-Instruct` (14.7B parameters, bfloat16, Trọng số CỐ ĐỊNH - Frozen Weights)
- **Hạ tầng tính toán**: NVIDIA H200 SXM (141GB VRAM) trên Modal Cloud (vLLM v0.29.0, FlashAttention-3)
- **Bộ dữ liệu**: APPS (Tập Introductory: 100 bài toán thuật toán từ `apps_4000` đến `apps_4099`, chấm độc lập qua Hidden Judge)

---

## 1. Tóm Tắt Kết Quả Thực Nghiệm Cốt Lõi

| Chỉ số (Metric) | 1. Direct Baseline (Greedy) | 2. Best-of-3 Baseline | 3. RethinkMCTS (Đề xuất) |
| :--- | :---: | :---: | :---: |
| **Tỷ lệ Pass@1 (100% Test Ẩn)** | **21.00%** | **23.00%** | **30.00%** 🏆 |
| **Số bài Giải Đúng Hoàn Toàn** | 21 / 100 | 23 / 100 | **30 / 100** |
| **Tỷ lệ Pass Test Ẩn Trung Bình (Mean HPR)** | 38.89% | 44.87% | **49.88%** 🏆 |
| **Tổng Số Lượt Gọi Mô Hình** | 127 | 379 | 1158 |
| **Hiệu quả Mẫu (Avg Calls/Bài)** | 1.27 | 3.79 | 11.58 |
| **Mức Tăng Trưởng so với Direct** | Mốc chuẩn (Baseline) | +2.00% (+2 bài) | **+9.00% (+9 bài)** |
| **Số bài MCTS sửa thành công từ bài Direct giải sai** | - | 4 / 79 | **11 / 79** 🎯 |
| **Số bài MCTS giải đúng độc nhất (Cả Direct & BoN3 đều sai)** | - | - | **10 bài** 💎 |

---

## 2. Danh Sách Bài Toán MCTS Đột Phá So Với Baseline

- **Các bài MCTS sửa thành công mà Direct thất bại (11 bài)**: `apps_4015`, `apps_4016`, `apps_4017`, `apps_4022`, `apps_4048`, `apps_4055`, `apps_4060`, `apps_4064`, `apps_4075`, `apps_4089`, `apps_4095`
- **Các bài MCTS giải đúng độc quyền mà cả Direct và Best-of-3 đều thất bại (10 bài)**: `apps_4015`, `apps_4016`, `apps_4017`, `apps_4022`, `apps_4048`, `apps_4055`, `apps_4060`, `apps_4064`, `apps_4075`, `apps_4095`

## 3. Bảng Chi Tiết Từng Bài Toán (Per-Problem Breakdown)

| Problem ID | Direct Pass@1 | Direct HPR | BoN-3 Pass@1 | BoN-3 HPR | MCTS Pass@1 | MCTS HPR | MCTS Calls | Ưu thế MCTS |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `apps_4000` | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | 20 |  |
| `apps_4001` | ❌ FAIL | 2.9% | ❌ FAIL | 3.7% | ❌ FAIL | 40.1% | 20 | 📈 HPR cao hơn |
| `apps_4002` | ❌ FAIL | 13.8% | ❌ FAIL | 3.8% | ❌ FAIL | 48.1% | 17 | 📈 HPR cao hơn |
| `apps_4003` | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | ❌ FAIL | 2.1% | 20 | 📈 HPR cao hơn |
| `apps_4004` | ❌ FAIL | 47.1% | ❌ FAIL | 49.0% | ❌ FAIL | 45.8% | 5 |  |
| `apps_4005` | ❌ FAIL | 81.1% | ❌ FAIL | 78.0% | ❌ FAIL | 86.4% | 3 | 📈 HPR cao hơn |
| `apps_4006` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4007` | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | 17 |  |
| `apps_4008` | ❌ FAIL | 14.3% | ❌ FAIL | 14.3% | ❌ FAIL | 19.4% | 20 | 📈 HPR cao hơn |
| `apps_4009` | ❌ FAIL | 26.8% | ✅ PASS | 100.0% | ❌ FAIL | 74.2% | 3 |  |
| `apps_4010` | ❌ FAIL | 69.8% | ❌ FAIL | 70.8% | ❌ FAIL | 88.5% | 9 | 📈 HPR cao hơn |
| `apps_4011` | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | ❌ FAIL | 18.4% | 20 | 📈 HPR cao hơn |
| `apps_4012` | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | ❌ FAIL | 2.5% | 20 | 📈 HPR cao hơn |
| `apps_4013` | ✅ PASS | 100.0% | ❌ FAIL | 26.3% | ✅ PASS | 100.0% | 5 |  |
| `apps_4014` | ❌ FAIL | 16.0% | ❌ FAIL | 29.3% | ❌ FAIL | 33.3% | 3 | 📈 HPR cao hơn |
| `apps_4015` | ❌ FAIL | 93.3% | ❌ FAIL | 93.3% | ✅ PASS | 100.0% | 8 | 💎 Độc quyền MCTS |
| `apps_4016` | ❌ FAIL | 11.0% | ❌ FAIL | 41.1% | ✅ PASS | 100.0% | 5 | 💎 Độc quyền MCTS |
| `apps_4017` | ❌ FAIL | 63.8% | ❌ FAIL | 63.8% | ✅ PASS | 100.0% | 9 | 💎 Độc quyền MCTS |
| `apps_4018` | ❌ FAIL | 25.0% | ❌ FAIL | 20.6% | ❌ FAIL | 19.1% | 20 |  |
| `apps_4019` | ❌ FAIL | 1.4% | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | 20 |  |
| `apps_4020` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4021` | ❌ FAIL | 9.7% | ❌ FAIL | 8.1% | ❌ FAIL | 6.5% | 3 |  |
| `apps_4022` | ❌ FAIL | 0.0% | ❌ FAIL | 25.0% | ✅ PASS | 100.0% | 8 | 💎 Độc quyền MCTS |
| `apps_4023` | ❌ FAIL | 56.1% | ❌ FAIL | 75.4% | ❌ FAIL | 36.8% | 3 |  |
| `apps_4024` | ❌ FAIL | 26.3% | ❌ FAIL | 33.3% | ❌ FAIL | 35.1% | 17 | 📈 HPR cao hơn |
| `apps_4025` | ❌ FAIL | 1.9% | ❌ FAIL | 1.9% | ❌ FAIL | 3.7% | 18 | 📈 HPR cao hơn |
| `apps_4026` | ❌ FAIL | 48.1% | ❌ FAIL | 53.7% | ❌ FAIL | 55.6% | 3 | 📈 HPR cao hơn |
| `apps_4027` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4028` | ❌ FAIL | 18.0% | ❌ FAIL | 22.0% | ❌ FAIL | 14.0% | 20 |  |
| `apps_4029` | ❌ FAIL | 24.0% | ❌ FAIL | 22.0% | ❌ FAIL | 34.0% | 20 | 📈 HPR cao hơn |
| `apps_4030` | ❌ FAIL | 23.4% | ❌ FAIL | 23.4% | ❌ FAIL | 23.4% | 20 |  |
| `apps_4031` | ❌ FAIL | 89.4% | ❌ FAIL | 89.4% | ❌ FAIL | 89.4% | 20 |  |
| `apps_4032` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4033` | ❌ FAIL | 58.7% | ❌ FAIL | 41.3% | ❌ FAIL | 41.3% | 8 |  |
| `apps_4034` | ❌ FAIL | 4.3% | ❌ FAIL | 41.3% | ❌ FAIL | 41.3% | 20 |  |
| `apps_4035` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4036` | ❌ FAIL | 2.3% | ❌ FAIL | 25.0% | ❌ FAIL | 25.0% | 20 |  |
| `apps_4037` | ❌ FAIL | 77.3% | ❌ FAIL | 77.3% | ❌ FAIL | 52.3% | 20 |  |
| `apps_4038` | ❌ FAIL | 44.2% | ❌ FAIL | 16.3% | ❌ FAIL | 4.7% | 20 |  |
| `apps_4039` | ❌ FAIL | 74.4% | ❌ FAIL | 74.4% | ❌ FAIL | 4.7% | 5 |  |
| `apps_4040` | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | ❌ FAIL | 72.1% | 20 | 📈 HPR cao hơn |
| `apps_4041` | ❌ FAIL | 7.1% | ❌ FAIL | 7.1% | ❌ FAIL | 66.7% | 20 | 📈 HPR cao hơn |
| `apps_4042` | ❌ FAIL | 2.4% | ❌ FAIL | 2.4% | ❌ FAIL | 2.4% | 20 |  |
| `apps_4043` | ❌ FAIL | 6.5% | ❌ FAIL | 0.0% | ❌ FAIL | 41.3% | 20 | 📈 HPR cao hơn |
| `apps_4044` | ❌ FAIL | 0.0% | ❌ FAIL | 4.9% | ❌ FAIL | 2.4% | 20 |  |
| `apps_4045` | ❌ FAIL | 27.5% | ❌ FAIL | 0.0% | ❌ FAIL | 32.5% | 20 | 📈 HPR cao hơn |
| `apps_4046` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 5 |  |
| `apps_4047` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4048` | ❌ FAIL | 2.6% | ❌ FAIL | 15.4% | ✅ PASS | 100.0% | 13 | 💎 Độc quyền MCTS |
| `apps_4049` | ❌ FAIL | 0.0% | ❌ FAIL | 10.5% | ❌ FAIL | 10.5% | 3 |  |
| `apps_4050` | ❌ FAIL | 2.6% | ❌ FAIL | 0.0% | ❌ FAIL | 10.5% | 20 | 📈 HPR cao hơn |
| `apps_4051` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ❌ FAIL | 71.1% | 5 |  |
| `apps_4052` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4053` | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | ❌ FAIL | 2.7% | 20 | 📈 HPR cao hơn |
| `apps_4054` | ❌ FAIL | 13.5% | ❌ FAIL | 13.5% | ❌ FAIL | 10.8% | 20 |  |
| `apps_4055` | ❌ FAIL | 61.1% | ❌ FAIL | 47.2% | ✅ PASS | 100.0% | 8 | 💎 Độc quyền MCTS |
| `apps_4056` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4057` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 5 |  |
| `apps_4058` | ❌ FAIL | 45.7% | ❌ FAIL | 34.3% | ❌ FAIL | 40.0% | 8 |  |
| `apps_4059` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ❌ FAIL | 0.0% | 3 |  |
| `apps_4060` | ❌ FAIL | 3.0% | ❌ FAIL | 0.0% | ✅ PASS | 100.0% | 13 | 💎 Độc quyền MCTS |
| `apps_4061` | ❌ FAIL | 42.4% | ❌ FAIL | 42.4% | ❌ FAIL | 33.3% | 9 |  |
| `apps_4062` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4063` | ❌ FAIL | 28.1% | ❌ FAIL | 28.1% | ❌ FAIL | 28.1% | 20 |  |
| `apps_4064` | ❌ FAIL | 41.9% | ❌ FAIL | 41.9% | ✅ PASS | 100.0% | 5 | 💎 Độc quyền MCTS |
| `apps_4065` | ❌ FAIL | 43.3% | ❌ FAIL | 43.3% | ❌ FAIL | 43.3% | 3 |  |
| `apps_4066` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4067` | ❌ FAIL | 10.3% | ❌ FAIL | 6.9% | ❌ FAIL | 27.6% | 20 | 📈 HPR cao hơn |
| `apps_4068` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4069` | ❌ FAIL | 6.9% | ❌ FAIL | 75.9% | ❌ FAIL | 24.1% | 3 |  |
| `apps_4070` | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | 20 |  |
| `apps_4071` | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | 20 |  |
| `apps_4072` | ❌ FAIL | 60.7% | ❌ FAIL | 60.7% | ❌ FAIL | 42.9% | 5 |  |
| `apps_4073` | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | 20 |  |
| `apps_4074` | ❌ FAIL | 32.1% | ❌ FAIL | 32.1% | ❌ FAIL | 32.1% | 20 |  |
| `apps_4075` | ❌ FAIL | 17.9% | ❌ FAIL | 17.9% | ✅ PASS | 100.0% | 6 | 💎 Độc quyền MCTS |
| `apps_4076` | ❌ FAIL | 10.7% | ❌ FAIL | 10.7% | ❌ FAIL | 10.7% | 20 |  |
| `apps_4077` | ❌ FAIL | 0.0% | ❌ FAIL | 29.6% | ❌ FAIL | 51.9% | 20 | 📈 HPR cao hơn |
| `apps_4078` | ❌ FAIL | 44.4% | ❌ FAIL | 22.2% | ❌ FAIL | 25.9% | 20 |  |
| `apps_4079` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4080` | ❌ FAIL | 22.2% | ❌ FAIL | 22.2% | ❌ FAIL | 18.5% | 20 |  |
| `apps_4081` | ❌ FAIL | 11.1% | ❌ FAIL | 37.0% | ❌ FAIL | 3.7% | 14 |  |
| `apps_4082` | ❌ FAIL | 55.6% | ❌ FAIL | 55.6% | ❌ FAIL | 48.1% | 14 |  |
| `apps_4083` | ❌ FAIL | 44.4% | ❌ FAIL | 63.0% | ❌ FAIL | 63.0% | 14 |  |
| `apps_4084` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4085` | ❌ FAIL | 19.2% | ❌ FAIL | 19.2% | ❌ FAIL | 0.0% | 5 |  |
| `apps_4086` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4087` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
| `apps_4088` | ❌ FAIL | 0.0% | ❌ FAIL | 34.6% | ❌ FAIL | 0.0% | 14 |  |
| `apps_4089` | ❌ FAIL | 3.8% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 6 | ⭐ Sửa lỗi Direct |
| `apps_4090` | ❌ FAIL | 0.0% | ❌ FAIL | 68.0% | ❌ FAIL | 4.0% | 14 |  |
| `apps_4091` | ❌ FAIL | 16.0% | ❌ FAIL | 16.0% | ❌ FAIL | 52.0% | 14 | 📈 HPR cao hơn |
| `apps_4092` | ❌ FAIL | 16.0% | ❌ FAIL | 20.0% | ❌ FAIL | 16.0% | 3 |  |
| `apps_4093` | ❌ FAIL | 0.0% | ❌ FAIL | 24.0% | ❌ FAIL | 0.0% | 14 |  |
| `apps_4094` | ❌ FAIL | 28.0% | ❌ FAIL | 52.0% | ❌ FAIL | 0.0% | 8 |  |
| `apps_4095` | ❌ FAIL | 0.0% | ❌ FAIL | 0.0% | ✅ PASS | 100.0% | 13 | 💎 Độc quyền MCTS |
| `apps_4096` | ❌ FAIL | 29.2% | ❌ FAIL | 29.2% | ❌ FAIL | 29.2% | 14 |  |
| `apps_4097` | ❌ FAIL | 0.0% | ❌ FAIL | 75.0% | ❌ FAIL | 66.7% | 14 |  |
| `apps_4098` | ❌ FAIL | 8.3% | ✅ PASS | 100.0% | ❌ FAIL | 58.3% | 6 |  |
| `apps_4099` | ✅ PASS | 100.0% | ✅ PASS | 100.0% | ✅ PASS | 100.0% | 3 |  |
