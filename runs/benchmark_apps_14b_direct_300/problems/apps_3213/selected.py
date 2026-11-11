import sys

def solve(M, S, steps):
    # Calculate the maximum power that can be achieved without considering the modulo operation
    max_power = 1
    for step in steps:
        if step == '+':
            max_power += 1
        elif step == 'x':
            max_power *= 2
    
    # Calculate the effective maximum power considering the modulo operation
    effective_max_power = max_power % (2 ** S)
    
    # Initialize the result list
    result = []
    
    # Iterate over the steps to determine which ones to keep
    current_power = 1
    for step in steps:
        if step == '+':
            new_power = current_power + 1
        elif step == 'x':
            new_power = current_power * 2
        
        # Check if keeping this step increases the effective power
        if new_power % (2 ** S) > current_power % (2 ** S):
            result.append(step)
            current_power = new_power
        else:
            result.append('o')
    
    return ''.join(result)

# Read input
input = sys.stdin.read
data = input().split()
M = int(data[0])
S = int(data[1])
steps = data[2]

# Solve the problem
output = solve(M, S, steps)

# Print the result
print(output)