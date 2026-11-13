def max_profit(n, k, a):
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    max_diff = [0] * (n + 1)
    
    for i in range(1, n + 1):
        max_diff[i] = max(max_diff[i - 1], a[i - 1])
        for j in range(1, min(i, k) + 1):
            dp[i][j] = max(dp[i][j], dp[i - 1][j], dp[i - 1][j - 1] + max_diff[i])
    
    result = []
    remaining_problems = n
    while remaining_problems > 0:
        for j in range(k, 0, -1):
            if dp[remaining_problems][j] != dp[remaining_problems][j - 1]:
                result.append(j)
                remaining_problems -= j
                break
    
    return dp[n][k], result[::-1]

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Output results
total_profit, distribution = max_profit(n, k, a)
print(total_profit)
print(' '.join(map(str, distribution)))