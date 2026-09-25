import sys
from itertools import combinations

def max_sum_divisible_by_k(n, m, k, matrix):
    # Initialize DP table
    dp = [0] * k
    
    for row in matrix:
        new_dp = dp[:]
        # Generate all possible subsets of the current row with size <= m//2
        for r in range(1, min(m // 2 + 1, len(row) + 1)):
            for subset in combinations(row, r):
                subset_sum = sum(subset)
                for i in range(k):
                    new_dp[(i + subset_sum) % k] = max(new_dp[(i + subset_sum) % k], dp[i] + subset_sum)
        dp = new_dp
    
    return dp[0]

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
k = int(data[2])
matrix = []
index = 3
for _ in range(n):
    row = list(map(int, data[index:index + m]))
    matrix.append(row)
    index += m

# Calculate and print the result
result = max_sum_divisible_by_k(n, m, k, matrix)
print(result)