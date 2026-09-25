import sys

def max_substring_to_remove(s, t):
    # Find all positions of characters in t within s
    positions = []
    j = 0
    for i in range(len(s)):
        if j < len(t) and s[i] == t[j]:
            positions.append(i)
            j += 1
    
    # If t is a prefix or suffix of s, we can remove the rest
    if positions[0] == 0 or positions[-1] == len(s) - 1:
        return len(s) - len(t)
    
    # Calculate the maximum length of substring to remove
    max_length = 0
    for i in range(1, len(positions)):
        max_length = max(max_length, positions[i] - positions[i-1] - 1)
    
    # Also consider the segments before the first character and after the last character
    max_length = max(max_length, positions[0])
    max_length = max(max_length, len(s) - positions[-1] - 1)
    
    return max_length

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_substring_to_remove(s, t))