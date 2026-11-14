# Tiểu luận chuyên ngành (LaTeX)

Project LaTeX của tiểu luận chuyên ngành (Bộ môn Trí tuệ nhân tạo, Khoa CNTT, ĐH Công nghệ Kỹ thuật TP.HCM, trước đây là ĐH Sư phạm Kỹ thuật TP.HCM).
Trình bày theo file mẫu quy cách khóa luận của khoa: [mau/Mau-5-TrinhBay-KLTN.docx](mau/Mau-5-TrinhBay-KLTN.docx).

## Biên dịch

Cần XeLaTeX và Biber (TeX Live), cùng các font Times New Roman và STIX Two Math (có sẵn trên macOS).

```bash
cd thesis
make          # xelatex → biber → xelatex ×2, ra main.pdf
make clean    # xóa file trung gian
```

`main.pdf` và các file trung gian không được commit (`.gitignore`).

## Cấu trúc

| File / thư mục | Nội dung |
|---|---|
| `main.tex` | File chính: thứ tự các phần theo mục 1–2 của file mẫu |
| `tlcn.sty` | Toàn bộ quy cách trình bày (lề, font, cỡ chữ, đề mục, hình, bảng, tài liệu tham khảo) |
| `thongtin.tex` | Tên trường, bộ môn, sinh viên, MSSV, GVHD, khóa |
| `truocnoidung/` | Bìa chính, bìa phụ, phiếu nhận xét GVHD/GVPB, lời cảm ơn, đề cương, chữ viết tắt, tóm tắt |
| `chuong/` | Phần mở đầu, Chương 1–5, Phần kết luận |
| `phuluc/` | Phụ lục A, B |
| `tailieu.bib` | Tài liệu tham khảo (chỉ mục nào được `\cite` mới được in) |
| `hinh/` | Hình riêng của báo cáo. `hinh/logo-cntt.png`: logo Khoa CNTT (FIT HCM-UTE), dùng trên bìa theo mẫu. `hinh/logo-truong.png`: logo trường (HCM-UTE, PNG 203×257 từ Wikimedia Commons), để dự phòng |
| `decuong/` | Đặt bản scan đề cương có chữ ký GVHD ở `decuong/decuong-ky.pdf` |

Hình kết quả không chép vào đây: `\graphicspath` trỏ thẳng tới `../docs/report/figures/v3/`
(sinh bằng `scripts/make_figures_v3.py`), nên hình trong báo cáo luôn khớp với artifact.

## Quy cách đã cài đặt (theo file mẫu, mục 3)

| Yêu cầu | Cách làm trong `tlcn.sty` |
|---|---|
| A4 đứng; lề trên 2, dưới 2, trái 3, phải 2 cm | `geometry` |
| Times New Roman, nội dung cỡ 13, canh đều | `fontspec`, lớp `scrreprt` với `fontsize=13pt` |
| Dãn dòng 1.5 lines | `\setstretch{1.44}` (tương đương 1.5 lines của Word với Times New Roman, xem chú thích trong file) |
| Tên chương: 14, in hoa, đậm, giữa | dạng `CHƯƠNG 1: TÊN CHƯƠNG` |
| Tiểu mục mức 1: 13, in hoa, đậm, trái | `\section` (2.1) |
| Tiểu mục mức 2: 13, thường, đậm, trái | `\subsection` (2.1.1) |
| Tiểu mục mức 3: 13, thường, nghiêng, trái | `\subsubsection`, không đánh số (tối đa ba chữ số) |
| Bảng: 12, giữa; tên bảng 11 đậm, trên bảng | `table` + `\caption` đặt **trước** `tabular` |
| Chú thích bảng: 10, nghiêng, giữa, dưới bảng | `\ghichubang{...}` |
| Tên hình: 11, đậm, giữa, dưới hình | `figure` + `\caption` đặt **sau** `\includegraphics` |
| Tài liệu tham khảo: 11, thường, trái; đánh số theo thứ tự từ điển | `biblatex` (`sorting=nyt`), các thành phần cách nhau bằng dấu phẩy |
| Số trang ở giữa, bên dưới | Kiểu trang `plain`; phần đầu đánh số La Mã, nội dung đánh số Ả-rập từ Phần mở đầu |

Lưu ý khi viết:

- **Thuật ngữ:** dùng "LLM" làm thuật ngữ chung (khớp tên đề tài); ba mô hình gọi là "LLM mở cỡ nhỏ (7–9B tham số)", không dùng "SLM" như một định nghĩa.
- **Tên chương và tiểu mục mức 1 viết bằng chữ in hoa ngay trong mã nguồn** (`\chapter{CƠ SỞ LÝ THUYẾT}`, `\section{KIẾN TRÚC TỔNG THỂ}`), để mục lục cũng in hoa giống đề mục.
- Phần mở đầu và Phần kết luận không đánh số chương: dùng `\addchap` và `\addsec`.
- Ô màu cam "Cần viết" (`\lipsumtodo{...}`) là chỗ giữ chỗ; xóa khi viết xong.
- Mọi con số trong báo cáo lấy từ `docs/results/BENCHMARK_LEDGER.md` hoặc `docs/results/v3/`. Nguồn **không in ra** trong báo cáo: ghi bằng comment `% Nguồn: ...` ngay cạnh bảng/hình/đoạn văn để truy vết.
- Viết về cách làm và kết quả của nhóm; không trình bày theo kiểu đối chiếu "bài báo làm thế này, chúng tôi làm thế kia".
- Ba cảnh báo còn lại khi biên dịch là vô hại: `typearea` (lề do `geometry` đặt), `csquotes` chưa cài, và không có mẫu ngắt từ tiếng Việt (đã tắt ngắt từ có chủ ý).

## Đối chiếu với khung báo cáo

Khung nội dung: [docs/report/KHUNG_BAO_CAO_v2.md](../docs/report/KHUNG_BAO_CAO_v2.md). Do mẫu của khoa có Phần mở đầu và Phần kết luận riêng, các chương được sắp lại:

| Khung v2 | Tiểu luận |
|---|---|
| Chương 1. Đặt vấn đề | Phần mở đầu (`chuong/mo-dau.tex`) |
| Chương 2. Cơ sở lý thuyết và phương pháp | Chương 1 (lý thuyết) và Chương 2 (thiết kế, cài đặt) |
| Chương 3. Thiết lập thực nghiệm | Chương 3 |
| Chương 4. Kết quả chính | Chương 4 |
| Chương 5. Phân tích | Chương 5 (kèm các yếu tố ảnh hưởng đến tính hợp lệ) |
| Chương 6. Hạn chế và hướng phát triển | Phần kết luận |
| Phụ lục A, B | Phụ lục A, B |
