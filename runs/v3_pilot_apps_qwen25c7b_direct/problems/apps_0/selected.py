def max_accordion_length(s):
    stack = []
    for char in s:
        if char == '[':
            stack.append(char)
        elif char == ']':
            if not stack or stack[-1] != '[':
                return -1
            stack.pop()
        elif char == ':' and len(stack) >= 2 and stack[-1] == '[' and stack[-2] == ':':
            stack.pop()
            stack.pop()
            stack.append(':')
        elif char == '|' and len(stack) >= 2 and stack[-1] == ':' and stack[-2] == ':':
            stack.pop()
            stack.pop()
            stack.append('|')
    if len(stack) != 2 or stack[0] != '[' or stack[1] != ']':
        return -1
    return 2 + sum(c == '|' for c in s if c == '|')

# Example usage:
import sys
input = sys.stdin.read
data = input().strip()
print(max_accordion_length(data))