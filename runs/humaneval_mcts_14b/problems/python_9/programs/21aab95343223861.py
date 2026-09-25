from typing import List


def rolling_max(numbers: List[int]) -> List[int]:
    if not numbers:
        return []

    max_stack = []
    result = []

    for i, num in enumerate(numbers):
        while max_stack and num > max_stack[-1][0]:
            max_stack.pop()
        max_stack.append((num, i))
        result.append(max_stack[0][0])

    return result