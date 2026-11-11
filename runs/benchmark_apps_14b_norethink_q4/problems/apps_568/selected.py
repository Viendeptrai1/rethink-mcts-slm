MOD = 10**9 + 7

def count_ways(n):
    total_ways = pow(3, 3 * n, MOD)
    
    # Count the number of ways where Tanya is not satisfied
    not_satisfied_ways = 0
    
    # Iterate over all possible values of a_i, a_(i+n), a_(i+2n)
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                if a + b + c == 6:
                    not_satisfied_ways += pow(3, 3 * n - 3, MOD)
                    not_satisfied_ways %= MOD
    
    # Subtract the number of not satisfied ways from total ways
    satisfied_ways = (total_ways - not_satisfied_ways) % MOD
    
    return satisfied_ways

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])

# Print the result
print(count_ways(n))