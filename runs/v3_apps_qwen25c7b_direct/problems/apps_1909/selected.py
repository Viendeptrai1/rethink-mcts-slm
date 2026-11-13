def find_best_start_task(n, k, powers):
    min_power = float('inf')
    best_start_task = 0
    
    for start in range(k):
        current_power = sum(powers[start::k])
        if current_power < min_power:
            min_power = current_power
            best_start_task = start + 1
    
    return best_start_task

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
powers = list(map(int, data[2:]))

result = find_best_start_task(n, k, powers)
print(result)