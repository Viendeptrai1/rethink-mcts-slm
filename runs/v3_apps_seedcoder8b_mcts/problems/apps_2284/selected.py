def min_cost_preparation_and_printing(n, k, a, b):
    # Initialize a list to store the minimum cost to prepare and print i problems by day j
    dp = [[float('inf')] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 0  # Base case: 0 problems, 0 days, cost is 0

    # Iterate over each problem
    for i in range(1, k + 1):
        # Iterate over each day
        for j in range(1, n + 1):
            # Calculate the cost of preparing and printing the i-th problem on the j-th day
            cost_prep = a[j - 1]
            cost_print = b[j - 1]
            dp[i][j] = min(dp[i][j], dp[i - 1][j - 1] + cost_prep + cost_print)
            # Carry forward the cost from the previous day without preparing the i-th problem
            if j > 1:
                dp[i][j] = min(dp[i][j], dp[i][j - 1])

    # The answer is the minimum cost to prepare and print k problems by the n-th day
    return min(dp[k][j] for j in range(1, n + 1))

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:n + 2]))
b = list(map(int, data[n + 2:2 * n + 2]))

# Output the result
print(min_cost_preparation_and_printing(n, k, a, b))