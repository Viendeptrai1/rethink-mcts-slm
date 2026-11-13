def maximize_discharged_power(M, S, steps):
    # Calculate the maximum power that can be discharged
    max_discharge = (1 << S) - 1
    
    # Initialize current power and the list of steps to output
    current_power = 1
    output_steps = list(steps)
    
    # Traverse the steps to determine the optimal transformation
    for i in range(M):
        if steps[i] == '+':
            current_power += 1
        elif steps[i] == 'x':
            current_power *= 2
        
        # If current power exceeds max discharge, consider changing this step
        if current_power > max_discharge:
            # Calculate the excess power
            excess_power = current_power - max_discharge
            
            # If the excess power is a power of 2, we can change this step to a no-op
            if (excess_power & (excess_power - 1)) == 0:
                output_steps[i] = 'o'
                current_power -= excess_power
    
    # Return the transformed steps as a string
    return ''.join(output_steps)

# Read input
import sys
input = sys.stdin.read
data = input().split()
M = int(data[0])
S = int(data[1])
steps = data[2]

# Get the result and print it
result = maximize_discharged_power(M, S, steps)
print(result)