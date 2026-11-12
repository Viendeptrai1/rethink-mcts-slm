import re

def max_accordion_length(s):
    # Regular expression to match the accordion pattern
    pattern = r'\[\:([|]*):\]'
    
    # Find all matches of the pattern in the string
    matches = re.findall(pattern, s)
    
    # If there are no matches, return -1
    if not matches:
        return -1
    
    # Calculate the maximum length of the matches
    max_length = max(len(match) + 4 for match in matches)
    
    return max_length

# Read input from stdin
import sys
input = sys.stdin.read().strip()

# Print the result
print(max_accordion_length(input))