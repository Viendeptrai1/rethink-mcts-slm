# APPS 300 Benchmark: Kế hoạch Thực nghiệm (7B vs 14B)

* **Tập dữ liệu:** 300 bài APPS (100 Introductory, 100 Interview, 100 Competition).
* **Phương pháp lấy mẫu:** Stratified Random Sampling từ 5.000 bài test gốc của APPS (Hugging Face), cố định `seed = 2027`.
* **File danh sách bài (Cohort):** [`data/cohorts/apps_benchmark_300.json`](file:///Users/kotori/Documents/TLCN/data/cohorts/apps_benchmark_300.json)

---

## 1. Danh mục 300 Bài toán (`seed=2027`)

| Tầng độ khó | Số lượng | Dải ID bài toán | Test Cases |
| :--- | :---: | :---: | :--- |
| **Introductory** | 100 bài | `apps_4005` $\to$ `apps_4842` | 200 public + 1.258 hidden |
| **Interview** | 100 bài | `apps_51` $\to$ `apps_2879` | 200 public + 2.414 hidden |
| **Competition** | 100 bài | `apps_3013` $\to$ `apps_3990` | 200 public + 1.684 hidden |
| **Tổng cộng** | **300 bài** | *(Rải đều từ 5.000 bài gốc)* | **600 public + 5.356 hidden** |

---

## 2. Phân chia Công việc (7B vs 14B)

Cả 2 người chạy trên **cùng một tập 300 bài** để đối đầu trực tiếp:

* **Thành viên 1 (Bạn):** Chạy **14B** với [`configs/benchmark_apps_14b.yaml`](file:///Users/kotori/Documents/TLCN/configs/benchmark_apps_14b.yaml).
* **Thành viên 2 (Bạn của bạn):** Chạy **7B** với [`configs/benchmark_apps_7b.yaml`](file:///Users/kotori/Documents/TLCN/configs/benchmark_apps_7b.yaml).

### Chia 3 đợt chạy (Batch) để kiểm soát rủi ro:
1. **Batch 1 (Introductory - 100 bài):** Chạy trước (~1.5h - 2h) để test thông suốt toàn bộ hệ thống.
2. **Batch 2 (Interview - 100 bài):** Trọng tâm đánh giá giải thuật (~2.5h - 3.5h).
3. **Batch 3 (Competition - 100 bài):** Đo trần suy luận của mô hình (~3h - 4h).

---

## 3. Lệnh Thực thi

### Bước 1: Deploy Endpoint vLLM (Modal)

```bash
# Cho luồng 14B:
modal deploy deploy/modal_vllm.py

# Cho luồng 7B:
MODAL_APP_NAME="rethink-vllm-7b" VLLM_MODEL_ID="Qwen/Qwen2.5-Coder-7B-Instruct" modal deploy deploy/modal_vllm.py
```

### Bước 2: Chạy Benchmark

#### Cách A: Chạy Full 300 bài (1 lệnh duy nhất)
```bash
# 14B:
python scripts/run_benchmark_batch.py \
  --config configs/benchmark_apps_14b.yaml \
  --problem-ids @data/cohorts/apps_benchmark_300.json \
  --output-dir runs/benchmark_apps_300_14b

# 7B:
python scripts/run_benchmark_batch.py \
  --config configs/benchmark_apps_7b.yaml \
  --problem-ids @data/cohorts/apps_benchmark_300.json \
  --output-dir runs/benchmark_apps_300_7b
```

#### Cách B: Chạy theo từng Độ khó (Batch)
```bash
# Ví dụ chạy Batch 1 (Introductory):
python scripts/run_benchmark_batch.py --config configs/benchmark_apps_14b.yaml --difficulty introductory --output-dir runs/benchmark_apps_14b_intro

# Ví dụ chạy Batch 2 (Interview):
python scripts/run_benchmark_batch.py --config configs/benchmark_apps_14b.yaml --difficulty interview --output-dir runs/benchmark_apps_14b_interview

# Ví dụ chạy Batch 3 (Competition):
python scripts/run_benchmark_batch.py --config configs/benchmark_apps_14b.yaml --difficulty competition --output-dir runs/benchmark_apps_14b_competition
```

---

## 4. Dự toán Chi phí Modal

* **Mô hình 7B:** ~$3.5 - $4.5 (thời gian ~5h).
* **Mô hình 14B:** ~$4.5 - $6.0 (thời gian ~6h).
* **Tổng cộng 2 bên:** ~$8.0 - $10.5 *(Số dư khả dụng hiện có: ~$98.41)*.

---

## 5. Đoạn văn đưa vào Luận văn (Phương pháp luận)

> *"Nghiên cứu đánh giá thuật toán Rethink-MCTS trên tập kiểm thử gồm 300 bài toán từ bộ dữ liệu APPS (Hendrycks et al., 2021). Nhằm loại bỏ thiên kiến đồng cụm (Clustering Bias) của việc lấy mẫu tuần tự, chúng tôi áp dụng phương pháp lấy mẫu ngẫu nhiên phân tầng không hoàn lại (Stratified Uniform Random Sampling) với hạt giống cố định `seed=2027` trên toàn bộ 5.000 bài toán thuộc tập test gốc. Mẫu thu được gồm 100 bài Nhập môn (apps_4005 đến apps_4842), 100 bài Phỏng vấn (apps_51 đến apps_2879) và 100 bài Thi đấu (apps_3013 đến apps_3990). Toàn bộ bài toán được cố định tại `data/cohorts/apps_benchmark_300.json` nhằm đảm bảo khả năng tái lập thực nghiệm 100%."*
