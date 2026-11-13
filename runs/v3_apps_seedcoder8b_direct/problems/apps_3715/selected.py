def min_rest_days(n, activities):
    # dp[i][0] - minimum rest days if the last day is a rest
    # dp[i][1] - minimum rest days if the last day is doing sport
    # dp[i][2] - minimum rest days if the last day is writing contest
    dp = [[float('inf')] * 3 for _ in range(n)]
    
    # Initialize the first day
    if activities[0] == 0:
        dp[0][0] = 1  # Rest
    elif activities[0] == 2:
        dp[0][1] = 0  # Do sport
    elif activities[0] == 1:
        dp[0][2] = 0  # Write contest

    for i in range(1, n):
        if activities[i] == 0:
            dp[i][0] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2]) + 1
        elif activities[i] == 2:
            dp[i][1] = min(dp[i-1][0], dp[i-1][2])
        elif activities[i] == 1:
            dp[i][2] = min(dp[i-1][0], dp[i-1][1])
        # If activities[i] == 3, both sport and contest can be done
        if activities[i] == 3 or activities[i] == 2:
            dp[i][1] = min(dp[i][1], min(dp[i-1][0], dp[i-1][2]))
        if activities[i] == 3 or activities[i] == 1:
            dp[i][2] = min(dp[i][2], min(dp[i-1][0], dp[i-1][1]))

    # The result is the minimum of resting on the last day or doing sport/contest
    return min(dp[n-1][0], dp[n-1][1], dp[n-1][2])

# Read input
n = int(input().strip())
activities = list(map(int, input().strip().split()))

# Calculate and print the result
print(min_rest_days(n, activities))