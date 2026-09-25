import sys

def construct_binary_string(a, b, x):
    # Start with all 1s followed by all 0s
    s = ['1'] * b + ['0'] * a
    
    # Calculate the current number of transitions
    current_transitions = b  # Initially, there are b transitions between 1s and 0s
    
    # If the current number of transitions is less than x, we need to add more transitions
    if current_transitions < x:
        # Add more transitions by inserting 0s between 1s
        for i in range(x - current_transitions):
            s.insert(b + i, '0')
    
    # If the current number of transitions is more than x, we need to reduce transitions
    elif current_transitions > x:
        # Reduce transitions by merging groups of 0s and 1s from opposite ends
        while current_transitions > x:
            s.pop()  # Remove the last element
            current_transitions -= 1
    
    return ''.join(s)

# Read input
input_data = sys.stdin.read().strip().split()
a = int(input_data[0])
b = int(input_data[1])
x = int(input_data[2])

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)