MOD = 10**9 + 7

def count_random_pictures(n, m):
    if m == 1:
        return 2 ** n % MOD
    
    dp = [[[0, 0], [0, 0]] for _ in range(n)]
    
    # Initialize base case
    for k in range(2):
        for l in range(2):
            dp[0][k][l] = 1
    
    for i in range(1, n):
        for k in range(2):
            for l in range(2):
                dp[i][k][l] = (dp[i-1][k][0] + dp[i-1][k][1]) % MOD
    
    result = 0
    for k in range(2):
        for l in range(2):
            result = (result + dp[n-1][k][l]) % MOD
    
    return result

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])

# Output the result
print(count_random_pictures(n, m))