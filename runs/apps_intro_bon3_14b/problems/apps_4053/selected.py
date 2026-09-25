import sys

def guess_prefix_suffix(n, strings):
    # Create a dictionary to count occurrences of each string
    count_dict = {}
    for s in strings:
        if s in count_dict:
            count_dict[s] += 1
        else:
            count_dict[s] = 1
    
    # Initialize the result list
    result = []
    
    # Iterate through the strings and determine if they are prefixes or suffixes
    for s in strings:
        if count_dict[s] == 1:
            # If a string appears only once, it must be a prefix or suffix
            # Check if it can be a prefix
            if any(s + t for t in strings if len(s + t) == n):
                result.append('P')
            else:
                result.append('S')
        else:
            # If a string appears twice, we need to check the context
            # We will assume the first occurrence is a prefix and the second is a suffix
            result.append('P')
            count_dict[s] -= 1
    
    return ''.join(result)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
strings = data[1:]

# Guess the prefix and suffix
output = guess_prefix_suffix(n, strings)

# Print the result
print(output)