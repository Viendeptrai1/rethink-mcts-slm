def can_rearrange_to_smaller(s, t):
    return sorted(s) < sorted(t)

# Read input from standard input
import sys
input = sys.stdin.read
data = input().split()

# Extract the strings s and t
s = data[0]
t = data[1]

# Determine if it's possible to rearrange s' < t'
result = "Yes" if can_rearrange_to_smaller(s, t) else "No"

# Print the result
print(result)