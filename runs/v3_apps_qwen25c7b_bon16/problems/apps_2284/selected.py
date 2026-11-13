import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])

a = list(map(int, data[2:n+2]))
b = list(map(int, data[n+2:]))

dp = [[float('inf')] * (k+1) for _ in range(n+1)]
dp[0][0] = 0

for i in range(1, n+1):
    dp[i][0] = min(dp[i-1][0], dp[i][0]) + a[i-1]
    for j in range(1, min(i, k)+1):
        dp[i][j] = min(dp[i-1][j], dp[i][j]) + a[i-1]
        dp[i][j] = min(dp[i][j], dp[i-1][j-1] + b[i-1])

print(min(dp[-1][-k:]))