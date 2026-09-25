import sys

def construct_binary_string(a, b, x):
    n = a + b
    if x == 0:
        return '0' * a + '1' * b
    elif x == n - 1:
        return '01' * (a - 1) + '0' + '10' * (b - 1) + '1'
    
    # Start with a sequence of '0's followed by '1's
    result = ['0'] * a + ['1'] * b
    
    # We need to create x transitions
    transitions = 0
    i = 0
    
    while transitions < x:
        if i + 1 < n and result[i] == result[i + 1]:
            result[i], result[i + 1] = result[i + 1], result[i]
            transitions += 1
        i += 1
    
    return ''.join(result)

# Read input
input_line = sys.stdin.read().strip()
a, b, x = map(int, input_line.split())

# Construct and print the binary string
print(construct_binary_string(a, b, x))