def min_lexicographical_string(s):
    stack = []
    result = []
    
    for char in s:
        while stack and stack[-1] < char:
            result.append(stack.pop())
        stack.append(char)
    
    while stack:
        result.append(stack.pop())
    
    return ''.join(result)

# Input reading
import sys
input = sys.stdin.read
data = input().split()

# Processing and output
print(min_lexicographical_string(data[0]))