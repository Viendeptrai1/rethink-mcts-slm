def max_accordion_length(s: str) -> int:
    n = len(s)
    
    # Find the first valid '['
    left_bracket = -1
    for i in range(n):
        if s[i] == '[':
            left_bracket = i
            break
    
    # If no '[' is found, it's impossible to form an accordion
    if left_bracket == -1:
        return -1
    
    # Find the last valid ']'
    right_bracket = -1
    for i in range(n - 1, -1, -1):
        if s[i] == ']':
            right_bracket = i
            break
    
    # If no ']' is found, it's impossible to form an accordion
    if right_bracket == -1:
        return -1
    
    # Find the first valid ':' after the left_bracket
    first_colon = -1
    for i in range(left_bracket + 1, right_bracket):
        if s[i] == ':':
            first_colon = i
            break
    
    # If no ':' is found after the left_bracket, it's impossible to form an accordion
    if first_colon == -1:
        return -1
    
    # Find the last valid ':' before the right_bracket
    last_colon = -1
    for i in range(right_bracket - 1, first_colon, -1):
        if s[i] == ':':
            last_colon = i
            break
    
    # If no ':' is found before the right_bracket, it's impossible to form an accordion
    if last_colon == -1:
        return -1
    
    # Count the maximum number of '|' between the first_colon and last_colon
    max_vertical_bars = 0
    current_vertical_bars = 0
    for i in range(first_colon + 1, last_colon):
        if s[i] == '|':
            current_vertical_bars += 1
        else:
            max_vertical_bars = max(max_vertical_bars, current_vertical_bars)
            current_vertical_bars = 0
    
    # Consider the last segment of vertical bars
    max_vertical_bars = max(max_vertical_bars, current_vertical_bars)
    
    # The length of the accordion is 4 (for '[:|:]') plus the maximum number of '|'
    return 4 + max_vertical_bars

# Read input
import sys
input = sys.stdin.read().strip()

# Get the result
result = max_accordion_length(input)

# Print the result
print(result)