import sys

def construct_binary_string(a, b, x):
    n = a + b
    s = ['0'] * a + ['1'] * b
    
    # Sort the list to make it easier to manipulate transitions
    s.sort()
    
    # Calculate the current number of transitions
    current_transitions = sum(1 for i in range(n - 1) if s[i] != s[i + 1])
    
    # If the current number of transitions is less than x, we need to increase it
    if current_transitions < x:
        # Move '1's to the right to increase transitions
        for i in range(x - current_transitions):
            # Find the first '0' followed by a '1'
            for j in range(n - 1):
                if s[j] == '0' and s[j + 1] == '1':
                    # Swap them
                    s[j], s[j + 1] = s[j + 1], s[j]
                    break
    else:
        # If the current number of transitions is more than x, we need to decrease it
        for i in range(current_transitions - x):
            # Find the first '1' followed by a '0'
            for j in range(n - 1):
                if s[j] == '1' and s[j + 1] == '0':
                    # Swap them
                    s[j], s[j + 1] = s[j + 1], s[j]
                    break
    
    return ''.join(s)

# Read input
input_data = sys.stdin.read().split()
a = int(input_data[0])
b = int(input_data[1])
x = int(input_data[2])

# Construct and print the binary string
result = construct_binary_string(a, b, x)
print(result)