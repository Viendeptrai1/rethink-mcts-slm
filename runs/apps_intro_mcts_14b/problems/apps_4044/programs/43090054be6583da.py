import sys

def construct_binary_string(a, b, x):
    n = a + b
    s = []
    
    # Start with the more frequent character
    if a >= b:
        s.append('0')
        a -= 1
    else:
        s.append('1')
        b -= 1
    
    # Place transitions to achieve exactly x changes
    for _ in range(x - 1):
        if a > 0 and b > 0:
            if len(s) % 2 == 0:
                s.append('0')
                a -= 1
            else:
                s.append('1')
                b -= 1
        elif a > 0:
            s.append('0')
            a -= 1
        else:
            s.append('1')
            b -= 1
    
    # Fill the rest of the string with the remaining characters
    if a > 0:
        s.extend(['0'] * a)
    else:
        s.extend(['1'] * b)
    
    return ''.join(s)

# Read input
input = sys.stdin.read().strip().split()
a = int(input[0])
b = int(input[1])
x = int(input[2])

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)