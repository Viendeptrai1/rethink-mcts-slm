import sys

def max_tandem_repeat_length(s, k):
    n = len(s)
    max_length = 0
    
    # Check all possible substrings
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            doubled_substring = substring + substring
            if len(doubled_substring) <= n + k:
                max_length = max(max_length, len(doubled_substring))
    
    return max_length

# Read input
input = sys.stdin.read
data = input().split()
s = data[0]
k = int(data[1])

# Output the result
print(max_tandem_repeat_length(s, k))