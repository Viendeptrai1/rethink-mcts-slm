import sys

def max_substring_to_remove(s, t):
    n, m = len(s), len(t)
    # Create a list to store the indices of characters in s that match t
    match_indices = []
    
    # Fill match_indices with the indices of characters in s that match t
    j = 0
    for i in range(n):
        if j < m and s[i] == t[j]:
            match_indices.append(i)
            j += 1
    
    # If t is an empty string or matches the entire s, no removal is needed
    if not match_indices or match_indices[-1] == n - 1:
        return 0
    
    # Calculate the maximum length of substring that can be removed
    max_length = 0
    
    # Check the prefix part
    max_length = max(max_length, match_indices[0])
    
    # Check the suffix part
    max_length = max(max_length, n - 1 - match_indices[-1])
    
    # Check the middle parts
    for i in range(1, len(match_indices)):
        max_length = max(max_length, match_indices[i] - match_indices[i - 1] - 1)
    
    return max_length

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_substring_to_remove(s, t))