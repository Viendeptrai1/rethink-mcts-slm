import sys

def max_removable_substring(s, t):
    n, m = len(s), len(t)
    i, j = 0, 0
    last_match = -1
    max_remove = 0
    
    # Find all matches of t in s
    matches = []
    while i < n and j < m:
        if s[i] == t[j]:
            matches.append(i)
            j += 1
        i += 1
    
    # Calculate the maximum removable substring length
    if matches:
        # Check the segment before the first match
        max_remove = max(max_remove, matches[0])
        
        # Check the segments between consecutive matches
        for k in range(1, len(matches)):
            max_remove = max(max_remove, matches[k] - matches[k-1] - 1)
        
        # Check the segment after the last match
        max_remove = max(max_remove, n - 1 - matches[-1])
    
    return max_remove

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_removable_substring(s, t))