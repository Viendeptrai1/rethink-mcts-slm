import sys

def construct_binary_string(a, b, x):
    # Start with all '1's followed by all '0's
    s = ['1'] * b + ['0'] * a
    
    # Calculate the number of transitions needed
    current_transitions = b  # Initially, all '1's are followed by '0's
    
    # If we have more transitions than needed, move some '0's to the left
    if current_transitions > x:
        moves = current_transitions - x
        for i in range(moves):
            s[i] = '0'
    
    # If we have fewer transitions than needed, move some '1's to the right
    elif current_transitions < x:
        moves = x - current_transitions
        for i in range(moves):
            s[-(i + 1)] = '1'
    
    return ''.join(s)

# Read input
input = sys.stdin.read().strip()
a, b, x = map(int, input.split())

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)