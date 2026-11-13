def max_power_discharge(M, S, steps):
    # Initialize variables
    current_power = 1
    result = list(steps)
    
    # Iterate through each step
    for i in range(M):
        if steps[i] == '+':
            current_power += 1
        elif steps[i] == 'x':
            current_power *= 2
        
        # Check if we need to replace the current step with 'o'
        if current_power >= 2**S:
            result[i] = 'o'
            current_power //= 2
    
    return ''.join(result)

# Read input
import sys
input = sys.stdin.read
data = input().split()
M = int(data[0])
S = int(data[1])
steps = data[2]

# Get the result
result = max_power_discharge(M, S, steps)

# Print the result
print(result)