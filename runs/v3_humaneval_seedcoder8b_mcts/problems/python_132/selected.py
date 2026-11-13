def is_nested(string):
    stack = []
    nested = False
    
    for char in string:
        if char == '[':
            stack.append(char)
        elif char == ']':
            if not stack:
                return False
            stack.pop()
            if stack:
                nested = True
    
    return nested