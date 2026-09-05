import logging
from typing import List, Optional
from .schemas import Problem, TestCase

logger = logging.getLogger(__name__)


def _to_str(val) -> str:
    """Chuyển đổi bytes hoặc object sang string chuẩn utf-8."""
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace")
    return str(val) if val is not None else ""


def parse_code_contests_entry(item: dict) -> Problem:
    """Chuyển đổi một bản ghi từ deepmind/code_contests sang schema Problem."""
    # Xử lý public tests
    pub_tests = []
    if "public_tests" in item and item["public_tests"]:
        inputs = item["public_tests"].get("input", [])
        outputs = item["public_tests"].get("output", [])
        for inp, out in zip(inputs, outputs):
            pub_tests.append(TestCase(input=_to_str(inp), output=_to_str(out)))

    # Xử lý private tests
    priv_tests = []
    if "private_tests" in item and item["private_tests"]:
        inputs = item["private_tests"].get("input", [])
        outputs = item["private_tests"].get("output", [])
        for inp, out in zip(inputs, outputs):
            priv_tests.append(TestCase(input=_to_str(inp), output=_to_str(out)))

    # Xử lý generated tests
    gen_tests = []
    if "generated_tests" in item and item["generated_tests"]:
        inputs = item["generated_tests"].get("input", [])
        outputs = item["generated_tests"].get("output", [])
        for inp, out in zip(inputs, outputs):
            gen_tests.append(TestCase(input=_to_str(inp), output=_to_str(out)))

    cf_rating = item.get("cf_rating")
    if cf_rating is not None and int(cf_rating) <= 0:
        cf_rating = None

    # Xử lý solutions & incorrect_solutions (HuggingFace lưu dạng dict: {'language': [...], 'solution': [...]})
    def _extract_sols(data):
        res = []
        if isinstance(data, dict):
            langs = data.get("language", [])
            codes = data.get("solution", [])
            for l, c in zip(langs, codes):
                res.append({"language": l, "solution": _to_str(c)})
        elif isinstance(data, list):
            for item_sol in data:
                if isinstance(item_sol, dict):
                    res.append({"language": item_sol.get("language"), "solution": _to_str(item_sol.get("solution"))})
        return res

    solutions = _extract_sols(item.get("solutions"))
    incorrect_solutions = _extract_sols(item.get("incorrect_solutions"))
    cf_tags = item.get("cf_tags", [])
    time_limit = item.get("time_limit")
    if isinstance(time_limit, dict):
        time_limit = time_limit.get("seconds", 2.0)

    return Problem(
        id=str(item.get("name", "unknown_id")),
        title=_to_str(item.get("name", "Untitled")),
        description=_to_str(item.get("description", "")),
        public_tests=pub_tests,
        private_tests=priv_tests,
        generated_tests=gen_tests,
        source=str(item.get("source", "")),
        difficulty=str(item.get("difficulty", "")),
        cf_rating=cf_rating,
        cf_tags=[_to_str(t) for t in cf_tags] if isinstance(cf_tags, list) else [],
        time_limit=float(time_limit) if time_limit else 2.0,
        solutions=solutions,
        incorrect_solutions=incorrect_solutions
    )


def has_python3_solution(problem: Problem) -> bool:
    """Kiểm tra bài toán có ít nhất 1 bài nộp Python 3 (language=3) đúng hay không."""
    for sol in problem.solutions:
        # Schema CodeContests: 1=PYTHON2, 2=CPP, 3=PYTHON3, 4=JAVA
        lang = sol.get("language")
        if lang in (3, "PYTHON3", "PYTHON_3"):
            return True
    return False


def load_code_contests(
    split: str = "valid",
    limit: int = 5,
    streaming: bool = True,
    require_python3: bool = False,
    min_rating: Optional[int] = None,
    max_rating: Optional[int] = None
) -> List[Problem]:
    """
    Tải bài toán từ HuggingFace `deepmind/code_contests`.
    Hỗ trợ lọc bài có Python 3 solution và theo dải rating Codeforces.
    """
    try:
        from datasets import load_dataset
        logger.info(f"Đang tải bài toán từ deepmind/code_contests (split={split}, require_py3={require_python3})...")
        ds = load_dataset("deepmind/code_contests", split=split, streaming=streaming)
        problems = []
        for item in ds:
            prob = parse_code_contests_entry(item)
            if require_python3 and not has_python3_solution(prob):
                continue
            if min_rating is not None and (prob.cf_rating is None or prob.cf_rating < min_rating):
                continue
            if max_rating is not None and (prob.cf_rating is None or prob.cf_rating > max_rating):
                continue
            problems.append(prob)
            if len(problems) >= limit:
                break
        return problems if problems else [get_mock_problem()]
    except Exception as e:
        logger.warning(f"Không thể tải từ HuggingFace ({e}). Sử dụng bài toán mẫu dự phòng.")
        return [get_mock_problem()]


def get_mock_problem() -> Problem:
    """
    Bài toán mẫu ngoại tuyến chuẩn format Competitive Programming (Codeforces 4A - Watermelon)
    để kiểm thử toàn bộ pipeline mà không cần kết nối mạng.
    """
    desc = """One hot summer day Pete and his friend Billy decided to buy a watermelon. They chose the biggest and the ripest one, in their opinion. After that the watermelon was weighed, and the scales showed w kilos. They rushed home, dying of thirst, and decided to divide the berry, however they faced a hard problem.

Pete and Billy are great fans of even numbers, that's why they want to divide the watermelon in such a way that each of the two parts weighs even number of kilos, at the same time it is not obligatory that the parts are equal. The boys are extremely tired and want to start their meal as soon as possible, that's why you should help them: check if they can divide the watermelon in the way they want. For sure, each of them should get a part of positive weight.

Input
The first (and the only) input line contains integer number w (1 <= w <= 100) — the weight of the watermelon bought by the boys.

Output
Print YES, if the boys can divide the watermelon into two parts, each of them weighing even number of kilos; and NO in the opposite case."""

    return Problem(
        id="cf_4a_watermelon",
        title="4A. Watermelon",
        description=desc,
        public_tests=[
            TestCase(input="8\n", output="YES\n"),
            TestCase(input="2\n", output="NO\n")
        ],
        private_tests=[
            TestCase(input="3\n", output="NO\n"),
            TestCase(input="4\n", output="YES\n"),
            TestCase(input="5\n", output="NO\n"),
            TestCase(input="6\n", output="YES\n"),
            TestCase(input="100\n", output="YES\n")
        ],
        source="CODEFORCES",
        difficulty="EASY",
        cf_rating=800
    )
