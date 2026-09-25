def is_nested(string):
    depth = 0
    max_depth = 0
    
    for char in string:
        if char == '[':
            depth += 1
            max_depth = max(max_depth, depth)
        elif char == ']':
            depth -= 1
        
        # If depth goes negative, it means there are unmatched closing brackets
        if depth < 0:
            return False
    
    # Check if there was any nesting (max_depth > 1)
    return max_depth > 1