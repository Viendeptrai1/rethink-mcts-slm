def check_syntax(input_string):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for i, char in enumerate(input_string):
        if char in mapping.values():
            stack.append(char)
        elif char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return f"{char} {i}"
    
    if stack:
        return "ok so far"
    
    return "ok so far"

# Read input from stdin
import sys
input_string = sys.stdin.read().strip()

# Get the length of the string
length = int(input_string.split('\n')[0])

# Get the actual input string
program = input_string.split('\n')[1]

# Check syntax and print the result
result = check_syntax(program)
print(result)