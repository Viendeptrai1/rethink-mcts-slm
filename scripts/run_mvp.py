import os
import sys
import argparse
import logging
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.loader import get_mock_problem, load_code_contests
from data.schemas import Problem
from sandbox.executor import CodeExecutor
from sandbox.analyzer import FeedbackAnalyzer
from models.client import MockLLMClient, OpenAILLMClient
from mcts.search import RethinkMCTSEngine


def main():
    parser = argparse.ArgumentParser(description="Chạy thử nghiệm MVP RethinkMCTS trên bài toán lập trình.")
    parser.add_argument("--use-ollama", action="store_true", help="Sử dụng Ollama cục bộ (mặc định model qwen2.5-coder:7b).")
    parser.add_argument("--use-modal", action="store_true", help="Sử dụng vLLM API thực tế (từ Modal hoặc vLLM local).")
    parser.add_argument("--api-base", type=str, default=None, help="URL vLLM/Ollama API endpoint.")
    parser.add_argument("--model-name", type=str, default=None, help="Tên model phục vụ.")
    parser.add_argument("--rollouts", type=int, default=3, help="Số lượng rollouts tối đa cho MCTS.")
    parser.add_argument("--from-dataset", action="store_true", help="Tải bài từ deepmind/code_contests thay vì bài mẫu offline.")
    parser.add_argument("--min-rating", type=int, default=800, help="Rating tối thiểu Codeforces.")
    parser.add_argument("--max-rating", type=int, default=1200, help="Rating tối đa Codeforces.")
    parser.add_argument("--require-python3", action="store_true", default=True, help="Chỉ lấy bài có lời giải Python 3.")
    args = parser.parse_args()

    # Cấu hình logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    print("\n" + "="*80)
    print(" KHỞI CHẠY THỬ NGHIỆM MVP: RETHINK-MCTS FOR CODE GENERATION ")
    print("="*80)

    # 1. Tải bài toán
    if args.from_dataset:
        print(f"[1/4] Đang stream bài toán từ deepmind/code_contests (Rating {args.min_rating}-{args.max_rating}, Python 3={args.require_python3})...")
        problems = load_code_contests(
            split="valid",
            limit=1,
            streaming=True,
            require_python3=args.require_python3,
            min_rating=args.min_rating,
            max_rating=args.max_rating
        )
        problem = problems[0]
    else:
        print("[1/4] Sử dụng bài toán mẫu offline (Codeforces 4A - Watermelon)...")
        problem = get_mock_problem()

    print(f"-> Bài toán: {problem.title} (Source: {problem.source}, Rating: {problem.cf_rating})")
    print(f"-> Số test công khai (Public tests): {len(problem.public_tests)}")
    print(f"-> Số test ẩn (Private tests): {len(problem.private_tests)}")
    if problem.cf_tags:
        print(f"-> Tags: {', '.join(problem.cf_tags)}")

    # 2. Khởi tạo LLM Client
    print("\n[2/4] Khởi tạo mô hình ngôn ngữ...")
    if args.use_ollama:
        api_base = args.api_base or "http://localhost:11434/v1"
        model_name = args.model_name or "qwen2.5-coder:7b"
        print(f"-> Kết nối Ollama cục bộ: {api_base} (Model: {model_name})")
        client = OpenAILLMClient(api_base=api_base, api_key="ollama", model_name=model_name)
    elif args.use_modal:
        api_base = args.api_base or "http://localhost:8000/v1"
        model_name = args.model_name or "Qwen/Qwen2.5-Coder-7B-Instruct"
        print(f"-> Kết nối vLLM endpoint: {api_base} (Model: {model_name})")
        client = OpenAILLMClient(api_base=api_base, model_name=model_name)
    else:
        print("-> Sử dụng MockLLMClient (Mô phỏng tư duy & cơ chế Rethink nội bộ)...")
        client = MockLLMClient()

    # 3. Khởi tạo Sandbox & MCTS Engine
    print("\n[3/4] Khởi tạo Sandbox thực thi và Động cơ RethinkMCTS...")
    timeout = max(2.0, (problem.time_limit or 1.0) * 2.5)
    print(f"-> Thiết lập timeout sandbox cho Python: {timeout:.1f}s")
    executor = CodeExecutor(timeout=timeout)
    analyzer = FeedbackAnalyzer()
    engine = RethinkMCTSEngine(
        client=client,
        executor=executor,
        analyzer=analyzer,
        max_rollouts=args.rollouts,
        max_children=3,
        c_base=10.0,
        c=4.0,
        reward_a=0.8,
        reward_b=0.2
    )

    # 4. Tiến hành tìm kiếm MCTS
    print("\n[4/4] Bắt đầu tìm kiếm cây và tự sửa lỗi...")
    best_code, best_reward, program_dict, root = engine.search(problem)

    print("\n" + "="*80)
    print(" KẾT QUẢ THỰC NGHIỆM TÌM KIẾM MCTS ")
    print("="*80)
    print(f"Tổng số giải pháp được đánh giá trong cây: {len(program_dict)}")
    print(f"Điểm thưởng cao nhất đạt được (trên Public Tests): {best_reward:.3f}")

    print("\n--- MÃ NGUỒN TỐI ƯU TÌM ĐƯỢC ---")
    print(best_code)

    # 5. Đánh giá tính tổng quát hóa trên tập Private Tests ẩn
    print("\n" + "-"*80)
    print(" KIỂM THỬ TRÊN TẬP TEST ẨN (PRIVATE TESTS EVALUATION) ")
    print("-"*80)
    eval_tests = problem.private_tests[:10] if problem.private_tests else problem.public_tests
    private_eval = executor.evaluate_code(best_code, eval_tests)
    print(f"Kết quả (trên {len(eval_tests)} test ẩn): {'CHÍNH XÁC HOÀN TOÀN (ACCEPTED)' if private_eval.all_passed else 'CÓ TEST THẤT BẠI'}")
    print(f"Tỷ lệ vượt qua (Pass Rate): {private_eval.passed_count}/{private_eval.total_count} ({private_eval.pass_rate*100:.1f}%)")

    for i, res in enumerate(private_eval.test_results):
        status_symbol = "✓" if res.status.value == "ACCEPTED" else "✗"
        inp_str = res.input.strip().replace("\n", " ")
        if len(inp_str) > 40:
            inp_str = inp_str[:40] + "..."
        exp_str = res.expected_output.strip().replace("\n", " ")
        if len(exp_str) > 30:
            exp_str = exp_str[:30] + "..."
        act_str = res.actual_output.strip().replace("\n", " ")
        if len(act_str) > 30:
            act_str = act_str[:30] + "..."
        print(f"  Test #{i+1} [{status_symbol} {res.status.value}]: Input='{inp_str}' -> Expected='{exp_str}', Got='{act_str}'")

    print("\n" + "="*80)
    print(" HOÀN TẤT THỬ NGHIỆM TRÊN TẬP DEEPMIND CODECONTESTS ")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
