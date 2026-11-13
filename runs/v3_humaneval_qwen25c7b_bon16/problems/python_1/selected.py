from typing import *
from collections import *

def separate_paren_groups(paren_string: str) -> List[str]:
    paren_string = paren_string.replace(' ', '')
    result = []
    current_group = []
    depth = 0

    for char in paren_string:
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        current_group.append(char)
        if depth == 0:
            result.append(''.join(current_group))
            current_group = []

    return result