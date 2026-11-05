# Kịch bản Demo Ứng dụng Thực tế & Hướng dẫn Trình diễn Luận văn
## Đề tài: RethinkMCTS trên Mô hình Nhỏ (7B–14B)

Tài liệu này ghi lại các phương án thiết kế kịch bản demo ứng dụng thực tế nhằm tối ưu hóa tính thuyết phục, tạo "khoảnh khắc ấn tượng" (Aha-moment) khi bảo vệ trước Hội đồng chấm Luận văn / Khóa luận tốt nghiệp (TLCN) hoặc trình diễn sản phẩm cho người dùng cuối.

---

## 1. Đặt vấn đề: "Công cụ Nghiên cứu" vs "Ứng dụng Thực tế"

| Tiêu chí | Công cụ Nghiên cứu (`Trace Viewer` hiện tại) | Ứng dụng Thực tế (Product / End-User Demo) |
| :--- | :--- | :--- |
| **Mục đích** | Mở nắp capo (Under-the-hood): kiểm tra thuật toán, UCB score, cây MCTS, từng rollout. | Giải quyết trực tiếp bài toán của người dùng: sửa lỗi mã nguồn, giải thuật toán phức tạp. |
| **Đối tượng** | Tác giả mô hình, nhà nghiên cứu AI/NLP. | Lập trình viên, học viên luyện code, hội đồng đánh giá tính ứng dụng. |
| **Trọng tâm hiển thị** | Cấu trúc cây, Q-value, log JSON, rollout sequence. | Code Editor, kết quả kiểm thử (Pass/Fail), so sánh hiệu quả rõ ràng. |

> **Nguyên tắc vàng khi Demo:** 
> Đi từ **giá trị người dùng (User Value)** trước, sau đó mới dẫn chứng bằng **nguyên lý thuật toán (Algorithmic Proof)**.

---

## 2. Ba Kịch bản Demo Ứng dụng Thực tế Đề xuất

### 🎯 Kịch bản 1: Chế độ Đối đầu A/B (Side-by-Side: SLM Thuần vs SLM + RethinkMCTS)
*Đây là kịch bản mang tính thuyết phục cao nhất trong buổi báo cáo.*

* **Giao diện:** Màn hình chia đôi (Split View):
  * **Cột trái — Base SLM (Qwen2.5-Coder-7B chạy Direct Sampling / Self-Refine):**
    * Sinh mã nguồn ngay lập tức.
    * Khi chạy sandbox: **Thất bại** (dính `IndexError`, sai edge case hoặc rơi vào vòng lặp sửa mù quáng lặp lại lỗi cũ).
  * **Cột phải — SLM + RethinkMCTS (Cùng model Qwen2.5-Coder-7B):**
    * Phân tích bài toán thành từng bước tư duy (`Thought 1`, `Thought 2`).
    * Khi gặp lỗi kiểm thử: hệ thống tự động bắt lỗi từ execution trace, kích hoạt **Rethink Leaf**, giữ nguyên các bước đúng và chỉ sửa bước sai.
    * Kết quả: **Pass 100% test cases**.
* **Thông điệp cốt lõi:**
  > *"Không cần chi trả chi phí lớn cho API của các mô hình khổng lồ (GPT-4 / Claude 3.5 Sonnet), chỉ với một mô hình 7B gọn nhẹ chạy cục bộ (Ollama) kết hợp thuật toán RethinkMCTS, hệ thống hoàn toàn vượt qua các bài toán thuật toán hóc búa."*

---

### 🎯 Kịch bản 2: AI Pair Programmer tự sửa lỗi mã nguồn (Self-Healing Code)
*Ứng dụng thực tiễn trong quy trình phát triển phần mềm (CI/CD hoặc IDE Plugin).*

* **Luồng tương tác:**
  1. Người dùng nhập:
     * Đoạn code đang phát triển (đang có bug logic tiềm ẩn).
     * Bộ unit test hiện tại (có 1-2 test cases bị FAIL).
  2. Người dùng nhấn: **"Tự động sửa lỗi với RethinkMCTS"**.
  3. Hệ thống tiến hành:
     * Chạy Sandbox cô lập, trích xuất Basic-Block CFG và snapshot biến runtime lúc xảy ra lỗi.
     * Sinh giả thuyết sửa đổi và đưa ra bản vá (Git Diff).
  4. Người dùng xem bản so sánh (Before/After) kèm giải thích lý do sửa và trạng thái kiểm thử chuyển sang xanh (All Tests Passed).

---

### 🎯 Kịch bản 3: Competitive Programming & Phỏng vấn Thuật toán (LeetCode Assistant)
*Ứng dụng hỗ trợ học tập và chuẩn bị phỏng vấn kỹ thuật.*

* **Luồng tương tác:**
  * Nhập đề bài (ví dụ từ APPS hoặc bài toán LeetCode Medium/Hard).
  * Hệ thống xuất ra:
    1. Chuỗi phân tích tư duy từng bước (Thought Process).
    2. Mã nguồn tối ưu có chú thích rõ ràng.
    3. Báo cáo kiểm thử tự động trên tập public test cases.
  * Tích hợp nút bấm mở rộng: **"🔍 Xem cây suy luận MCTS"** $\rightarrow$ Dẫn trực tiếp vào **Trace Viewer** để minh họa chi tiết đường đi tìm kiếm nghiệm tối ưu.

---

## 3. Cấu trúc Luồng Thuyết trình 3 Bước Chuẩn Hội đồng (10–15 phút)

```text
[BƯỚC 1: ĐẶT VẤN ĐỀ] (2-3 phút)
  └─ Cho model nhỏ (7B) giải một bài toán thực tế ──> Code bị lỗi / sửa loanh quanh thất bại.
  
[BƯỚC 2: TRÌNH DIỄN GIẢI PHÁP] (5-7 phút)
  └─ Kích hoạt RethinkMCTS (Kịch bản 1: Đối đầu A/B) ──> Hệ thống tự phản hồi, tự sửa và đạt PASS 100%.

[BƯỚC 3: CHỨNG MINH KHOA HỌC] (3-5 phút)
  └─ Mở "nắp capo" qua Trace Viewer ──> Giải thích cơ chế UCB, Selection, và Leaf Revision đã cứu vãn quá trình suy luận như thế nào.
```

---

## 4. Lộ trình Triển khai Đề xuất (Next Steps)

1. **Backend Integration:**
   * Tận dụng các endpoints sẵn có của module `rethink_mcts` và `server.py`.
   * Thêm 1 API endpoint đơn giản `POST /api/solve/custom` nhận đề bài tùy ý hoặc code + test case tự do.
2. **Frontend UI:**
   * Xây dựng một tab giao diện **"Playground / Duel View"** cạnh tab **"Trace Viewer"** hiện tại.
   * Giao diện gồm 2 khung code và bảng trạng thái test trực quan.

