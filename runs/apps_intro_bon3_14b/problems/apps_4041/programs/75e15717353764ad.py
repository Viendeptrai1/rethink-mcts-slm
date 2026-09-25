import sys

def max_substring_to_remove(s, t):
    # Initialize pointers for s and t
    i, j = 0, 0
    n, m = len(s), len(t)
    
    # Find the longest prefix of t that is a subsequence of s
    while i < n and j < m:
        if s[i] == t[j]:
            j += 1
        i += 1
    
    # If we matched the entire t, no need to remove anything
    if j == m:
        return 0
    
    # Now, find the longest suffix of t that is a subsequence of s
    i, j = n - 1, m - 1
    while i >= 0 and j >= 0:
        if s[i] == t[j]:
            j -= 1
        i -= 1
    
    # Calculate the maximum length of substring to remove
    prefix_length = j + 1
    suffix_length = m - (j + 1)
    
    return n - (prefix_length + suffix_length)

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_substring_to_remove(s, t))