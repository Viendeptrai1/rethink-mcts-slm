import sys

def max_substring_to_remove(s, t):
    n, m = len(s), len(t)
    
    # Find the longest prefix of s that matches t
    prefix_match = 0
    for i in range(n):
        if prefix_match < m and s[i] == t[prefix_match]:
            prefix_match += 1
    
    # Find the longest suffix of s that matches t
    suffix_match = 0
    for i in range(n - 1, -1, -1):
        if suffix_match < m and s[i] == t[m - 1 - suffix_match]:
            suffix_match += 1
    
    # Calculate the maximum length of substring that can be removed
    max_remove = 0
    if prefix_match + suffix_match > m:
        max_remove = n - (prefix_match + suffix_match - m)
    
    return max_remove

# Read input
input = sys.stdin.read
data = input().split()
s = data[0]
t = data[1]

# Output the result
print(max_substring_to_remove(s, t))