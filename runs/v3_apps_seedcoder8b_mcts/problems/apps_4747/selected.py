def expected_score(n, k):
    # Initialize a DP table where dp[i][j] represents the expected score
    # with i rolls left and j sides on the die.
    dp = [[0.0] * (n + 1) for _ in range(k + 1)]
    
    # Base case: If no rolls are left, the expected score is 0.
    for j in range(1, n + 1):
        dp[0][j] = 0.0
    
    # Fill the DP table
    for i in range(1, k + 1):
        for j in range(1, n + 1):
            # Calculate the expected score for stopping or rerolling
            expected_reroll = sum(dp[i - 1][l] for l in range(1, n + 1)) / n
            expected_stop = j
            dp[i][j] = max(expected_stop, expected_reroll)
    
    # The answer is the maximum expected score with k rolls and n sides
    return dp[k][n]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, k = map(int, data.split())
    print(expected_score(n, k))