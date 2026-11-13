def count_ways_to_fill_grid(n, k):
    MOD = 10**9 + 7
    
    # Base cases
    if n > k:
        return 0
    if n == k:
        return 1
    
    # Initialize dp array
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Fill the base cases
    for j in range(1, k + 1):
        dp[1][j] = 1
    
    # Fill the dp table
    for i in range(2, n + 1):
        for j in range(1, k + 1):
            dp[i][j] = (dp[i][j-1] + dp[i-1][j]) % MOD
    
    # Calculate the result
    result = 1
    for i in range(1, n + 1):
        result = (result * dp[n][k]) % MOD
    
    return result

# Read input
n, k = map(int, input().split())

# Calculate and print the result
print(count_ways_to_fill_grid(n, k))