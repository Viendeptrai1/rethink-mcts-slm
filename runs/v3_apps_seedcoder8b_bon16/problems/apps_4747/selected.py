def expected_score(n, k):
    # Initialize a table to store the expected score for each state
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # If we roll a single die, the expected score is the average of the numbers on the die
    for i in range(1, n + 1):
        dp[i][1] = i / n
    
    # Fill the dp table
    for rolls in range(2, k + 1):
        for sides in range(1, n + 1):
            # Calculate the expected score for sides with 'rolls' rolls
            expected_value = 0
            for face in range(1, sides + 1):
                # The probability of getting each face
                probability = 1 / sides
                # The score would be the face value or the expected score of rerolling
                expected_value += probability * max(face, dp[sides][rolls - 1])
            dp[sides][rolls] = expected_value
    
    return dp[n][k]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, k = map(int, data.split())
    print(expected_score(n, k))