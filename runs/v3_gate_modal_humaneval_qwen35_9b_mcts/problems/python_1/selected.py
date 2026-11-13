from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    # Remove all spaces from the input string
    paren_string = paren_string.replace(" ", "")
    
    result: List[str] = []
    current_group: str = ""
    balance: int = 0
    
    for char in paren_string:
        if char == '(':
            balance += 1
            current_group += char
        elif char == ')':
            balance -= 1
            current_group += char
            
            # If balance returns to zero, we have a complete group
            if balance == 0:
                result.append(current_group)
                current_group = ""
    
    return result