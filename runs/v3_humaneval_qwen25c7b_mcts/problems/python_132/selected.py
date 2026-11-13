def is_nested(s):
    max_depth = 0
    current_depth = 0
    
    for char in s:
        if char == '[':
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == ']':
            current_depth -= 1
        
        # If current_depth goes negative, it means there's an unmatched closing bracket
        if current_depth < 0:
            return False
    
    # If max_depth is greater than 1, there is at least one nested pair
    return max_depth > 1