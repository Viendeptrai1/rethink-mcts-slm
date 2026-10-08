import sys

def max_discharge_power(M, S, steps):
    MOD = 1 << S
    max_power = 0
    current_power = 1
    best_steps = list(steps)
    
    # Calculate the maximum power we can achieve without any no-ops
    for step in steps:
        if step == '+':
            current_power = (current_power + 1) % MOD
        elif step == 'x':
            current_power = (current_power * 2) % MOD
        max_power = max(max_power, current_power)
    
    # Now, we need to find the optimal steps to transform into no-ops
    current_power = 1
    for i in range(M):
        if steps[i] == '+':
            next_power = (current_power + 1) % MOD
        elif steps[i] == 'x':
            next_power = (current_power * 2) % MOD
        
        if next_power <= current_power:
            best_steps[i] = 'o'
        else:
            current_power = next_power
    
    return ''.join(best_steps)

# Read input
input = sys.stdin.read
data = input().split()
M = int(data[0])
S = int(data[1])
steps = data[2]

# Output the result
print(max_discharge_power(M, S, steps))