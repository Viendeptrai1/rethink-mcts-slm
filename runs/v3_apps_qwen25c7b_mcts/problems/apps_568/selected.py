MOD = 10**9 + 7

def count_valid_distributions(n):
    total_ways = pow(3, 3 * n, MOD)
    invalid_ways = 0
    
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                if (a + a + n + b + 2*n != 6) and (b + b + n + c + 2*n != 6) and (c + c + n + a + 2*n != 6):
                    continue
                invalid_ways += 1
    
    valid_ways = (total_ways - invalid_ways * pow(3, 3 * n - 3, MOD)) % MOD
    return valid_ways

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])

# Output result
print(count_valid_distributions(n))