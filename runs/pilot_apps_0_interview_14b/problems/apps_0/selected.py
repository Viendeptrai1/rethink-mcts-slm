import sys

def max_accordion_length(s):
    n = len(s)
    max_length = -1
    
    # Find all possible starting positions of the accordion
    start_positions = []
    for i in range(n):
        if s[i] == '[':
            start_positions.append(i)
    
    # Find all possible ending positions of the accordion
    end_positions = []
    for i in range(n):
        if s[i] == ']':
            end_positions.append(i)
    
    # Check each possible pair of start and end positions
    for start in start_positions:
        for end in end_positions:
            if start < end:
                # Extract the substring between the start and end positions
                substring = s[start:end+1]
                
                # Check if the substring is a valid accordion
                if substring.startswith('[') and substring.endswith(']'):
                    # Count the number of '|' characters between the colons
                    colon_count = substring.count(':')
                    if colon_count == 2:
                        pipe_count = substring.count('|')
                        # Calculate the length of the accordion
                        accordion_length = len(substring)
                        # Update the maximum length if this accordion is longer
                        max_length = max(max_length, accordion_length)
    
    return max_length

# Read input from standard input
input_string = sys.stdin.read().strip()

# Print the result
print(max_accordion_length(input_string))