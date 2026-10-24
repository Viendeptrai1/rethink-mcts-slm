from datasets import load_dataset
import os
import json
import shutil

# Thu muc data/ nam ngay tren scripts/.
DATA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(DATA_ROOT, "apps")
os.makedirs(APPS_DIR, exist_ok=True)

# codeparrot/apps dung dataset loading script (apps.py), khong con duoc ho tro
# tu datasets>=4.0 -> phai tro thang toi cac file parquet trong thu muc "all/"
# cua nhanh refs/convert/parquet (HF tu sinh san cho cac dataset script cu).
# LUU Y: neu goi load_dataset("codeparrot/apps", revision="refs/convert/parquet")
# KHONG chi dinh file cu the, datasets se gom luon ca 3 thu muc con
# introductory/, interview/, competition/ (von la ban chia nho trung lap cua
# chinh "all/") -> bi NHAN DOI du lieu (train/test thanh 10000 thay vi 5000).
APPS_PARQUET_FILES = {
    "train": "hf://datasets/codeparrot/apps@refs/convert/parquet/all/train/0000.parquet",
    "test": [
        "hf://datasets/codeparrot/apps@refs/convert/parquet/all/test/0000.parquet",
        "hf://datasets/codeparrot/apps@refs/convert/parquet/all/test/0001.parquet",
    ],
}


def load_apps_hf():
    return load_dataset("parquet", data_files=APPS_PARQUET_FILES)


# APPS raw co cau truc thu muc ma repo RethinkMCTS goc can.
# File tar.gz goc (people.eecs.berkeley.edu/~hendrycks/APPS.tar.gz) da 404,
# khong con tai duoc (da kiem tra: server tra 404 Not Found that, khong phai
# loi mang tam thoi). Thay vao do, TU DUNG lai dung cau truc thu muc ma
# APPSHandler.py (repo goc) can, tu du lieu HuggingFace tai tam thoi:
# codeparrot/apps chua day du, khong thieu field nao so voi ban raw goc:
#   question      -> question.txt
#   solutions     -> solutions.json   (chuoi JSON, ghi thang ra)
#   input_output  -> input_output.json (chuoi JSON, ghi thang ra, co fn_name neu call-based)
#   starter_code  -> starter_code.py  (chi ghi neu khong rong)
#   difficulty    -> metadata.json
apps_raw_dir = os.path.join(APPS_DIR, "raw")


def build_apps_raw(apps_hf):
    for split in ["train", "test"]:
        for row in apps_hf[split]:
            prob_dir = os.path.join(apps_raw_dir, split, f"{row['problem_id']:04d}")
            os.makedirs(prob_dir, exist_ok=True)

            with open(os.path.join(prob_dir, "question.txt"), "w", encoding="utf-8") as f:
                f.write(row["question"])

            with open(os.path.join(prob_dir, "solutions.json"), "w", encoding="utf-8") as f:
                f.write(row["solutions"] or "[]")

            with open(os.path.join(prob_dir, "input_output.json"), "w", encoding="utf-8") as f:
                f.write(row["input_output"] or "{}")

            if row["starter_code"]:
                with open(os.path.join(prob_dir, "starter_code.py"), "w", encoding="utf-8") as f:
                    f.write(row["starter_code"])

            with open(os.path.join(prob_dir, "metadata.json"), "w", encoding="utf-8") as f:
                json.dump(
                    {"difficulty": row["difficulty"], "url": row["url"]}, f, ensure_ascii=False
                )


if os.path.exists(apps_raw_dir):
    print(f"Da co APPS (raw) tai: {apps_raw_dir}, bo qua.")
else:
    print("Dang dung lai APPS (raw) tu du lieu HuggingFace...")
    apps_hf = load_apps_hf()
    try:
        build_apps_raw(apps_hf)
    except Exception:
        # dung do lo loi -> xoa sach de lan chay sau tu lam lai tu dau,
        # tranh de lai thu muc "coi nhu da xong" (check os.path.exists) nhung thieu du lieu
        shutil.rmtree(apps_raw_dir, ignore_errors=True)
        raise
    print(f"Xong APPS (raw), dung vao: {apps_raw_dir}")
