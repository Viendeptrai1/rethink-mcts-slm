import sys

def max_removable_substring(s, t):
    n, m = len(s), len(t)
    t_index = 0
    last_match = -1
    
    # Find all matches of t in s
    matches = []
    for i in range(n):
        if t_index < m and s[i] == t[t_index]:
            matches.append(i)
            t_index += 1
    
    # Calculate the maximum removable length
    max_remove = matches[0]  # Length of substring before the first match
    for i in range(1, len(matches)):
        max_remove = max(max_remove, matches[i] - matches[i-1] - 1)
    
    max_remove = max(max_remove, n - matches[-1] - 1)  # Length of substring after the last match
    
    return max_remove

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_removable_substring(s, t))