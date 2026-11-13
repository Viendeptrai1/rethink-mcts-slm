def find_substring_to_reverse(s):
    n = len(s)
    
    # Iterate over all possible substrings
    for i in range(n):
        for j in range(i + 2, n + 1):  # At least 2 characters to reverse
            reversed_substring = s[:i] + s[i:j][::-1] + s[j:]
            if reversed_substring < s:
                return "YES", i + 1, j
    
    return "NO"

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
s = data[1]

# Find and print result
result = find_substring_to_reverse(s)
print(result[0], *result[1:]) if isinstance(result, tuple) else print(result)