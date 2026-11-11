from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    result = []
    current_group = []
    open_count = 0
    
    for char in paren_string.replace(" ", ""):
        if char == '(':
            open_count += 1
            current_group.append(char)
        elif char == ')':
            open_count -= 1
            current_group.append(char)
        
        if open_count == 0 and current_group:
            result.append(''.join(current_group))
            current_group = []
    
    return result