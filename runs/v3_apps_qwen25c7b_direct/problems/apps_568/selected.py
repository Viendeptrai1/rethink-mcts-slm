MOD = 10**9 + 7

def count_ways(n):
    # Calculate the total number of ways to distribute coins without any restrictions
    total_ways = pow(3, 3 * n, MOD)
    
    # Calculate the number of invalid distributions where the condition is violated
    invalid_ways = 0
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                if a + a + n + b + 2*n != 6 or a + b + b + n + 2*n != 6 or a + b + c + n + 2*n != 6:
                    invalid_ways += 1
    
    # Since each triplet is counted 3 times, we need to divide by 3
    invalid_ways //= 3
    
    # Subtract the invalid ways from the total ways and take modulo MOD
    valid_ways = (total_ways - invalid_ways) % MOD
    
    return valid_ways

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])

# Output the result
print(count_ways(n))