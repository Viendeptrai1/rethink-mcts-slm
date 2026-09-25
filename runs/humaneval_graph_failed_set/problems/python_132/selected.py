def is_nested(string):
    # Edge case: if the string is empty or has less than 2 characters, return False
    if len(string) < 2:
        return False
    
    # Initialize a stack to keep track of open brackets
    stack = []
    # Flag to check if we have seen a nested bracket
    has_nested = False
    
    for char in string:
        if char == '[':
            stack.append(char)
        elif char == ']':
            if not stack:
                # Unmatched closing bracket
                return False
            stack.pop()
            # If stack is not empty after popping, it means we had a nested structure
            if stack:
                has_nested = True
    
    # If stack is not empty, it means there are unmatched opening brackets
    if stack:
        return False
    
    return has_nested