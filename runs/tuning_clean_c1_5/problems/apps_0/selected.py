import sys

def max_accordion_length(s):
    n = len(s)
    max_length = -1
    
    # Find all possible starting positions of the accordion
    start_positions = []
    for i in range(n):
        if s[i] == '[' and i + 2 < n and s[i + 1] == ':':
            start_positions.append(i)
    
    # Find all possible ending positions of the accordion
    end_positions = []
    for i in range(n):
        if s[i] == ']' and i - 2 >= 0 and s[i - 1] == ':':
            end_positions.append(i)
    
    # Check each possible start and end position
    for start in start_positions:
        for end in end_positions:
            if start < end:
                # Check if there are only '|' characters between start and end
                valid = True
                for j in range(start + 2, end):
                    if s[j] != '|':
                        valid = False
                        break
                if valid:
                    max_length = max(max_length, end - start + 1)
    
    return max_length

# Read input
input_string = sys.stdin.read().strip()

# Output the result
print(max_accordion_length(input_string))