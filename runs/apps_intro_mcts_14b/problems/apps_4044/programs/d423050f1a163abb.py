import sys

def construct_binary_string(a, b, x):
    n = a + b
    result = []
    
    # Start with alternating 0s and 1s
    while a > 0 and b > 0:
        if len(result) % 2 == 0:
            result.append('0')
            a -= 1
        else:
            result.append('1')
            b -= 1
    
    # Append remaining 0s or 1s
    if a > 0:
        result.extend(['0'] * a)
    else:
        result.extend(['1'] * b)
    
    # Adjust the string to have exactly x transitions
    transitions = sum(1 for i in range(n - 1) if result[i] != result[i + 1])
    if transitions < x:
        # Add more transitions
        for i in range(n - 1):
            if transitions == x:
                break
            if result[i] == result[i + 1]:
                result[i + 1] = '1' if result[i] == '0' else '0'
                transitions += 1
    elif transitions > x:
        # Remove some transitions
        for i in range(n - 1):
            if transitions == x:
                break
            if result[i] != result[i + 1]:
                result[i + 1] = result[i]
                transitions -= 1
    
    return ''.join(result)

# Read input
input_data = sys.stdin.read().strip().split()
a = int(input_data[0])
b = int(input_data[1])
x = int(input_data[2])

# Construct and print the binary string
print(construct_binary_string(a, b, x))