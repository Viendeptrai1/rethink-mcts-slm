def min_paint(n, m, k, colors, paint):
    inf = float('inf')
    
    # dp[i][j] will store the minimum paint required to color the first i trees with j groups
    dp = [[inf] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0  # Base case: 0 paint to have 0 groups with 0 trees
    
    for i in range(1, n + 1):
        if colors[i - 1] != 0:
            # If the tree is already colored, copy the previous state
            for j in range(k + 1):
                dp[i][j] = dp[i - 1][j]
        else:
            # If the tree is uncolored, try coloring it with each color
            for j in range(1, m + 1):
                for g in range(k + 1):
                    if g == 0:
                        # New group starts
                        dp[i][g + 1] = min(dp[i][g + 1], dp[i - 1][g] + paint[i - 1][j - 1])
                    else:
                        # Continue existing group or start a new one
                        dp[i][g] = min(dp[i][g], dp[i - 1][g] + paint[i - 1][j - 1])
                        dp[i][g + 1] = min(dp[i][g + 1], dp[i - 1][g] + paint[i - 1][j - 1])
    
    # Find the minimum paint required to have exactly k groups
    result = min(dp[n][k], inf)
    return result if result != inf else -1

# Read input
n, m, k = map(int, input().split())
colors = list(map(int, input().split()))
paint = [list(map(int, input().split())) for _ in range(n)]

# Output the result
print(min_paint(n, m, k, colors, paint))