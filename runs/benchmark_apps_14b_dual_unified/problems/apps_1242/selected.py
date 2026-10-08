def solve(s):
    n = len(s)
    result = [0] * n
    s = list(s)
    
    for i in range(n):
        if i == 0:
            if s[i] == 'b':
                result[i] = 1
                s[i] = 'a'
        else:
            if s[i] == 'b' and s[i-1] == 'a':
                result[i] = 1
                s[i], s[i-1] = s[i-1], s[i]
    
    return result

# Read input
import sys
input = sys.stdin.read().strip()
s = input

# Solve the problem
result = solve(s)

# Print the result
print(" ".join(map(str, result)))