from typing import List

def parse_nested_parens(paren_string: str) -> List[int]:
    def max_depth(s: str) -> int:
        depth = max_depth_so_far = 0
        for char in s:
            if char == '(':
                depth += 1
                max_depth_so_far = max(max_depth_so_far, depth)
            elif char == ')':
                depth -= 1
        return max_depth_so_far

    return [max_depth(group) for group in paren_string.split()]