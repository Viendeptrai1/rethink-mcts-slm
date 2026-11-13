def check_error(t):
    n = len(t)
    for i in range(1, n // 2 + 1):
        if t[:i] == t[i:i+i]:
            return "YES", t[:i]
    return "NO", ""

# Read input from stdin
import sys
input = sys.stdin.read().strip()

# Process the input and get the result
result, message = check_error(input)

# Print the result
print(result)
if result == "YES":
    print(message)