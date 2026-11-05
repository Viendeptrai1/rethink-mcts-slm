# Báo cáo Đề tài: RethinkMCTS cho Mô hình Ngôn ngữ Nhỏ (7B–14B)

> Sườn báo cáo khoa học. Mỗi chương là một file riêng.
> Số liệu nào cũng phải có link tới artifact gốc. Chỗ chưa có số liệu ghi `TODO` và liên kết tới [EXPERIMENT_CHECKLIST.md](EXPERIMENT_CHECKLIST.md).

## Cấu trúc

| # | File | Nội dung | Trạng thái |
| :-: | :--- | :--- | :-: |
| 1 | [01_dat_van_de.md](01_dat_van_de.md) | Bối cảnh, vấn đề, câu hỏi nghiên cứu | Có sườn |
| 2 | [02_giai_phap.md](02_giai_phap.md) | Phương pháp RethinkMCTS và kiến trúc hệ thống | Có sườn |
| 3 | [03_thiet_lap_thuc_nghiem.md](03_thiet_lap_thuc_nghiem.md) | Dữ liệu, mô hình, siêu tham số, metric, baseline | Có sườn |
| 4 | [04_ket_qua_thuc_nghiem.md](04_ket_qua_thuc_nghiem.md) | Bảng kết quả (có sẵn và còn thiếu) | Thiếu một phần |
| 5 | [05_phan_tich_thao_luan.md](05_phan_tich_thao_luan.md) | Ablation, LLM Critic, scaling, phân loại lỗi | Thiếu nhiều |
| 6 | [06_han_che_va_huong_phat_trien.md](06_han_che_va_huong_phat_trien.md) | Hạn chế, threats to validity, hướng tiếp theo | Có sườn |
| ✓ | [EXPERIMENT_CHECKLIST.md](EXPERIMENT_CHECKLIST.md) | **Danh sách thực nghiệm cần chạy / cần phân tích** | Đang dùng |

Tài liệu phụ trợ (không thuộc chương chính):
- Kịch bản demo ứng dụng: [../demo_scenarios.md](../demo_scenarios.md)
- Báo cáo benchmark gốc 7B vs 14B: [../results/BENCHMARK_7B_VS_14B_REPORT.md](../results/BENCHMARK_7B_VS_14B_REPORT.md)
- Protocol thực nghiệm: [../research/PROTOCOL.md](../research/PROTOCOL.md)
- Giả thuyết RQ1–RQ3: [../research/HYPOTHESIS_LAB.md](../research/HYPOTHESIS_LAB.md)

## Quy ước

- `✅` có số liệu, đã đối chiếu artifact. `⏳` cần chạy thêm (tốn GPU). `🧮` chỉ cần phân tích offline trên artifact có sẵn. `⚠️` có số liệu nhưng không so sánh trực tiếp được.
- Không trộn kết quả của các cohort khác nhau vào cùng một bảng.
- Mỗi run mới dùng thư mục riêng `runs/<dataset>_<method>_<model>_<cohort>/`.

