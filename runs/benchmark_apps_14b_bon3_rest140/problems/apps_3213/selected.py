import sys

def solve(M, S, steps):
    # Initialize variables
    max_power = 0
    best_steps = ""
    current_power = 1
    mask = (1 << S) - 1
    
    # Iterate over all possible subsets of steps to turn into no-ops
    for i in range(1 << M):
        current_steps = ""
        power = 1
        for j in range(M):
            if (i & (1 << j)) == 0:
                if steps[j] == '+':
                    power += 1
                elif steps[j] == 'x':
                    power *= 2
                current_steps += steps[j]
            else:
                current_steps += 'o'
        
        # Calculate the effective power after applying the mask
        effective_power = power & mask
        
        # Update the best result if this one is better
        if effective_power > max_power:
            max_power = effective_power
            best_steps = current_steps
    
    return best_steps

# Read input
input = sys.stdin.read
data = input().split()
M = int(data[0])
S = int(data[1])
steps = data[2]

# Solve the problem
result = solve(M, S, steps)

# Print the result
print(result)