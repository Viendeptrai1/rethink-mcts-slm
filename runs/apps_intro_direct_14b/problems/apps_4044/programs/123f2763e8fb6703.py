import sys

def construct_binary_string(a, b, x):
    n = a + b
    if x == 0:
        return '0' * a + '1' * b
    elif x == n - 1:
        return '01' * (a - 1) + '0' + '10' * (b - 1) + '1'
    
    # Start with a sequence of 0s followed by 1s
    s = ['0'] * a + ['1'] * b
    
    # We need to create x transitions
    # If x is less than a, we can place transitions within the 0s
    if x < a:
        for i in range(x):
            s[i] = '1'
    else:
        # If x is greater than or equal to a, we place transitions within the 1s
        for i in range(x - a):
            s[a + i] = '0'
    
    return ''.join(s)

# Read input
input_data = sys.stdin.read().strip().split()
a = int(input_data[0])
b = int(input_data[1])
x = int(input_data[2])

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)