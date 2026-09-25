import sys

def max_substring_to_remove(s, t):
    n, m = len(s), len(t)
    
    # Find the longest prefix of s that matches t
    prefix_match = 0
    j = 0
    for i in range(n):
        if j < m and s[i] == t[j]:
            j += 1
        prefix_match += 1
        if j == m:
            break
    
    # Find the longest suffix of s that matches t
    suffix_match = 0
    j = m - 1
    for i in range(n - 1, -1, -1):
        if j >= 0 and s[i] == t[j]:
            j -= 1
        suffix_match += 1
        if j == -1:
            break
    
    # The maximum length of the substring we can remove
    return n - max(prefix_match, suffix_match)

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_substring_to_remove(s, t))