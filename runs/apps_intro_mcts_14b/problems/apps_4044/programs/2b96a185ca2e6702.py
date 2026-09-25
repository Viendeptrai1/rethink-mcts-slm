import sys

def construct_binary_string(a, b, x):
    # Create a string with all '1's followed by all '0's
    s = '1' * b + '0' * a
    
    # Insert x transitions by swapping adjacent characters
    for i in range(x):
        if s[i] == '0':
            s = s[:i] + '1' + s[i+1:]
        else:
            s = s[:i] + '0' + s[i+1:]
    
    return s

# Read input
input = sys.stdin.read().strip().split()
a = int(input[0])
b = int(input[1])
x = int(input[2])

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)