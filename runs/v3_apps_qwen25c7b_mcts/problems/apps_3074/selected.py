MOD = 10**9 + 7

def count_valid_subsets(N, S):
    dp = [0] * 3
    dp[0] = 1
    
    for char in S:
        next_dp = [0] * 3
        for i in range(3):
            next_dp[(i + int(char)) % 3] += dp[i]
            next_dp[(i + int(char)) % 3] %= MOD
        dp = next_dp
    
    return sum(dp) % MOD

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
S = data[1]

# Compute and print result
result = count_valid_subsets(N, S)
print(result)