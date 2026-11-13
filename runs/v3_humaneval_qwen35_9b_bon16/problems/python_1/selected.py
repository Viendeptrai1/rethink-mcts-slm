from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    result: List[str] = []
    current_group: str = ""
    balance: int = 0

    # Remove all spaces from the input string
    paren_string = paren_string.replace(" ", "")

    for char in paren_string:
        if char == '(':
            current_group += char
            balance += 1
        elif char == ')':
            current_group += char
            balance -= 1

        # If balance returns to zero, we've found a complete group
        if balance == 0:
            result.append(current_group)
            current_group = ""

    return result