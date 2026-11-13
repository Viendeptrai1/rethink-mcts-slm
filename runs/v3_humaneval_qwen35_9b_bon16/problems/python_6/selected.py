from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    groups = paren_string.split()
    result = []
    for group in groups:
        level = 0
        max_level = 0
        for char in group:
            if char == '(':
                level += 1
                if level > max_level:
                    max_level = level
            elif char == ')':
                level -= 1
        result.append(max_level)
    return result