def count_ways(n):
    MOD = 10**9 + 7
    
    # Calculate the number of ways to distribute coins such that Tanya is satisfied
    # For each i, we need a_i + a_{i+1} + a_{i+2} ≠ 6
    # This is equivalent to a_i + a_{i+1} + a_{i+2} ≠ 5 and a_i + a_{i+1} + a_{i+2} ≠ 7
    
    # dp[i][j] will store the number of ways to fill the first i positions with sum j
    dp = [[0] * 6 for _ in range(3 * n + 1)]
    dp[0][0] = 1  # Base case: one way to have sum 0 with 0 elements
    
    for i in range(1, 3 * n + 1):
        for j in range(6):
            for k in range(1, 4):  # k is the number of coins (1, 2, or 3)
                if j - k >= 0:
                    dp[i][j] = (dp[i][j] + dp[i - 1][j - k]) % MOD
    
    # We need to check for each starting point i (0 to n-1)
    total_ways = 0
    for start in range(n):
        valid = True
        for j in range(3):
            sum_triplet = (dp[start + j][5] + dp[start + j][7]) % MOD
            if sum_triplet == 0:
                valid = False
                break
        if valid:
            total_ways = (total_ways + 1) % MOD
    
    return total_ways

# Read input
n = int(input().strip())

# Calculate and print the result
print(count_ways(n))