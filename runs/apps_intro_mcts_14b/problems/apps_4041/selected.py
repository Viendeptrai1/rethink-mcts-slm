import sys

def max_substring_removal(s, t):
    # Find the positions of characters of t in s while maintaining order
    positions = []
    t_index = 0
    for i, char in enumerate(s):
        if t_index < len(t) and char == t[t_index]:
            positions.append(i)
            t_index += 1
    
    # If t is not found in s, return the length of s
    if not positions:
        return len(s)
    
    # Calculate the maximum length of substring that can be removed
    max_length = 0
    
    # Check the length of substring that can be removed before the first character of t
    max_length = max(max_length, positions[0])
    
    # Check the length of substring that can be removed after the last character of t
    max_length = max(max_length, len(s) - 1 - positions[-1])
    
    # Check the length of substring that can be removed between consecutive characters of t
    for i in range(1, len(positions)):
        max_length = max(max_length, positions[i] - positions[i-1] - 1)
    
    return max_length

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_substring_removal(s, t))