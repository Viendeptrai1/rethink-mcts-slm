import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        k = int(next(iterator))
        w = []
        for _ in range(n):
            w.append(int(next(iterator)))
    except StopIteration:
        return

    MOD = 10**9 + 7

    # Precompute factorials and inverse factorials for combinations
    # We need up to n!
    fact = [1] * (n + 1)
    inv = [1] * (n + 1)
    
    for i in range(2, n + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n - 1, 1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD

    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    # Sort weights to help with logic if needed, but actually the formula depends on sum of weights
    # Let's compute prefix sums of weights to quickly get sum of any subset if we were enumerating,
    # but we need a combinatorial approach.
    
    # Let S be the total sum of all weights.
    # Let S_i be the sum of weights of the i-th subset in a partition.
    # The weight of a partition is sum_{j=1 to k} (|S_j| * S_j).
    # We need to sum this over all partitions.
    
    # By linearity of expectation (or summation), we can consider the contribution of each element w_i.
    # However, the term is |S_j| * S_j = sum_{x in S_j} sum_{y in S_j} w_y.
    # So W(R) = sum_{j=1 to k} sum_{x in S_j} sum_{y in S_j} w_y.
    # This can be rewritten as sum_{x, y} w_y * (number of partitions where x and y are in the same subset, multiplied by the size of that subset? No.)
    
    # Let's re-evaluate:
    # W(R) = sum_{S in R} |S| * sum_{x in S} w_x
    #       = sum_{S in R} sum_{x in S} |S| * w_x
    #       = sum_{x in U} w_x * (sum_{S in R, x in S} |S|)
    #
    # For a fixed element x, let's say x is in subset S_j with size s_j.
    # The term contributed by x is w_x * s_j.
    # We need to sum this over all partitions.
    # Total = sum_{x} w_x * (sum_{R} s_j where x is in S_j of R)
    #
    # Due to symmetry, for any two elements x and y, the sum of sizes of the subset containing x is the same.
    # Let T = sum_{R} (size of subset containing a specific element x).
    # Then Total = (sum w_x) * T.
    #
    # Now we need to calculate T.
    # T = sum_{R} |S(x)| where S(x) is the subset containing x in partition R.
    #
    # Consider the structure of partitions. We are partitioning n elements into k non-empty subsets.
    # The number of such partitions is S(n, k) * k! where S(n, k) is Stirling numbers of the second kind.
    # But we need the sum of sizes.
    #
    # Alternative approach:
    # Instead of fixing x, let's consider pairs (x, y) including x=y.
    # W(R) = sum_{S} |S| * sum_{x in S} w_x = sum_{S} sum_{x in S} sum_{y in S} w_y
    #      = sum_{x, y} w_y * (number of partitions where x and y are in the same subset S, and we count |S|? No.)
    #
    # Let's go back to: W(R) = sum_{x, y} w_y * I(x, y in same subset) * (something)?
    # Actually, |S| = sum_{z in S} 1.
    # So |S| * sum_{x in S} w_x = sum_{x in S} w_x * sum_{z in S} 1 = sum_{x in S} sum_{z in S} w_x.
    # So W(R) = sum_{S in R} sum_{x in S} sum_{z in S} w_x
    #         = sum_{x, z in U} w_x * (number of partitions where x and z are in the same subset)
    #
    # Let N(x, z) be the number of partitions of n elements into k non-empty subsets such that x and z are in the same subset.
    # If x == z: x and z are always in the same subset.
    #   Number of partitions = S(n, k) * k! (Total partitions)
    # If x != z: x and z must be in the same subset. We can treat {x, z} as a single super-element?
    #   Not exactly, because the subset can have more elements.
    #   If x and z are in the same subset, we can think of merging x and z into a single entity 'pair'.
    #   Then we are partitioning n-1 entities (the pair + n-2 others) into k non-empty subsets.
    #   Number of ways = S(n-1, k) * k!.
    #
    # So:
    # Contribution of pair (x, z) to the total sum is w_x * (count where x, z together).
    # Total Sum = sum_{x} sum_{z} w_x * Count(x, z)
    #           = sum_{x} w_x * [ Count(x, x) + sum_{z != x} Count(x, z) ]
    #
    # Count(x, x) = Total partitions = S(n, k) * k!
    # Count(x, z) for x != z = S(n-1, k) * k!
    #
    # Let A = S(n, k) * k!
    # Let B = S(n-1, k) * k!
    #
    # Total Sum = sum_{x} w_x * [ A + sum_{z != x} B ]
    #           = sum_{x} w_x * [ A + (n-1) * B ]
    #           = (sum w_x) * [ A + (n-1) * B ]
    #
    # Wait, is this correct?
    # Let's check the logic:
    # W(R) = sum_{S} |S| * sum_{x in S} w_x
    #      = sum_{S} sum_{x in S} w_x * |S|
    #      = sum_{S} sum_{x in S} w_x * sum_{z in S} 1
    #      = sum_{S} sum_{x in S} sum_{z in S} w_x
    #      = sum_{x} sum_{z} w_x * (number of partitions where x and z are in the same subset S)
    #
    # Yes, the logic holds.
    #
    # So we need:
    # 1. Sum of all weights: W_total = sum(w)
    # 2. Total partitions: Total = S(n, k) * k!
    # 3. Partitions with x, z together (x!=z): Together = S(n-1, k) * k!
    #
    # Result = W_total * (Total + (n-1) * Together) % MOD
    #
    # We need to compute Stirling numbers of the second kind S(n, k).
    # Formula: S(n, k) = (1/k!) * sum_{i=0 to k} (-1)^(k-i) * C(k, i) * i^n
    #
    # So:
    # Total = S(n, k) * k! = sum_{i=0 to k} (-1)^(k-i) * C(k, i) * i^n
    # Together = S(n-1, k) * k! = sum_{i=0 to k} (-1)^(k-i) * C(k, i) * i^(n-1)
    #
    # Note: If i=0, 0^n is 0 (for n>=1), 0^(n-1) is 0 (for n-1>=1).
    # Since n >= k >= 1, n >= 1.
    # If n=1, k=1:
    #   Total = sum_{i=0}^1 (-1)^(1-i) C(1, i) i^1 = (-1)^1 C(1,0)*0 + (-1)^0 C(1,1)*1 = 1. Correct (1 partition).
    #   Together = sum_{i=0}^1 (-1)^(1-i) C(1, i) i^0 = 0 + 1*1 = 1. Correct.
    #   Result = w1 * (1 + 0*1) = w1. Correct.
    #
    # Algorithm:
    # 1. Calculate W_total = sum(w) % MOD.
    # 2. Calculate Total = sum_{i=1 to k} (-1)^(k-i) * C(k, i) * i^n % MOD.
    # 3. Calculate Together = sum_{i=1 to k} (-1)^(k-i) * C(k, i) * i^(n-1) % MOD.
    # 4. Ans = W_total * (Total + (n-1) * Together) % MOD.
    
    # Precompute powers? n, k up to 2e5.
    # We need i^n and i^(n-1) for i in 1..k.
    # We can compute these in O(k log n) or O(k) if we precompute powers.
    # Since k <= 2e5, O(k log n) is fine (2e5 * 18 ~ 3.6e6 ops).
    
    # Helper for modular exponentiation
    def power(a, b):
        res = 1
        a %= MOD
        while b > 0:
            if b % 2 == 1:
                res = (res * a) % MOD
            a = (a * a) % MOD
            b //= 2
        return res

    # Calculate Total
    total_partitions = 0
    # Calculate Together
    together_partitions = 0
    
    # We iterate i from 1 to k
    # Term: (-1)^(k-i) * C(k, i) * i^n
    # Sign is positive if (k-i) is even, negative if odd.
    
    for i in range(1, k + 1):
        # Calculate C(k, i)
        # C(k, i) = fact[k] * inv[i] * inv[k-i]
        comb = (fact[k] * inv[i]) % MOD
        comb = (comb * inv[k-i]) % MOD
        
        # Calculate i^n and i^(n-1)
        p_n = power(i, n)
        p_n_minus_1 = power(i, n - 1)
        
        term_total = (comb * p_n) % MOD
        term_together = (comb * p_n_minus_1) % MOD
        
        # Determine sign
        if (k - i) % 2 == 1:
            total_partitions = (total_partitions - term_total + MOD) % MOD
            together_partitions = (together_partitions - term_together + MOD) % MOD
        else:
            total_partitions = (total_partitions + term_total) % MOD
            together_partitions = (together_partitions + term_together) % MOD
            
    # Final calculation
    # Ans = W_total * (Total + (n-1) * Together)
    
    factor = (total_partitions + (n - 1) * together_partitions) % MOD
    ans = (W_total * factor) % MOD
    
    print(ans)

if __name__ == '__main__':
    solve()