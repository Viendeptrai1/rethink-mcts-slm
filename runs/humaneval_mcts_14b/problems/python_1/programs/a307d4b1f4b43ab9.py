from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    result = []
    current_group = []
    balance = 0
    
    for char in paren_string:
        if char == ' ':
            continue
        current_group.append(char)
        
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        
        if balance == 0 and current_group:
            result.append(''.join(current_group))
            current_group = []
    
    return result

# Example usage:
# print(separate_paren_groups('( ) (( )) (( )( ))'))  # Output: ['()', '(())', '(()())']