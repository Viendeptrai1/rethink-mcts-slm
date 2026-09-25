import sys

def construct_binary_string(a, b, x):
    n = a + b
    # Start with a string of all zeros
    s = ['0'] * a + ['1'] * b
    
    # Count the current number of transitions
    current_transitions = a if a > 0 else 0
    
    # If the current number of transitions is less than x, we need to add more transitions
    if current_transitions < x:
        # Add transitions by moving '1's to the right
        for i in range(x - current_transitions):
            s[i + a] = '0'
            s[i + a + 1] = '1'
    
    # If the current number of transitions is more than x, we need to remove some transitions
    elif current_transitions > x:
        # Remove transitions by moving '1's to the left
        for i in range(current_transitions - x):
            s[a - i - 1] = '1'
            s[a - i] = '0'
    
    return ''.join(s)

# Read input
input_line = sys.stdin.read().strip()
a, b, x = map(int, input_line.split())

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)