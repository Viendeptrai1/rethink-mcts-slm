import sys

def solve(s):
    n = len(s)
    result = [0] * n
    
    # Convert the string to a list for easier manipulation
    s = list(s)
    
    for i in range(n):
        # Check if reversing the prefix (0 to i) will make the string lexicographically smaller
        if i > 0 and s[i] < s[i - 1]:
            # Reverse the prefix
            s[:i + 1] = reversed(s[:i + 1])
            result[i] = 1
    
    return result

# Read input
input = sys.stdin.read
data = input().strip()

# Solve the problem
output = solve(data)

# Print the result
print(" ".join(map(str, output)))