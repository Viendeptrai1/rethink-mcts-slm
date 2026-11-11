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
    
    for i in range(k, n + 1):
        # Number of ways to choose i elements out of n
        ways_to_choose = comb(n, i) % MOD
        # Weight contribution of choosing i elements
        weight_contribution = pow(total_weight, i, MOD)
        # Number of ways to partition i elements into k non-empty subsets
        stirling_number = pow(k, i, MOD) * inv_fact[k] % MOD
        # Total contribution to the result
        result = (result + ways_to_choose * weight_contribution * stirling_number) % MOD
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    weights = list(map(int, data[2:]))
    
    print(sum_of_partition_weights(n, k, weights))

if __name__ == "__main__":
    main()