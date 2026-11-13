from typing import List

def parse_nested_parens(paren_string: str) -> List[int]:
    def max_depth(s: str) -> int:
        current_depth = 0
        max_depth = 0
        for char in s:
            if char == '(':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == ')':
                current_depth -= 1
        return max_depth

    groups = paren_string.split()
    return [max_depth(group) for group in groups]