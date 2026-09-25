import sys

def construct_binary_string(a, b, x):
    n = a + b
    s = []
    
    # Start with a 0 if a >= b, otherwise start with a 1
    current_char = '0' if a >= b else '1'
    s.append(current_char)
    
    # Place transitions to achieve exactly x transitions
    for _ in range(x):
        if current_char == '0':
            if b > 0:
                s.append('1')
                b -= 1
                current_char = '1'
            elif a > 0:
                s.append('0')
                a -= 1
        else:
            if a > 0:
                s.append('0')
                a -= 1
                current_char = '0'
            elif b > 0:
                s.append('1')
                b -= 1
    
    # Append remaining characters
    s.extend(['0'] * a)
    s.extend(['1'] * b)
    
    return ''.join(s)

# Read input
input_line = sys.stdin.read().strip()
a, b, x = map(int, input_line.split())

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)