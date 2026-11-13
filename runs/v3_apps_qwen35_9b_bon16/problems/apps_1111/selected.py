import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(200005)

MOD = 10**9 + 7

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

    # Precompute factorials and inverse factorials for combinations
    max_val = n + 5
    fact = [1] * max_val
    inv = [1] * max_val
    finv = [1] * max_val

    for i in range(2, max_val):
        fact[i] = (fact[i-1] * i) % MOD

    finv[max_val-1] = pow(fact[max_val-1], MOD - 2, MOD)
    for i in range(max_val-2, -1, -1):
        finv[i] = (finv[i+1] * (i+1)) % MOD

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (finv[r] * finv[n-r]) % MOD
        return (num * den) % MOD

    # Precompute prefix sums of weights to quickly get sum of any subset if needed,
    # but actually we will derive the formula analytically.
    
    # Mathematical Derivation:
    # We need to calculate Sum_{R} W(R) where R is a partition of {1..n} into k non-empty subsets.
    # W(R) = sum_{S in R} (|S| * sum_{i in S} w_i)
    # 
    # Let's rewrite the total sum by considering the contribution of each pair (i, j) or just each element i.
    # However, the term is |S| * sum(w_i). This can be seen as: for a subset S, every element w_i in S is added |S| times.
    # So, Total Sum = sum_{partitions R} sum_{S in R} (|S| * sum_{i in S} w_i)
    #                = sum_{partitions R} sum_{i=1}^n w_i * |{S in R : i in S}| * |S|
    # 
    # For a fixed element i, let's consider a specific partition R.
    # Suppose element i is in a subset S of size s. Then w_i contributes s * w_i to W(R).
    # We need to sum s * w_i over all partitions where i is in a subset of size s.
    # By symmetry, for a fixed size s, the number of partitions where a specific element i is in a subset of size s is the same for all i.
    # 
    # Let's count the number of ways to form a partition of n elements into k subsets such that a specific element (say element 1) 
    # belongs to a subset of size s.
    # 1. Choose s-1 other elements from the remaining n-1 elements to be in the same subset as element 1. Ways: C(n-1, s-1).
    # 2. Now we have a "super-element" representing this subset of size s, and n-s remaining individual elements.
    # 3. We need to partition these (n-s + 1) entities into k subsets. The super-element counts as 1 entity.
    #    Wait, the super-element is already formed as one subset. We need to form the remaining k-1 subsets from the remaining n-s elements.
    #    So we need to partition the remaining n-s elements into k-1 non-empty subsets.
    #    The number of ways to partition a set of m elements into p non-empty subsets is Stirling numbers of the second kind S(m, p).
    #    Here m = n-s, p = k-1.
    #    So ways = C(n-1, s-1) * S(n-s, k-1).
    #
    # If element i is in a subset of size s, it contributes s * w_i.
    # Total contribution of w_i across all partitions = w_i * sum_{s=1}^{n-k+1} [ s * C(n-1, s-1) * S(n-s, k-1) ].
    #
    # Since this is the same for all i, the total answer is:
    # (sum_{i=1}^n w_i) * sum_{s=1}^{n-k+1} [ s * C(n-1, s-1) * S(n-s, k-1) ]
    #
    # Let T = sum_{i=1}^n w_i.
    # We need to compute K_sum = sum_{s=1}^{n-k+1} s * C(n-1, s-1) * S(n-s, k-1).
    # Let j = s-1. Then s = j+1. Range of j: 0 to n-k.
    # K_sum = sum_{j=0}^{n-k} (j+1) * C(n-1, j) * S(n-1-j, k-1).
    #
    # We need an efficient way to compute sum_{j} (j+1) * C(n-1, j) * S(n-1-j, k-1).
    # Let m = n-1. We are summing (j+1) * C(m, j) * S(m-j, k-1).
    # Identity: S(n, k) = sum_{i=0}^{n} C(n, i) * S(n-i, k-1) * (i+1)? No.
    #
    # Let's use the recurrence or generating functions.
    # Alternatively, we can compute S(n, k) iteratively. But n is up to 2e5, so O(n) is fine.
    # We need S(x, y) for various x. Specifically x ranges from k-1 to n-1.
    # We can precompute Stirling numbers S(i, j) for i in [0, n] and j in [1, k].
    # Since k can be up to n, we cannot compute the full table O(n^2).
    # But we only need S(n-s, k-1) for varying s. The second argument is fixed at k-1.
    # So we need the sequence S(0, k-1), S(1, k-1), ..., S(n-1, k-1).
    # There is a linear recurrence for fixed k: S(n, k) = k * S(n-1, k) + S(n-1, k-1).
    # This doesn't help directly to compute the whole column S(., k-1) in O(n) without the previous column.
    #
    # However, we can compute the specific sum using the property of Stirling numbers and binomial coefficients.
    # Sum_{j=0}^{m} C(m, j) * S(m-j, k-1) = S(m+1, k). (Standard identity)
    # We have an extra factor (j+1).
    # Sum_{j=0}^{m} (j+1) * C(m, j) * S(m-j, k-1)
    # = Sum_{j=0}^{m} j * C(m, j) * S(m-j, k-1) + Sum_{j=0}^{m} C(m, j) * S(m-j, k-1)
    # The second part is S(m+1, k).
    # The first part: j * C(m, j) = m * C(m-1, j-1).
    # So sum_{j=1}^{m} m * C(m-1, j-1) * S(m-j, k-1)
    # Let p = j-1. Then j = p+1. m-j = m - (p+1) = (m-1) - p.
    # Sum = m * sum_{p=0}^{m-1} C(m-1, p) * S((m-1)-p, k-1)
    # This is m * S(m, k).
    #
    # So the total sum we need is: m * S(m, k) + S(m+1, k), where m = n-1.
    # Target Sum = (n-1) * S(n-1, k) + S(n, k).
    #
    # Wait, let's re-verify the identity.
    # Identity: sum_{j=0}^{n} C(n, j) S(n-j, k) = S(n+1, k+1).
    # Our term: sum_{j} C(m, j) S(m-j, k-1). Here the second arg is fixed.
    # Let N = m-j. Then j = m-N. As j goes 0..m, N goes m..0.
    # Sum_{N=0}^{m} C(m, m-N) S(N, k-1) = Sum_{N=0}^{m} C(m, N) S(N, k-1).
    # This is exactly the identity for S(m+1, k). Correct.
    #
    # Now the weighted sum: sum_{j=0}^{m} (j+1) C(m, j) S(m-j, k-1)
    # = sum_{j} j C(m, j) S(m-j, k-1) + sum_{j} C(m, j) S(m-j, k-1)
    # Term 2: S(m+1, k).
    # Term 1: sum_{j=1}^{m} j C(m, j) S(m-j, k-1) = sum_{j=1}^{m} m C(m-1, j-1) S(m-j, k-1)
    # Let p = j-1. Sum_{p=0}^{m-1} m C(m-1, p) S(m-1-p, k-1)
    # = m * [ sum_{p=0}^{m-1} C(m-1, p) S((m-1)-p, k-1) ]
    # = m * S(m, k).
    #
    # So the multiplier for the total weight sum is: (n-1)*S(n-1, k) + S(n, k).
    #
    # We need to compute S(n, k) and S(n-1, k).
    # We can compute Stirling numbers of the second kind S(n, k) in O(k log MOD) or O(k) or O(n)?
    # Since k can be up to n, O(n) is required.
    # Formula: S(n, k) = 1/k! * sum_{i=0}^{k} (-1)^{k-i} * C(k, i) * i^n.
    # We need S(n, k) and S(n-1, k).
    # We can compute this in O(k log n) using the formula. Given constraints n, k <= 2e5, O(k log n) is acceptable.
    #
    # Algorithm:
    # 1. Read n, k, w.
    # 2. Compute sum_w = sum(w) % MOD.
    # 3. If k > n, output 0 (though problem says k <= n).
    # 4. Compute S_n_k = S(n, k) and S_n_minus_1_k = S(n-1, k) using the inclusion-exclusion formula.
    #    S(N, K) = sum_{i=0}^{K} (-1)^(K-i) * C(K, i) * i^N / K!
    # 5. Result = sum_w * ( (n-1)*S_n_minus_1_k + S_n_k ) % MOD.
    
    if k > n:
        print(0)
        return

    # Precompute factorials for combinations needed in S(n,k) formula
    # We need up to k! for division, and C(k, i) which uses factorials up to k.
    # We already have fact and finv up to n.
    
    # Function to compute S(N, K)
    def compute_stirling(N, K):
        if K == 0:
            return 1 if N == 0 else 0
        if K > N:
            return 0
        res = 0
        # Formula: sum_{i=0}^{K} (-1)^(K-i) * C(K, i) * i^N
        for i in range(K + 1):
            term = (fact[K] * finv[i] * finv[K-i]) % MOD # This is C(K, i)
            # Actually C(K, i) = fact[K] * finv[i] * finv[K-i]
            # But we can simplify: C(K, i) = fact[K] * finv[i] * finv[K-i]
            # Wait, I have fact and finv arrays.
            # C(K, i) = fact[K] * finv[i] * finv[K-i]
            
            # Power i^N
            if i == 0:
                if N == 0:
                    p = 1
                else:
                    p = 0
            else:
                p = pow(i, N, MOD)
            
            term = (term * p) % MOD
            
            if (K - i) % 2 == 1:
                res = (res - term + MOD) % MOD
            else:
                res = (res + term) % MOD
        
        # Divide by K!
        res = (res * finv[K]) % MOD
        return res

    S_n_k = compute_stirling(n, k)
    S_nm1_k = compute_stirling(n - 1, k)
    
    sum_w = sum(w) % MOD
    
    term1 = (sum_w * S_nm1_k) % MOD
    term2 = (sum_w * S_n_k) % MOD
    
    # Multiplier is (n-1)*S(n-1, k) + S(n, k)
    # Wait, the derivation was:
    # Total = sum_w * [ (n-1)*S(n-1, k) + S(n, k) ]
    
    multiplier = ( (n - 1) * S_nm1_k + S_n_k ) % MOD
    ans = (sum_w * multiplier) % MOD
    
    print(ans)

if __name__ == '__main__':
    solve()