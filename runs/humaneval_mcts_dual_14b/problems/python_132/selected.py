def is_nested(string):
    max_depth = 0
    current_depth = 0
    
    for char in string:
        if char == '[':
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == ']':
            current_depth -= 1
            if current_depth < 0:
                return False
    
    return max_depth > 1