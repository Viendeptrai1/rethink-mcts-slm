def count_ways(n, k):
    MOD = 10**9 + 7
    if k == 1:
        return pow(n, n-1, MOD)
    
    dp = [0] * (n+1)
    dp[1] = 1
    
    for i in range(2, n+1):
        dp[i] = (dp[i-1] * (i-1) + dp[i-2]) % MOD
    
    result = 0
    for i in range(1, k+1):
        result += dp[i]
        result %= MOD
    
    for i in range(k+1, n+1):
        result += dp[i] * pow(i-1, n-i, MOD)
        result %= MOD
    
    return result

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

print(count_ways(n, k))