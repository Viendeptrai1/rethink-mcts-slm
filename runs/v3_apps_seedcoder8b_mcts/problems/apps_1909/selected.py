def min_power_to_tell_off(n, k, a):
    # Calculate the total power for each starting position
    total_power = [0] * n
    for i in range(n):
        total_power[i] = sum(a[(i + j) % n] for j in range(0, n, k))
    
    # Find the minimum power and the corresponding starting task
    min_power = min(total_power)
    min_start_task = total_power.index(min_power) + 1
    
    return min_start_task

# Read input
n, k = map(int, input().split())
a = list(map(int, input().split()))

# Get the result and print it
result = min_power_to_tell_off(n, k, a)
print(result)