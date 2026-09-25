import sys

def max_substring_removal(s, t):
    # Find all positions of characters in t within s
    positions = []
    j = 0
    for i in range(len(s)):
        if j < len(t) and s[i] == t[j]:
            positions.append(i)
            j += 1
    
    # If t is a prefix or suffix of s, we can remove everything except t
    if positions[0] == 0 or positions[-1] == len(s) - 1:
        return len(s) - len(t)
    
    # Calculate the maximum gap that can be removed
    max_gap = 0
    for i in range(1, len(positions)):
        max_gap = max(max_gap, positions[i] - positions[i - 1] - 1)
    
    # Also consider the gaps at the ends
    max_gap = max(max_gap, positions[0])
    max_gap = max(max_gap, len(s) - 1 - positions[-1])
    
    return max_gap

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_substring_removal(s, t))