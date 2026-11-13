def maximize_discharged_power(M, S, steps):
    current_power = 1
    max_power = 1
    max_position = 0
    
    # Calculate the maximum power we can reach and the position at which it occurs
    for i in range(M):
        if steps[i] == '+':
            current_power += 1
        else:  # steps[i] == 'x'
            current_power *= 2
        
        if current_power > max_power:
            max_power = current_power
            max_position = i
    
    # Calculate the max power after considering the strength limitation
    effective_max_power = max_power % (2**S)
    
    # Starting from the position of max power, convert steps to no-ops
    # until effective_max_power is reached
    result = list(steps)
    for i in range(M-1, max_position, -1):
        if result[i] == '+' and effective_max_power > 1:
            effective_max_power -= 1
        elif result[i] == 'x':
            if effective_max_power % 2 == 1:
                effective_max_power -= 1
            effective_max_power //= 2
    
    # Convert remaining steps to 'o' starting from max_position
    for i in range(max_position, M):
        result[i] = 'o'
    
    return ''.join(result)

# Read input
M, S = map(int, input().split())
steps = input().strip()

# Call the function and print the result
print(maximize_discharged_power(M, S, steps))