from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    paren_string = paren_string.replace(" ", "")  # Remove spaces from the input string
    result = []
    stack = []
    start_index = None

    for i, char in enumerate(paren_string):
        if char == '(':
            if not stack:
                start_index = i
            stack.append(i)
        elif char == ')':
            if stack:
                stack.pop()
                if not stack:
                    result.append(paren_string[start_index:i+1])

    return result