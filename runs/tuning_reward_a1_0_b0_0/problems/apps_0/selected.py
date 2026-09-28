import sys

def max_accordion_length(s):
    n = len(s)
    max_length = -1
    
    # State variables to track the current position in the accordion pattern
    start_found = False
    first_colon_found = False
    second_colon_found = False
    end_found = False
    
    # Variables to track the current length of the accordion being formed
    current_length = 0
    
    for char in s:
        if not start_found:
            if char == '[':
                start_found = True
                current_length += 1
        elif not first_colon_found:
            if char == ':':
                first_colon_found = True
                current_length += 1
        elif not second_colon_found:
            if char == '|':
                current_length += 1
            elif char == ':':
                second_colon_found = True
                current_length += 1
        elif not end_found:
            if char == ']':
                end_found = True
                current_length += 1
                # Update the maximum length found
                max_length = max(max_length, current_length)
                # Reset state variables for the next potential accordion
                start_found = False
                first_colon_found = False
                second_colon_found = False
                end_found = False
                current_length = 0
    
    return max_length

# Read input from standard input
input_string = sys.stdin.read().strip()

# Calculate and print the maximum possible length of the accordion
print(max_accordion_length(input_string))