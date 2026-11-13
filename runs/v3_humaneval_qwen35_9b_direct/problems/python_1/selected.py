from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
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
            # If balance returns to zero, we have a complete group
            if balance == 0:
                result.append(current_group)
                current_group = ""

    return result