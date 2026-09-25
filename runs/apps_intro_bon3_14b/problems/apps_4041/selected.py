import sys

def max_substring_to_remove(s, t):
    # Initialize pointers for s and t
    i, j = 0, 0
    n, m = len(s), len(t)
    
    # Find the longest prefix of s that matches t
    while i < n and j < m:
        if s[i] == t[j]:
            j += 1
        i += 1
    
    # The length of the matching prefix
    prefix_length = j
    
    # Reset pointers for s and t
    i, j = n - 1, m - 1
    
    # Find the longest suffix of s that matches t
    while i >= 0 and j >= 0:
        if s[i] == t[j]:
            j -= 1
        i -= 1
    
    # The length of the matching suffix
    suffix_length = m - j - 1
    
    # If the entire t is matched in s, no removal is needed
    if prefix_length == m:
        return 0
    
    # Calculate the maximum length of substring to remove
    max_remove = max(prefix_length + (n - suffix_length - m), n - m)
    
    return max_remove

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_substring_to_remove(s, t))