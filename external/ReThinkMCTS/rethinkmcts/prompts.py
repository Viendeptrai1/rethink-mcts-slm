from __future__ import annotations


def _problem_header(statement: str, starter_code: str = "") -> str:
    extra = f"\n\nStarter code:\n{starter_code.rstrip()}" if starter_code.strip() else ""
    return f"Problem statement:\n{statement.rstrip()}{extra}"


def _interface_instruction(dataset: str, function_name: str | None = None) -> str:
    if dataset != "apps":
        return ""
    if function_name:
        return (
            f"\n\nExecution interface: call-based. Define `{function_name}` as a top-level "
            "function or a method on `Solution`; the judge calls it with the test arguments. "
            "Return the result instead of printing it."
        )
    return (
        "\n\nExecution interface: standard input/output. The judge runs the source as a "
        "standalone Python program. Read from stdin, invoke your solution for the "
        "provided input, and print the answer to stdout. A function definition by "
        "itself produces no output and fails the tests."
    )


def expand_prompt(
    statement: str,
    thoughts: list[str],
    *,
    feedback: str | None = None,
    width: int = 3,
    starter_code: str = "",
    dataset: str = "",
    function_name: str | None = None,
) -> str:
    history = "\n".join(f"{index + 1}. {thought}" for index, thought in enumerate(thoughts)) or "(none)"
    feedback_text = f"\n\nExecution feedback:\n{feedback}" if feedback else ""
    return (
        "You are the reasoning planner for a code-generation search.\n"
        f"{_problem_header(statement, starter_code)}"
        f"{_interface_instruction(dataset, function_name)}\n\n"
        f"Previous thoughts:\n{history}{feedback_text}\n\n"
        f"Produce exactly {width} distinct next reasoning strategies. Do not write code. "
        "Return only a JSON list. Each item must contain a short `thought` string and a "
        "`reasonableness` number in [0, 1]. The numbers should sum to 1."
    )


def code_prompt(
    statement: str,
    thoughts: list[str],
    *,
    starter_code: str = "",
    dataset: str = "",
    function_name: str | None = None,
) -> str:
    history = "\n".join(f"{index + 1}. {thought}" for index, thought in enumerate(thoughts)) or "(none)"
    return (
        "You are an expert Python programmer.\n"
        f"{_problem_header(statement, starter_code)}"
        f"{_interface_instruction(dataset, function_name)}\n\n"
        f"Reasoning path:\n{history}\n\n"
        "Return only the complete Python solution. Include imports and the required function "
        "signature when the task is call-based. Do not explain the solution and do not use "
        "Markdown fences."
    )


def self_evaluation_prompt(statement: str, thoughts: list[str], code: str) -> str:
    history = "\n".join(f"{index + 1}. {thought}" for index, thought in enumerate(thoughts)) or "(none)"
    return (
        "You are a strict code correctness evaluator.\n"
        f"Problem statement:\n{statement.rstrip()}\n\n"
        f"Reasoning path:\n{history}\n\n"
        f"Candidate code:\n```python\n{code.rstrip()}\n```\n\n"
        "The candidate already passes all public tests. Estimate whether it passes unseen "
        "edge cases. Return only JSON with one numeric key `evaluation` in [-1, 1]."
    )


def feedback_prompt(
    statement: str,
    thoughts: list[str],
    code: str,
    failed_test: str,
    trace_text: str,
    *,
    dataset: str = "",
    function_name: str | None = None,
) -> str:
    history = "\n".join(f"{index + 1}. {thought}" for index, thought in enumerate(thoughts)) or "(none)"
    interface_check = (
        "First check that the code follows the execution interface. If stdout is empty "
        "but output is expected, identify a missing driver or print call before analyzing "
        "the algorithm. Use `block`: `interface` when no code block was executed incorrectly. "
        if dataset == "apps" and not function_name else ""
    )
    return (
        "You are a code debugger performing block-level analysis.\n"
        f"Problem statement:\n{statement.rstrip()}"
        f"{_interface_instruction(dataset, function_name)}\n\n"
        f"Reasoning path:\n{history}\n\n"
        f"Candidate code:\n```python\n{code.rstrip()}\n```\n\n"
        f"Failed public test:\n{failed_test}\n\n"
        f"Execution trace by AST statement block:\n{trace_text}\n\n"
        f"{interface_check}"
        "Identify the first incorrect block using the trace. Return JSON containing "
        "`block`, `correct`, and `explanation`. Do not rewrite the code."
    )


def rethink_prompt(
    statement: str,
    thoughts: list[str],
    code: str,
    feedback: str,
    *,
    dataset: str = "",
    function_name: str | None = None,
) -> str:
    history = "\n".join(f"Thought-{index + 1}: {thought}" for index, thought in enumerate(thoughts)) or "(none)"
    return (
        "You are refining one erroneous reasoning step in a code-generation search.\n"
        f"Problem statement:\n{statement.rstrip()}"
        f"{_interface_instruction(dataset, function_name)}\n\n"
        f"Thoughts:\n{history}\n\n"
        f"Generated code:\n```python\n{code.rstrip()}\n```\n\n"
        f"Execution feedback:\n{feedback}\n\n"
        "Replace only the most recent thought with a better reasoning step that avoids the "
        "observed error. Return one or two sentences of thought only, never code."
    )
