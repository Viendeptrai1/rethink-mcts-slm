import sys

def construct_binary_string(a, b, x):
    n = a + b
    if x == 0:
        return '0' * a + '1' * b
    elif x == n - 1:
        return '01' * (a - 1) + '0' + '10' * (b - 1) + '1'
    
    # Start with a sequence of 0s followed by 1s
    s = ['0'] * a + ['1'] * b
    
    # We need x transitions, so we will place x-1 '1's in the first part
    # and the rest in the second part
    transitions = x - 1
    for i in range(transitions):
        s[i] = '1'
    
    # Now we need to ensure the last part has the correct number of transitions
    # We do this by swapping adjacent elements
    for i in range(transitions, n - 1):
        if s[i] == s[i + 1]:
            s[i], s[i + 1] = s[i + 1], s[i]
    
    return ''.join(s)

# Read input
input = sys.stdin.read().strip().split()
a = int(input[0])
b = int(input[1])
x = int(input[2])

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)