import sys

def max_discharge_power(M, S, steps):
    # Initialize variables
    power = 1
    max_discharge = 0
    best_steps = list(steps)
    
    # Calculate the maximum possible discharge
    max_possible_discharge = (1 << S) - 1
    
    # Iterate over each step in reverse to decide which steps to convert to 'o'
    for i in range(M - 1, -1, -1):
        if steps[i] == '+':
            # If the current step is '+', check if it's beneficial to keep it
            if (power * 2 - 1) % (1 << S) > max_discharge:
                max_discharge = (power * 2 - 1) % (1 << S)
                best_steps[i] = '+'
                power = power * 2 - 1
            else:
                best_steps[i] = 'o'
        elif steps[i] == 'x':
            # If the current step is 'x', check if it's beneficial to keep it
            if (power * 2) % (1 << S) > max_discharge:
                max_discharge = (power * 2) % (1 << S)
                best_steps[i] = 'x'
                power *= 2
            else:
                best_steps[i] = 'o'
    
    return ''.join(best_steps)

# Read input
input = sys.stdin.read
data = input().split()
M = int(data[0])
S = int(data[1])
steps = data[2]

# Get the result
result = max_discharge_power(M, S, steps)

# Print the result
print(result)