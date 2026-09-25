import sys
from itertools import combinations

def max_sum_divisible_by_k(n, m, k, matrix):
    # Initialize the DP table
    dp = [[0] * (m // 2 + 1) for _ in range(n + 1)]
    
    # Iterate over each row
    for i in range(1, n + 1):
        # Iterate over each possible number of elements to pick from the current row
        for j in range(m // 2 + 1):
            # If we don't pick any element from the current row
            dp[i][j] = dp[i - 1][j]
            
            # Try picking 1 to j elements from the current row
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