def validate_delimiters(L):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    
    for i, char in enumerate(L):
        if char in mapping.values():
            stack.append(char)
        elif char in mapping.keys():
            if not stack or stack.pop() != mapping[char]:
                return f"{char} {i}"
    
    if stack:
        return "ok so far"
    else:
        return "ok so far"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
L = data[1]
print(validate_delimiters(L))