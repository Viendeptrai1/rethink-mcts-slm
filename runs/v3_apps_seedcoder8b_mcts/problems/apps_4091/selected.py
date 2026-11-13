def max_profit_distribution(n, k, a):
    # Initialize dp table and path array
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    path = [[0] * (k + 1) for _ in range(n + 1)]

    # Fill the dp table
    for i in range(1, n + 1):
        max_difficulty = 0
        for j in range(1, min(i, k) + 1):
            max_difficulty = max(max_difficulty, a[i - 1])
            if j == 1:
                dp[i][j] = max_difficulty * i
            else:
                dp[i][j] = dp[i - 1][j - 1] + max_difficulty
            path[i][j] = max_difficulty

    # Reconstruct the solution
    result = [0] * k
    i, j = n, k
    while j > 0:
        max_difficulty = path[i][j]
        count = 0
        while i > 0 and path[i][j] == max_difficulty:
            count += 1
            i -= 1
        result[j - 1] = count
        j -= 1

    # Print the results
    print(dp[n][k])
    print(*result)

# Read input
n, k = map(int, input().split())
a = list(map(int, input().split()))

# Call the function
max_profit_distribution(n, k, a)