import sys

def max_discharge(M, S, steps):
    power = 1
    result = []
    threshold = 1 << S
    
    for step in steps:
        if step == '+':
            power += 1
        elif step == 'x':
            power *= 2
        
        # Reduce power modulo threshold to prevent overflow
        power %= threshold
        
        # Determine if we should keep the step or turn it into a no-op
        if step == 'x' and power < threshold // 2:
            result.append('o')
        else:
            result.append(step)
    
    return ''.join(result)

# Read input
input = sys.stdin.read
data = input().split()
M = int(data[0])
S = int(data[1])
steps = data[2]

# Output the result
print(max_discharge(M, S, steps))