def max_average_power(n, k, m, powers):
    powers.sort()
    total_operations = m
    increases_used = [0] * n
    
    # Use binary search to find the optimal threshold
    left, right = 0, max(powers)
    while left < right:
        mid = (left + right + 1) // 2
        current_operations = 0
        
        for i in range(n):
            if powers[i] < mid:
                needed_increases = mid - powers[i]
                if increases_used[i] + needed_increases <= k:
                    current_operations += needed_increases
                    increases_used[i] += needed_increases
                else:
                    current_operations += k
                    increases_used[i] = k
        
        if current_operations > total_operations:
            right = mid - 1
        else:
            left = mid
    
    return left / n

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
m = int(data[2])
powers = list(map(int, data[3:]))

result = max_average_power(n, k, m, powers)
print(f"{result:.15f}")