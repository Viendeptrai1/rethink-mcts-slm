def max_accordion_length(s: str) -> int:
    open_bracket = '['
    close_bracket = ']'
    colon = ':'
    vertical_line = '|'
    
    # Initialize counters for each component of the accordion
    open_bracket_count = 0
    colon_count = 0
    vertical_line_count = 0
    close_bracket_count = 0
    
    # First pass: count the necessary components
    for char in s:
        if char == open_bracket:
            open_bracket_count += 1
        elif char == colon:
            colon_count += 1
        elif char == vertical_line:
            vertical_line_count += 1
        elif char == close_bracket:
            close_bracket_count += 1
    
    # Check if we have at least one of each component
    if open_bracket_count == 0 or colon_count == 0 or close_bracket_count == 0:
        return -1
    
    # Calculate the maximum possible length of the accordion
    # We need at least one colon and one vertical line for the middle part
    if colon_count < 2:
        return -1
    
    # The minimum length of an accordion is 4: [::]
    # We can add vertical lines in the middle part
    max_length = 4 + min(vertical_line_count, colon_count - 2)
    
    return max_length

# Read input
import sys
input = sys.stdin.read().strip()

# Get the result and print it
result = max_accordion_length(input)
print(result)