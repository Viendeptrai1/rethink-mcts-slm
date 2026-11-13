def expected_score(n, k):
    # Initialize a table to store expected scores for each state
    dp = [[0.0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: if no rolls are left, the expected score is 0
    for i in range(1, n + 1):
        dp[i][0] = 0.0
    
    # Fill the table for each number of rolls
    for rolls in range(1, k + 1):
        for sides in range(1, n + 1):
            # Calculate the expected score for stopping or rerolling
            expected_reroll = sum(dp[max(1, sides - i)][rolls - 1] for i in range(1, sides + 1)) / sides
            dp[sides][rolls] = (sides + expected_reroll) / 2
    
    # The answer is the expected score for n sides and k rolls
    return dp[n][k]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, k = map(int, data.split())
    print(expected_score(n, k))