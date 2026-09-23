"""
Execution harnesses for stdin, function, class_method, and assertion_suite modes (§4.1).
"""

import json
from typing import Any
from rethink_mcts.domain.problem import ExecutionMode, ExecutionSpec, TestCase, StdinCase, FunctionCase, AssertionSuite


def wrap_code_for_execution(code: str, test_case: TestCase, spec: ExecutionSpec) -> str:
    """
    Wraps candidate code with harness logic if mode is function or class_method.
    For stdin mode, returns candidate code unmodified.
    """
    if isinstance(test_case, AssertionSuite):
        return f"{code}\n\n# --- Assertion Suite Harness ---\n{test_case.test_code}\n"

    if isinstance(test_case, FunctionCase):
        # Generate wrapper that imports or defines function, calls with args/kwargs, and prints JSON output
        entry_point = spec.entry_point or test_case.entry_point
        args_json = json.dumps(list(test_case.args))
        kwargs_json = json.dumps(dict(test_case.kwargs))

        wrapper = f"""{code}

if __name__ == '__main__':
    import json, sys
    try:
        args = json.loads({repr(args_json)})
        kwargs = json.loads({repr(kwargs_json)})
        fn = globals().get({repr(entry_point)})
        if fn is None and 'Solution' in globals():
            fn = getattr(Solution(), {repr(entry_point)}, None)
        if fn is None:
            sys.stderr.write(f"Entry point '{entry_point}' not found in candidate code.\\n")
            sys.exit(1)
        res = fn(*args, **kwargs)
        print(json.dumps(res))
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
"""
        return wrapper

    return code
