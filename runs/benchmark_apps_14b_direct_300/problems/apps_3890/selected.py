MOD = 1000000007

def count_ways(n, k):
    if k == 1:
        return pow(n - 1, n - 1, MOD)
    
    def stirling_second_kind(n, k):
        dp = [[0] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        for i in range(1, n + 1):
            for j in range(1, k + 1):
                dp[i][j] = (dp[i - 1][j - 1] + j * dp[i - 1][j]) % MOD
        return dp[n][k]
    
    result = 0
    for i in range(1, k + 1):
        result = (result + stirling_second_kind(k, i) * pow(n - k, n - k, MOD) * pow(i, n - k, MOD)) % MOD
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Output the result
print(count_ways(n, k))