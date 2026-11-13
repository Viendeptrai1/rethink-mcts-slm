def max_profit_distribution(n, k, difficulties):
    # Calculate the maximum profit of solving problems from l to r
    max_profit = [[0] * n for _ in range(n)]
    for i in range(n):
        current_max = difficulties[i]
        for j in range(i, n):
            current_max = max(current_max, difficulties[j])
            max_profit[i][j] = current_max

    # dp[i][j] will store the maximum total profit for the first i problems in j days
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    # track the split points to reconstruct the answer
    split_points = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, min(k, i) + 1):
            # If there's only one day, solve all problems up to i
            if j == 1:
                dp[i][j] = max_profit[0][i - 1]
                split_points[i][j] = 0
            else:
                # Consider the best split point for the last day
                for x in range(split_points[i - 1][j - 1] + 1, i):
                    current_profit = dp[x][j - 1] + max_profit[x][i - 1]
                    if current_profit > dp[i][j]:
                        dp[i][j] = current_profit
                        split_points[i][j] = x

    # Reconstruct the solution
    result = []
    i, j = n, k
    while j > 0:
        start = split_points[i][j]
        result.append(i - start)
        i = start
        j -= 1

    # Output the maximum total profit and the number of problems per day
    result.reverse()
    print(dp[n][k])
    print(" ".join(map(str, result)))

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
difficulties = list(map(int, data[2:]))
max_profit_distribution(n, k, difficulties)