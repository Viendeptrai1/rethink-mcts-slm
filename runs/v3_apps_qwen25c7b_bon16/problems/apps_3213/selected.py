def max_power_discharge(M, S, steps):
    result = list(steps)
    current_power = 1
    
    for i in range(M):
        if steps[i] == '+':
            current_power += 1
            if current_power >= 2**S:
                result[i] = 'o'
                current_power = (current_power % (2**S)) // 2
        elif steps[i] == 'x':
            current_power *= 2
            if current_power >= 2**S:
                result[i] = 'o'
                current_power = (current_power % (2**S)) // 2
                
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