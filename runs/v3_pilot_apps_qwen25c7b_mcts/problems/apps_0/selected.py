import re

def max_accordion_length(s):
    # Regular expression to match the accordion pattern
    pattern = r'\[\:.*\:\]'
    
    # Find all substrings that match the accordion pattern
    matches = re.findall(pattern, s)
    
    # If there are no matches, return -1
    if not matches:
        return -1
    
    # Return the length of the longest match
    return max(len(match) for match in matches)

# Read input from stdin
import sys
input = sys.stdin.read().strip()

# Print the result
print(max_accordion_length(input))