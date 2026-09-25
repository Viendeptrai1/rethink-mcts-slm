import sys

def construct_binary_string(a, b, x):
    n = a + b
    s = []
    
    # Start with the character that has more occurrences
    if a >= b:
        current_char = '0'
        remaining_a = a
        remaining_b = b
    else:
        current_char = '1'
        remaining_a = a
        remaining_b = b
    
    # Place transitions to achieve exactly x changes
    for i in range(x):
        s.append(current_char)
        if current_char == '0':
            current_char = '1'
            remaining_b -= 1
        else:
            current_char = '0'
            remaining_a -= 1
    
    # Fill the rest of the string with the remaining characters
    if remaining_a > 0:
        s.extend(['0'] * remaining_a)
    if remaining_b > 0:
        s.extend(['1'] * remaining_b)
    
    return ''.join(s)

# Read input
input = sys.stdin.read().strip().split()
a = int(input[0])
b = int(input[1])
x = int(input[2])

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)