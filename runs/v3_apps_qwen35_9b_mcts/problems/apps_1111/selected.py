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
    max_val = n + 5
    fact = [1] * max_val
    inv = [1] * max_val
    finv = [1] * max_val

    for i in range(2, max_val):
        fact[i] = (fact[i-1] * i) % MOD

    inv[max_val-1] = pow(fact[max_val-1], MOD - 2, MOD)
    for i in range(max_val-2, 1, -1):
        inv[i] = (inv[i+1] * (i+1)) % MOD

    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    # Precompute Stirling numbers of the second kind S(n, k)
    # We need S(n, k) for the final count of partitions, but we also need
    # a more general form or a way to compute the sum of sizes.
    #
    # Let's re-derive the contribution of a specific element w_i.
    # Consider an element x. In a partition into k subsets, suppose x is in a subset S of size s.
    # The contribution of x to W(R) is s * w_x.
    # We need to sum s * w_x over all valid partitions.
    # Total contribution of w_x = w_x * (sum over all partitions of size of subset containing x).
    #
    # By symmetry, every element has the same expected behavior.
    # Let T be the total sum of weights over all partitions.
    # T = sum_{partitions R} sum_{S in R} |S| * sum_{x in S} w_x
    # T = sum_{x} w_x * (sum_{partitions R} |S_x|) where S_x is the subset containing x.
    #
    # Let C(n, k, s) be the number of partitions of n elements into k non-empty subsets
    # such that a specific element (say element 1) is in a subset of size s.
    # If element 1 is in a subset of size s, we choose s-1 other elements from the remaining n-1: C(n-1, s-1).
    # The remaining n-s elements must be partitioned into k-1 non-empty subsets: S(n-s, k-1).
    # So, C(n, k, s) = C(n-1, s-1) * S(n-s, k-1).
    #
    # The total contribution factor for w_x is sum_{s=1 to n-k+1} s * C(n, k, s).
    # Note: s can range from 1 to n-k+1 because we need at least k-1 elements for the other k-1 sets.
    # Actually, the max size is n-(k-1) = n-k+1.
    #
    # Let F = sum_{s=1}^{n-k+1} s * C(n-1, s-1) * S(n-s, k-1).
    # Then Answer = (sum(w_i)) * F % MOD.
    #
    # We need to compute S(m, r) for m up to n and r up to k.
    # Since k <= n <= 2e5, we can compute the first row of Stirling numbers iteratively?
    # No, we need S(n-s, k-1) for varying first argument.
    # We can precompute a table S[i][j] for 0 <= i <= n and 0 <= j <= k.
    # Size: 2e5 * 2e5 is too big.
    # However, we only need S(m, k-1) for m from 0 to n.
    # We can compute the sequence S(m, K) for a fixed K as m varies?
    # S(m, K) = S(m-1, K-1) + K * S(m-1, K).
    # If we fix K = k-1, we can compute S(m, k-1) for m=0..n in O(n) time if we have S(m-1, k-2) and S(m-1, k-1).
    # But we need the whole column?
    # Actually, we can compute the entire triangle S[i][j] for j up to k in O(n*k) which is too slow (4e10).
    #
    # Alternative approach:
    # We need sum_{s} s * C(n-1, s-1) * S(n-s, k-1).
    # Let m = n-s. Then s = n-m.
    # Sum becomes sum_{m=k-1}^{n-1} (n-m) * C(n-1, n-m-1) * S(m, k-1)
    # = sum_{m=k-1}^{n-1} (n-m) * C(n-1, m) * S(m, k-1)  [since C(n-1, n-m-1) = C(n-1, m)]
    #
    # We need to compute this sum efficiently.
    # We need values of S(m, k-1) for m in [k-1, n-1].
    # Can we compute the sequence S(m, K) for a fixed K efficiently?
    # Yes, using the recurrence S(m, K) = S(m-1, K-1) + K * S(m-1, K).
    # But this depends on K-1.
    # If we want S(m, k-1) for all m, we need the previous column S(m, k-2).
    # This suggests we need to compute columns up to k-1.
    # Total complexity O(n*k) is too slow.
    #
    # Is there a closed form or generating function?
    # S(m, K) is the coefficient of x^K/K! in (e^x - 1)^m? No.
    # S(m, K) = 1/K! * sum_{j=0}^K (-1)^(K-j) * C(K, j) * j^m.
    #
    # Let's substitute this into our sum:
    # Sum = sum_{m=k-1}^{n-1} (n-m) * C(n-1, m) * [ 1/(k-1)! * sum_{j=0}^{k-1} (-1)^(k-1-j) * C(k-1, j) * j^m ]
    #
    # Swap sums:
    # Sum = 1/(k-1)! * sum_{j=0}^{k-1} [ (-1)^(k-1-j) * C(k-1, j) * sum_{m=k-1}^{n-1} (n-m) * C(n-1, m) * j^m ]
    #
    # Let's analyze the inner sum:
    # Inner(m) = (n-m) * C(n-1, m) * j^m
    # Note that C(n-1, m) * j^m = C(n-1, m) * j^m.
    # Also (n-m) * C(n-1, m) = (n-m) * (n-1)! / (m! (n-1-m)!)
    # = n * (n-1)! / (m! (n-1-m)!) - m * (n-1)! / (m! (n-1-m)!)
    # = n * C(n-1, m) - (n-1)! / ((m-1)! (n-1-m)!)
    # = n * C(n-1, m) - (n-1) * C(n-2, m-1) ? No.
    # m * C(n-1, m) = m * (n-1)! / (m! (n-1-m)!) = (n-1)! / ((m-1)! (n-1-m)!) = (n-1) * C(n-2, m-1) * (n-1)/(n-1)?
    # Actually, m * C(n-1, m) = (n-1) * C(n-2, m-1).
    # So (n-m) * C(n-1, m) = n * C(n-1, m) - (n-1) * C(n-2, m-1).
    #
    # So Inner Sum = sum_{m} [ n * C(n-1, m) * j^m - (n-1) * C(n-2, m-1) * j^m ]
    # = n * sum_{m} C(n-1, m) j^m - (n-1) * sum_{m} C(n-2, m-1) j^m
    #
    # First part: sum_{m=0}^{n-1} C(n-1, m) j^m = (1+j)^(n-1).
    # Second part: let p = m-1. sum_{p=0}^{n-2} C(n-2, p) j^(p+1) = j * (1+j)^(n-2).
    #
    # So Inner Sum = n * (1+j)^(n-1) - (n-1) * j * (1+j)^(n-2).
    #
    # This is valid for j >= 0.
    # If j=0:
    #   Term 1: n * 1^(n-1) = n.
    #   Term 2: (n-1) * 0 * ... = 0.
    #   Result = n.
    #   Formula check: n * 1 - (n-1)*0 = n. Correct.
    #
    # So the total sum F is:
    # F = 1/(k-1)! * sum_{j=0}^{k-1} [ (-1)^(k-1-j) * C(k-1, j) * ( n*(1+j)^(n-1) - (n-1)*j*(1+j)^(n-2) ) ]
    #
    # This allows O(k log n) computation.
    #
    # Edge case: k=1.
    # If k=1, we partition into 1 subset. The only partition is {1, 2, ..., n}.
    # Size is n. Weight = n * sum(w).
    # Formula check:
    # k-1 = 0. Sum j=0 to 0.
    # j=0: (-1)^0 * C(0,0) * [ n*(1)^(n-1) - (n-1)*0 ] = n.
    # F = 1/0! * n = n.
    # Answer = sum(w) * n. Correct.
    #
    # Edge case: k > n. Problem says k <= n.
    #
    # Implementation details:
    # Precompute factorials for C(k-1, j).
    # Compute powers (1+j)^(n-1) and (1+j)^(n-2) for j in 0..k-1.
    # Sum up and multiply by inv_fact[k-1].
    # Finally multiply by sum(w).

    if k == 1:
        total_w = sum(w) % MOD
        ans = (total_w * n) % MOD
        print(ans)
        return

    # Precompute factorials up to k
    # We already have fact and inv up to n, so we can use them.
    # But let's ensure we have inv_fact for k-1.
    # inv array is inverse of factorial. So inv[k-1] is 1/(k-1)!.
    
    # Calculate sum_w
    sum_w = sum(w) % MOD

    # Calculate F
    # F = inv_fact[k-1] * sum_{j=0}^{k-1} ( (-1)^(k-1-j) * C(k-1, j) * Term(j) )
    # Term(j) = n * (1+j)^(n-1) - (n-1) * j * (1+j)^(n-2)
    
    F = 0
    base = k - 1
    
    # Precompute powers if needed, but k is up to 2e5, so O(k log n) is fine.
    # pow(base, exp, mod) is efficient.
    
    for j in range(k):
        # Calculate C(k-1, j)
        # C(n, r) = fact[n] * inv[r] * inv[n-r]
        # Here n=base, r=j
        comb = (fact[base] * inv[j] % MOD) * inv[base - j] % MOD
        
        # Sign
        if (base - j) % 2 == 1:
            sign = -1
        else:
            sign = 1
        
        # Term calculation
        # (1+j)
        val = j + 1
        
        # pow1 = val^(n-1)
        # pow2 = val^(n-2)
        # If n=1, n-2 = -1, but k<=n, if n=1 then k=1 handled above. So n>=2 here.
        
        p1 = pow(val, n - 1, MOD)
        p2 = pow(val, n - 2, MOD)
        
        term = (n * p1) % MOD
        term2 = ((n - 1) * j) % MOD
        term2 = (term2 * p2) % MOD
        
        term = (term - term2) % MOD
        
        contribution = (comb * term) % MOD
        if sign == -1:
            F = (F - contribution) % MOD
        else:
            F = (F + contribution) % MOD
            
    F = (F * inv[base]) % MOD
    
    ans = (sum_w * F) % MOD
    print(ans)

if __name__ == '__main__':
    solve()