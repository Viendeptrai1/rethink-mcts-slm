import sys

def construct_binary_string(a, b, x):
    n = a + b
    if x == 0:
        return '0' * a + '1' * b
    elif x == n - 1:
        return '01' * (a - 1) + '0' + '10' * (b - 1) + '1'
    
    # Start with a sequence of '0's followed by '1's
    s = ['0'] * a + ['1'] * b
    
    # We need to create x transitions
    # If x is even, we can alternate between 0s and 1s
    # If x is odd, we need to adjust the last character
    if x % 2 == 0:
        for i in range(x // 2):
            s[2 * i] = '1'
            s[2 * i + 1] = '0'
    else:
        for i in range(x // 2):
            s[2 * i] = '1'
            s[2 * i + 1] = '0'
        s[x] = '1' if s[x] == '0' else '0'
    
    return ''.join(s)

# Read input
input_line = sys.stdin.read().strip()
a, b, x = map(int, input_line.split())

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)