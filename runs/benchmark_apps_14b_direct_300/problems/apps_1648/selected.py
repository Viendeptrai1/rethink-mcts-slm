MOD = 10**9 + 7

def count_ways(N, K):
    # Initialize a list to store the number of ways for each i
    ways = [0] * (K + 1)
    
    # Generate all combinations of positions for K blue balls in N positions
    from itertools import combinations
    
    for comb in combinations(range(N), K):
        # Count the number of segments of consecutive blue balls
        segments = 1
        for j in range(1, K):
            if comb[j] != comb[j - 1] + 1:
                segments += 1
        
        # Increment the count for the number of segments
        ways[segments] += 1
    
    # Return the results modulo 10^9 + 7
    return [w % MOD for w in ways[1:]]

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
K = int(data[1])

# Compute and print the result
result = count_ways(N, K)
for r in result:
    print(r)