import sys
from math import comb

MOD = 10**9 + 7

def count_ways(n, k):
    if n == 1:
        return k % MOD
    
    # Calculate the number of ways to place the minimum values in the first row and column
    min_values = comb(k - 1, n - 1)
    
    # Calculate the number of ways to fill the remaining cells
    remaining_cells = (k - 1) ** (n * n - n - n + 1)
    
    # Total number of ways
    total_ways = (min_values * remaining_cells) % MOD
    
    return total_ways

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Output result
print(count_ways(n, k))