import sys

def max_removable_substring(s, t):
    # Find all positions of characters in s that match any character in t
    matched_positions = []
    t_index = 0
    for i in range(len(s)):
        if t_index < len(t) and s[i] == t[t_index]:
            matched_positions.append(i)
            t_index += 1
    
    # Calculate the maximum gap between consecutive matched positions
    max_gap = 0
    if matched_positions:
        # Gap before the first match
        max_gap = max(max_gap, matched_positions[0])
        # Gap after the last match
        max_gap = max(max_gap, len(s) - 1 - matched_positions[-1])
        # Gaps between consecutive matches
        for i in range(1, len(matched_positions)):
            max_gap = max(max_gap, matched_positions[i] - matched_positions[i-1] - 1)
    
    return max_gap

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_removable_substring(s, t))