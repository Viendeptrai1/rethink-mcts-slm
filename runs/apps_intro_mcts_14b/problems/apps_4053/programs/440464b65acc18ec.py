import sys

def guess_prefix_suffix(n, strings):
    # Create a dictionary to store the count of each string
    string_count = {}
    for s in strings:
        if s in string_count:
            string_count[s] += 1
        else:
            string_count[s] = 1
    
    # Create a list to store the result
    result = [''] * (2 * n - 2)
    
    # Iterate over the strings and assign 'P' or 'S'
    for i, s in enumerate(strings):
        if string_count[s] == 1:
            # If the string appears only once, it must be a prefix or suffix
            # Check if it can be a prefix
            if s + strings[i + 1] in string_count:
                result[i] = 'P'
                result[i + 1] = 'S'
            else:
                result[i] = 'S'
                result[i + 1] = 'P'
            string_count[s] -= 1
            string_count[strings[i + 1]] -= 1
        else:
            # If the string appears twice, we need to check compatibility
            # Check if it can be a prefix
            if s + strings[i + 1] in string_count:
                result[i] = 'P'
                result[i + 1] = 'S'
            else:
                result[i] = 'S'
                result[i + 1] = 'P'
            string_count[s] -= 1
            string_count[strings[i + 1]] -= 1
    
    return ''.join(result)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
strings = data[1:]

# Guess the prefix and suffix
result = guess_prefix_suffix(n, strings)

# Print the result
print(result)