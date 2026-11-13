def max_average_power(n, k, m, powers):
    # Sort the powers to facilitate removal of minimum and increase of maximum
    powers.sort()
    
    # Initialize variables
    total_operations = m
    total_superheroes = n
    
    # Decrease operations used for removing the lowest power superheroes
    while total_operations > 0 and len(powers) > 1:
        if powers[1] - powers[0] <= total_operations:
            powers.pop(0)
            total_operations -= (powers[1] - powers[0])
            total_superheroes -= 1
        else:
            break
    
    # Increase operations used for increasing the highest power superheroes
    while total_operations > 0 and total_superheroes < n + k:
        if powers[-1] - powers[-2] >= 1:
            powers[-1] += min(total_operations, 1)
            total_operations -= 1
        else:
            break
    
    # Calculate the maximum average power
    max_average = sum(powers) / len(powers)
    return max_average

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
m = int(data[2])
powers = list(map(int, data[3:]))

# Output the result
print(max_average_power(n, k, m, powers))