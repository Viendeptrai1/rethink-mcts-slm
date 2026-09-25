import sys

def max_substring_to_remove(s, t):
    # Find all positions of characters in t within s
    positions = []
    j = 0
    for i in range(len(s)):
        if j < len(t) and s[i] == t[j]:
            positions.append(i)
            j += 1
    
    # If t is a subsequence of s, we can remove everything except the positions found
    # Calculate the maximum length of the substring that can be removed
    max_length = 0
    if positions:
        # Consider the segment before the first occurrence of t
        max_length = max(max_length, positions[0])
        # Consider the segment after the last occurrence of t
        max_length = max(max_length, len(s) - 1 - positions[-1])
        # Consider the segments between consecutive occurrences of t
        for i in range(1, len(positions)):
            max_length = max(max_length, positions[i] - positions[i-1] - 1)
    
    return max_length

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_substring_to_remove(s, t))