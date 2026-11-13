def min_telling_off_power(n, k, powers):
    min_power = float('inf')
    best_start = 0
    
    for start in range(k):
        current_power = sum(powers[start::k])
        if current_power < min_power:
            min_power = current_power
            best_start = start
            
    return best_start + 1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
powers = list(map(int, data[2:]))

print(min_telling_off_power(n, k, powers))