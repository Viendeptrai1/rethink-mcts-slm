MOD = 10**9 + 7

def count_random_pictures(n, m):
    if m == 1:
        return 2 ** n % MOD
    
    # Initialize the number of ways to color the first row
    prev_ways = [1, 1]
    
    for _ in range(1, n):
        current_ways = [0, 0]
        # Calculate the number of ways to color the current row given the previous row
        current_ways[0] = (prev_ways[0] + prev_ways[1]) % MOD
        current_ways[1] = (prev_ways[0] + prev_ways[1]) % MOD
        prev_ways = current_ways
    
    # Each row can be colored in 2^(m-1) ways independently
    total_ways = pow(2, m - 1, MOD)
    result = (total_ways * sum(prev_ways)) % MOD
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])

# Print the result
print(count_random_pictures(n, m))