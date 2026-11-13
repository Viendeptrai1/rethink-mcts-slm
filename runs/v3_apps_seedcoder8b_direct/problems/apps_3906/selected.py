def count_random_pictures(n, m):
    MOD = 10**9 + 7

    # Base cases
    if n == 1 or m == 1:
        return 2

    # For larger dimensions, we can use dynamic programming
    # dp[i][j] represents the number of valid pictures for a grid of size i x j
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Initialize base cases
    for j in range(1, m + 1):
        dp[1][j] = 2
    for i in range(1, n + 1):
        dp[i][1] = 2

    # Fill the dp table
    for i in range(2, n + 1):
        for j in range(2, m + 1):
            # The number of valid pictures for i x j grid is the sum of:
            # 1. All valid pictures for (i-1) x j grid
            # 2. All valid pictures for i x (j-1) grid
            # 3. All valid pictures for (i-1) x (j-1) grid
            dp[i][j] = (dp[i-1][j] + dp[i][j-1] + dp[i-1][j-1]) % MOD

    return dp[n][m]

# Read input
n, m = map(int, input().split())

# Calculate and print the result
result = count_random_pictures(n, m)
print(result)