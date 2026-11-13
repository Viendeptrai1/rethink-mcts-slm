MOD = 10**9 + 7

def count_special_numbers(n, k):
    dp = [[0] * (k + 1) for _ in range(1001)]
    dp[0][0] = 1
    
    for i in range(1, 1001):
        dp[i][0] = dp[i - 1][0]
        for j in range(1, min(i, k) + 1):
            dp[i][j] = (dp[i - 1][j] + dp[i - 1][j - 1]) % MOD
    
    def count_bits(x):
        return bin(x).count('1')
    
    result = 0
    for i in range(1, n + 1):
        if count_bits(i) == k:
            result = (result + dp[count_bits(i)][k - 1]) % MOD
    
    return result

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0], 2)
k = int(data[1])

# Output the result
print(count_special_numbers(n, k))