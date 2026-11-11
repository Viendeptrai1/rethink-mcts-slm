def max_profit_distribution(n, k, difficulties):
    # Initialize the DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    # Initialize the parent table to reconstruct the solution
    parent = [[0] * (k + 1) for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            max_difficulty = 0
            for l in range(i, 0, -1):
                max_difficulty = max(max_difficulty, difficulties[l - 1])
                if dp[l - 1][j - 1] + max_difficulty > dp[i][j]:
                    dp[i][j] = dp[l - 1][j - 1] + max_difficulty
                    parent[i][j] = l

    # Reconstruct the solution
    result = []
    current = n
    for day in range(k, 0, -1):
        previous = parent[current][day]
        result.append(current - previous + 1)
        current = previous - 1

    return dp[n][k], result[::-1]

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
difficulties = list(map(int, data[2:]))

# Get the result
max_profit, distribution = max_profit_distribution(n, k, difficulties)

# Print the result
print(max_profit)
print(' '.join(map(str, distribution)))