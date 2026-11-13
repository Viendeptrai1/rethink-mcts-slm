def max_profit(n, k, a):
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    prev = [[0] * (k + 1) for _ in range(n + 1)]

    for j in range(1, k + 1):
        for i in range(j, n + 1):
            max_difficulty = 0
            for l in range(i - 1, j - 2, -1):
                max_difficulty = max(max_difficulty, a[l])
                if dp[l][j - 1] + max_difficulty > dp[i][j]:
                    dp[i][j] = dp[l][j - 1] + max_difficulty
                    prev[i][j] = l

    # Reconstruct the solution
    solution = []
    i, j = n, k
    while i > 0:
        solution.append(i - prev[i][j])
        i = prev[i][j]

    return dp[n][k], solution[::-1]

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Output
profit, distribution = max_profit(n, k, a)
print(profit)
print(' '.join(map(str, distribution)))