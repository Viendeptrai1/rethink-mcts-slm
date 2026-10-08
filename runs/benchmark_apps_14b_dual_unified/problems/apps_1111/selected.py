import sys
from collections import defaultdict

MOD = 10**9 + 7

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    weights = list(map(int, data[2:]))
    
    # Precompute factorials and their modular inverses
    fact = [1] * (n + 1)
    inv_fact = [1] * (n + 1)
    for i in range(2, n + 1):
        fact[i] = fact[i - 1] * i % MOD
        inv_fact[i] = pow(fact[i], MOD - 2, MOD)
    
    # Precompute binomial coefficients
    binom = [[0] * (k + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        binom[i][0] = 1
        for j in range(1, min(i, k) + 1):
            binom[i][j] = (binom[i - 1][j - 1] + binom[i - 1][j]) % MOD
    
    # Calculate the sum of weights of all partitions
    total_weight = sum(weights)
    result = 0
    
    for i in range(k, n + 1):
        # Number of ways to choose i elements out of n
        ways_to_choose = binom[n][i]
        # Number of ways to partition i elements into k non-empty subsets
        stirling_number = 0
        for j in range(k):
            stirling_number += (-1)**(k - j) * binom[k][j] * pow(j, i, MOD)
        stirling_number %= MOD
        # Total weight contribution of this partition
        weight_contribution = ways_to_choose * stirling_number * pow(total_weight, i, MOD) % MOD
        result = (result + weight_contribution) % MOD
    
    print(result)

if __name__ == "__main__":
    main()