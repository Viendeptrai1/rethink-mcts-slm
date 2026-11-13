MOD = 10**9 + 7

def sum_of_weights(n, k, weights):
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    prefix_sum = [0] * (n + 1)
    
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + weights[i - 1]
    
    for i in range(1, n + 1):
        dp[i][1] = prefix_sum[i] * i
    
    for j in range(2, k + 1):
        for i in range(j, n + 1):
            dp[i][j] = (dp[i - 1][j] + dp[i - 1][j - 1] * (prefix_sum[i] - prefix_sum[i - j])) % MOD
    
    return dp[n][k]

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
weights = list(map(int, data[2:]))

# Output result
print(sum_of_weights(n, k, weights))