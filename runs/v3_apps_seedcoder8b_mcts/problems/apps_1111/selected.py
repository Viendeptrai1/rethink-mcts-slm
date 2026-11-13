def sum_of_weights_partitions(n, k, weights):
    MOD = 10**9 + 7

    # Precompute the prefix sums of weights
    prefix_sums = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sums[i] = (prefix_sums[i - 1] + weights[i - 1]) % MOD

    # Function to calculate the sum of weights of all partitions
    def calculate_partition_sum(n, k):
        if k == 1:
            return prefix_sums[n] * n % MOD
        if n < k:
            return 0

        # dp[i][j] will store the sum of weights of partitions of i elements into j subsets
        dp = [[0] * (k + 1) for _ in range(n + 1)]

        # Base case: 1 way to partition i elements into 1 subset
        for i in range(1, n + 1):
            dp[i][1] = prefix_sums[i] * i % MOD

        # Fill the dp table
        for i in range(1, n + 1):
            for j in range(2, min(i, k) + 1):
                dp[i][j] = dp[i - 1][j]  # Case where the last element is in a new subset
                for x in range(1, i):
                    dp[i][j] = (dp[i][j] + dp[x][j - 1] * (prefix_sums[i] - prefix_sums[x]) % MOD) % MOD

        return dp[n][k]

    return calculate_partition_sum(n, k)

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
weights = list(map(int, data[2:]))

# Calculate and print the result
result = sum_of_weights_partitions(n, k, weights)
print(result)