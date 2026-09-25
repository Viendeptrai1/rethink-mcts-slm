import sys

def max_substring_to_remove(s, t):
    # Find all positions of each character in t within s
    positions = {char: [] for char in t}
    for i, char in enumerate(s):
        if char in positions:
            positions[char].append(i)
    
    # Initialize variables to track the maximum length of removable substring
    max_length = 0
    current_end = -1
    
    # Iterate over each character in t
    for char in t:
        if not positions[char]:
            break
        # Find the smallest index in s that is greater than current_end
        next_index = next((index for index in positions[char] if index > current_end), None)
        if next_index is None:
            break
        # Update current_end to the found index
        current_end = next_index
    
    # Calculate the length of the removable substring
    max_length = len(s) - (current_end + 1)
    
    return max_length

# Read input
input = sys.stdin.read().splitlines()
s = input[0]
t = input[1]

# Output the result
print(max_substring_to_remove(s, t))