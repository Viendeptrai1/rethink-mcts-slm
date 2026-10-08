MOD = 10**9 + 7

def count_permutations(n, k, p):
    if k == 1:
        return 0 if n > 1 else 1
    
    dp = [[0] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 1
    
    for i in range(1, k + 1):
        dp[i][0] = 0
        for j in range(1, n + 1):
            dp[i][j] = (dp[i][j - 1] + dp[i - 1][j - 1]) % p
            if j >= 2:
                dp[i][j] = (dp[i][j] + dp[i - 1][j - 2]) % p
    
    result = 0
    for i in range(1, k + 1):
        result = (result + dp[i][n]) % p
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
p = int(data[2])

# Output the result
print(count_permutations(n, k, p))