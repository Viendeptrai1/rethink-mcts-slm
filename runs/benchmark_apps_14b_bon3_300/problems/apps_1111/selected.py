import sys
from math import comb

MOD = 10**9 + 7

def sum_of_partition_weights(n, k, weights):
    # Precompute factorials and their modular inverses
    fact = [1] * (n + 1)
    inv_fact = [1] * (n + 1)
    for i in range(2, n + 1):
        fact[i] = fact[i - 1] * i % MOD
        inv_fact[i] = pow(fact[i], MOD - 2, MOD)
    
    # Calculate the sum of weights of all partitions
    total_weight = sum(weights)
    result = 0
    
    # Iterate over all possible sizes of the first subset
    for i in range(1, n - k + 2):
        # Choose i elements for the first subset
        choose_i = comb(n, i) % MOD
        # Calculate the weight of the first subset
        weight_i = total_weight * i % MOD
        # Calculate the remaining weight after choosing the first subset
        remaining_weight = total_weight * (n - i) % MOD
        # Calculate the number of ways to partition the remaining elements into k-1 subsets
        ways_to_partition_remaining = pow(k - 1, n - i, MOD)
        # Calculate the contribution of this partition to the result
        contribution = choose_i * weight_i * remaining_weight * ways_to_partition_remaining % MOD
        # Add the contribution to the result
        result = (result + contribution) % MOD
    
    return result

# Read input
n, k = map(int, sys.stdin.readline().split())
weights = list(map(int, sys.stdin.readline().split()))

# Print the result
print(sum_of_partition_weights(n, k, weights))