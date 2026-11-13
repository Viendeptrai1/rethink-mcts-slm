def maximize_dischargeable_power(M, S, steps):
    power = 1
    max_dischargeable_power = 0
    best_steps = list(steps)
    
    # Calculate the maximum possible power after each step
    max_power_after_step = [0] * M
    for i in range(M):
        if steps[i] == '+':
            power += 1
        else:  # steps[i] == 'x'
            power *= 2
        max_power_after_step[i] = power
    
    # Calculate the maximum dischargeable power
    for i in range(M):
        max_dischargeable_power = max(max_dischargeable_power, max_power_after_step[i] % (2 ** S))
    
    # Determine which steps to replace with 'o'
    for i in range(M):
        if steps[i] == 'x':
            # Temporarily replace 'x' with 'o'
            best_steps[i] = 'o'
            power = 1
            for j in range(M):
                if best_steps[j] == '+':
                    power += 1
                elif best_steps[j] == 'x':
                    power *= 2
            # Check if this replacement increases the max dischargeable power
            if power % (2 ** S) > max_dischargeable_power:
                max_dischargeable_power = power % (2 ** S)
            else:
                # Revert the change if it doesn't improve
                best_steps[i] = 'x'
    
    return ''.join(best_steps)

# Read input
M, S = map(int, input().split())
steps = input().strip()

# Get the result
result = maximize_dischargeable_power(M, S, steps)

# Print the result
print(result)