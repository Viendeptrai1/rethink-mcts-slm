from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    groups = paren_string.split()
    result = []
    
    for group in groups:
        current_depth = 0
        max_depth = 0
        for char in group:
            if char == '(':
                current_depth += 1
                if current_depth > max_depth:
                    max_depth = current_depth
            elif char == ')':
                current_depth -= 1
        result.append(max_depth)
    
    return result