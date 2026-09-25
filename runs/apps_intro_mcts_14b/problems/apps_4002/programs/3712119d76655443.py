import sys
from itertools import combinations

def max_sum_divisible_by_k(n, m, k, matrix):
    # Initialize the DP table with -1 (indicating not yet computed)
    dp = [[-1] * (m // 2 + 1) for _ in range(n + 1)]
    dp[0][0] = 0  # Base case: no elements chosen, sum is 0

    for i in range(1, n + 1):
        for j in range(m // 2 + 1):
            # Option 1: Do not take any element from the i-th row
            if dp[i - 1][j] != -1:
                dp[i][j] = max(dp[i][j], dp[i - 1][j])

            # Option 2: Take some elements from the i-th row
            for l in range(1, min(j, m) + 1):
                for comb in combinations(matrix[i - 1], l):
                    current_sum = sum(comb)
                    if (dp[i - 1][j - l] + current_sum) % k == 0:
                        dp[i][j] = max(dp[i][j], dp[i - 1][j - l] + current_sum)

    return dp[n][m // 2]

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

matrix = []
index = 3
for i in range(n):
    row = list(map(int, data[index:index + m]))
    matrix.append(row)
    index += m

# Calculate and print the result
result = max_sum_divisible_by_k(n, m, k, matrix)
print(result)