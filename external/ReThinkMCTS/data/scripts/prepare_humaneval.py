from datasets import load_dataset
import os

DATA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUMANEVAL_DIR = os.path.join(DATA_ROOT, "humaneval")
os.makedirs(HUMANEVAL_DIR, exist_ok=True)

humaneval_path = os.path.join(HUMANEVAL_DIR, "arrow")

if os.path.exists(humaneval_path):
    print(f"Da co HumanEval tai: {humaneval_path}")
else:
    print("Dang tai HumanEval...")
    humaneval = load_dataset("openai/openai_humaneval")
    humaneval.save_to_disk(humaneval_path)
    print(f"Xong HumanEval, luu tai: {humaneval_path}")

humaneval = load_dataset("openai/openai_humaneval")
print("\n=== Thong tin dataset ===")
print(humaneval)
print("\n=== Bai mau dau tien ===")
print(humaneval["test"][0])
