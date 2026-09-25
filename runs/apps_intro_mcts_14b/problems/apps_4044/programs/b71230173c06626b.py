import sys

def construct_binary_string(a, b, x):
    n = a + b
    s = []
    
    # Start with '0' if there are more '0's than '1's initially
    if a >= b:
        current_char = '0'
    else:
        current_char = '1'
    
    # Create the string with exactly x transitions
    for _ in range(x):
        s.append(current_char)
        if current_char == '0':
            current_char = '1'
        else:
            current_char = '0'
    
    # Fill the remaining positions
    remaining_zeros = a - (x // 2)
    remaining_ones = b - (x // 2)
    
    if current_char == '0':
        s.extend(['0'] * remaining_zeros)
        s.extend(['1'] * remaining_ones)
    else:
        s.extend(['1'] * remaining_ones)
        s.extend(['0'] * remaining_zeros)
    
    return ''.join(s)

# Read input
input_data = sys.stdin.read().strip().split()
a = int(input_data[0])
b = int(input_data[1])
x = int(input_data[2])

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)