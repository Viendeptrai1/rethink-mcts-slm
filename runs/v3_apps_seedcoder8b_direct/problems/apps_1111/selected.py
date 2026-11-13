def sum_of_weights_of_partitions(n, k, weights):
    MOD = 10**9 + 7
    
    # Precompute the prefix sums of weights
    prefix_sums = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sums[i] = (prefix_sums[i - 1] + weights[i - 1]) % MOD
    
    # Function to calculate the sum of weights of a partition
    def calculate_partition_weight(i, j):
        return (j - i + 1) * (prefix_sums[j] - prefix_sums[i - 1]) % MOD
    
    # Dynamic programming table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: one partition with one subset
    for i in range(1, n + 1):
        dp[i][1] = calculate_partition_weight(1, i)
    
    # Fill the dp table
    for subsets in range(2, k + 1):
        for elements in range(subsets, n + 1):
            for partition_point in range(subsets - 1, elements):
                dp[elements][subsets] = (dp[elements][subsets] + 
                                         dp[partition_point][subsets - 1] * 
                                         calculate_partition_weight(partition_point + 1, elements)) % MOD
    
    return dp[n][k]

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
weights = list(map(int, data[2:]))

# Calculate and print the result
result = sum_of_weights_of_partitions(n, k, weights)
print(result)