import sys
from itertools import combinations

def max_sum_divisible_by_k(n, m, k, matrix):
    # Initialize dp array with -infinity
    dp = [-float('inf')] * k
    dp[0] = 0
    
    for row in matrix:
        # Create a new dp array to store the updated values
        new_dp = dp[:]
        # Iterate over all possible subset sizes (0 to floor(m/2))
        for subset_size in range(1, min(m // 2, m) + 1):
            # Generate all combinations of the current subset size
            for combo in combinations(row, subset_size):
                subset_sum = sum(combo)
                # Update the new_dp array
                for i in range(k):
                    new_dp[(i + subset_sum) % k] = max(new_dp[(i + subset_sum) % k], dp[i] + subset_sum)
        # Update the dp array with the new values
        dp = new_dp[:]
    
    # The maximum sum divisible by k is stored in dp[0]
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