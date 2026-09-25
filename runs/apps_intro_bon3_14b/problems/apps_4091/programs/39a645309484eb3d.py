import sys

def max_profit_distribution(n, k, difficulties):
    # Initialize the dp table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    # Initialize the path table to reconstruct the solution
    path = [[0] * (k + 1) for _ in range(n + 1)]

    # Fill the dp table
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            if j == 1:
                dp[i][j] = max(difficulties[:i])
                path[i][j] = i
            else:
                current_max = 0
                best_split = 0
                for split in range(j - 1, i):
                    current_max = max(current_max, difficulties[split])
                    if dp[split][j - 1] + current_max > dp[i][j]:
                        dp[i][j] = dp[split][j - 1] + current_max
                        best_split = split
                path[i][j] = best_split

    # Reconstruct the solution
    result = []
    current = n
    for day in range(k, 0, -1):
        result.append(current - path[current][day])
        current = path[current][day]

    return dp[n][k], result[::-1]

# Read input
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