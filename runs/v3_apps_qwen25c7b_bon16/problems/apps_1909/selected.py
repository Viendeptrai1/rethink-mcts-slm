def find_best_task(n, k, powers):
    min_power = float('inf')
    best_task = -1
    
    for start in range(k):
        current_power = sum(powers[i] for i in range(start, n, k))
        if current_power < min_power:
            min_power = current_power
            best_task = start + 1
    
    return best_task

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
powers = list(map(int, data[2:]))

# Find and print the best task
result = find_best_task(n, k, powers)
print(result)