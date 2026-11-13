def max_profit_distribution(n, k, a):
    # Precompute the maximum difficulty for any subarray starting from each index
    max_difficulty = [0] * n
    max_difficulty[-1] = a[-1]
    for i in range(n - 2, -1, -1):
        max_difficulty[i] = max(a[i], max_difficulty[i + 1])

    # dp[i][j] will store the maximum total profit for the first i problems in j days
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    # path[i][j] will store the number of problems in the last day for the optimal solution
    path = [[0] * (k + 1) for _ in range(n + 1)]

    # Initialize the dp table
    for i in range(1, n + 1):
        dp[i][1] = max_difficulty[i - 1]

    # Fill the dp table
    for j in range(2, k + 1):
        for i in range(j, n + 1):
            for x in range(j - 1, i):
                current_profit = dp[x][j - 1] + max_difficulty[x]
                if current_profit > dp[i][j]:
                    dp[i][j] = current_profit
                    path[i][j] = i - x

    # Reconstruct the solution
    result = []
    i, j = n, k
    while j > 0:
        result.append(path[i][j])
        i -= path[i][j]
        j -= 1

    result.reverse()

    # Output the maximum total profit and the distribution
    print(dp[n][k])
    print(*result)

# Example usage:
# max_profit_distribution(8, 3, [5, 4, 2, 6, 5, 1, 9, 2])