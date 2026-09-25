import sys

def construct_binary_string(a, b, x):
    n = a + b
    if a <= b:
        # Start with '0'
        result = ['0'] * a + ['1'] * b
    else:
        # Start with '1'
        result = ['1'] * b + ['0'] * a
    
    # Calculate the number of transitions needed
    transitions = min(a, b) - 1
    
    # If transitions are less than required, add more transitions
    if transitions < x:
        diff = x - transitions
        for i in range(diff):
            if i % 2 == 0:
                result[i] = '1' if result[i] == '0' else '0'
            else:
                result[n - i - 1] = '1' if result[n - i - 1] == '0' else '0'
    
    return ''.join(result)

# Read input
input_data = sys.stdin.read().strip().split()
a = int(input_data[0])
b = int(input_data[1])
x = int(input_data[2])

# Construct and print the binary string
output = construct_binary_string(a, b, x)
print(output)