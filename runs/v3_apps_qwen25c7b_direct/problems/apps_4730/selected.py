def check_delimiters(input_string):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    
    for i, char in enumerate(input_string):
        if char in mapping.values():
            stack.append((char, i))
        elif char in mapping.keys():
            if not stack or stack[-1][0] != mapping[char]:
                return f"{char} {i}"
            stack.pop()
    
    if stack:
        return f"{stack[-1][0]} {stack[-1][1]}"
    
    return "ok so far"

# Example usage:
import sys
input_string = sys.stdin.read().strip()
print(check_delimiters(input_string))