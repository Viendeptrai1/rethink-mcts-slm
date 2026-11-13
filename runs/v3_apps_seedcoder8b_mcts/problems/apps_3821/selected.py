def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    p = list(map(float, data[1:n+1]))
    
    # Initialize a DP table where dp[i][j] represents the probability of getting exactly j problems
    # from the first i friends.
    dp = [[0.0] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 1.0  # Base case: 100% probability of getting 0 problems from 0 friends
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(n + 1):
            # Probability of not getting a problem from the i-th friend
            dp[i][j] += dp[i-1][j] * (1 - p[i-1])
            # Probability of getting a problem from the i-th friend
            if j > 0:
                dp[i][j] += dp[i-1][j-1] * p[i-1]
    
    # Calculate the probability of Andrey not getting upset
    # This is the probability of getting exactly 1 problem
    probability_not_upset = dp[n][1]
    
    # Print the result with high precision
    print(f"{probability_not_upset:.12f}")

if __name__ == "__main__":
    main()