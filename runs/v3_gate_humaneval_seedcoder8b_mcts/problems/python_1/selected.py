from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    paren_string = paren_string.replace(" ", "")
    result = []
    current_group = []
    stack = []

    for char in paren_string:
        if char == '(':
            stack.append(char)
            current_group.append(char)
        elif char == ')':
            if stack:
                stack.pop()
                current_group.append(char)
                if not stack:
                    result.append(''.join(current_group))
                    current_group = []
            else:
                # Unbalanced closing parenthesis, reset current group
                current_group = []

    return result