def can_rearrange(s, t):
    return any(s[i] < t[j] for i in range(len(s)) for j in range(len(t)))

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Get the strings
s = data[0]
t = data[1]

# Determine if it's possible to satisfy s' < t'
result = "Yes" if can_rearrange(s, t) else "No"

# Print the result
print(result)