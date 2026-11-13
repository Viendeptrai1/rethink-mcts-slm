def count_ways_to_fill_grid(n, k):
    MOD = 10**9 + 7
    
    # Initialize a DP table where dp[i][j] represents the number of ways to fill
    # the first i rows and j columns with the given constraints.
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    # Base case: There's exactly one way to fill a 1x1 grid with any number from 1 to k.
    for x in range(1, min(k, n) + 1):
        dp[1][1] += 1
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == 1 and j == 1:
                continue  # Already handled the base case
            # Calculate the number of ways to fill dp[i][j]
            for x in range(1, min(k, i, j) + 1):
                dp[i][j] = (dp[i][j] + dp[i-1][j] + dp[i][j-1] - dp[i-1][j-1]) % MOD
    
    # The answer is the number of ways to fill the entire n x n grid
    return dp[n][n]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, k = map(int, data.split())
    result = count_ways_to_fill_grid(n, k)
    print(result)