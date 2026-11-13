import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(200000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        K = int(next(iterator))
    except StopIteration:
        return

    MOD = 1000007

    # If K is greater than total available items (N*M), answer is 0
    if K > N * M:
        print(0)
        return

    # We need to compute combinations with repetition constraints.
    # The problem is equivalent to finding the coefficient of x^K in:
    # (1 + x + x^2 + ... + x^M)^N
    # This can be rewritten as ((1 - x^(M+1)) / (1 - x))^N
    # = (1 - x^(M+1))^N * (1 - x)^(-N)
    #
    # Using binomial theorem:
    # (1 - x^(M+1))^N = sum_{i=0}^{N} C(N, i) * (-1)^i * x^(i*(M+1))
    # (1 - x)^(-N) = sum_{j=0}^{\infty} C(N+j-1, j) * x^j
    #
    # We want the coefficient of x^K.
    # Let i*(M+1) + j = K => j = K - i*(M+1)
    # Since j >= 0, we have i*(M+1) <= K => i <= K // (M+1)
    # Also i <= N.
    #
    # Coefficient = sum_{i=0}^{min(N, floor(K/(M+1)))} [ C(N, i) * (-1)^i * C(N + (K - i*(M+1)) - 1, K - i*(M+1)) ]
    #              = sum_{i} [ C(N, i) * (-1)^i * C(N + K - i*(M+1) - 1, N - 1) ]
    # Note: C(a, b) = C(a, a-b). Here C(N + j - 1, j) = C(N + j - 1, N - 1).

    # Precompute factorials and inverse factorials for combinations
    MAX_VAL = N + K + 5
    fact = [1] * MAX_VAL
    inv = [1] * MAX_VAL
    finv = [1] * MAX_VAL

    for i in range(2, MAX_VAL):
        fact[i] = (fact[i-1] * i) % MOD

    inv[MAX_VAL-1] = pow(fact[MAX_VAL-1], MOD - 2, MOD)
    for i in range(MAX_VAL-2, 1, -1):
        inv[i] = (inv[i+1] * (i+1)) % MOD

    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * finv[n-r]) % MOD
        return (num * den) % MOD

    # Wait, I made a mistake in precomputation logic above. 
    # inv array should store inverse of numbers or inverse factorials?
    # Let's restructure: fact stores factorials. finv stores inverse factorials.
    # Re-initialize properly.

    fact = [1] * (MAX_VAL)
    finv = [1] * (MAX_VAL)
    
    for i in range(2, MAX_VAL):
        fact[i] = (fact[i-1] * i) % MOD
    
    finv[MAX_VAL-1] = pow(fact[MAX_VAL-1], MOD - 2, MOD)
    for i in range(MAX_VAL-2, -1, -1):
        finv[i] = (finv[i+1] * (i+1)) % MOD

    def nCr_mod2(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (finv[r] * finv[n-r]) % MOD
        return (num * den) % MOD

    total_ways = 0
    limit = min(N, K // (M + 1))

    for i in range(limit + 1):
        term1 = nCr_mod2(N, i)
        # Calculate power of -1
        sign = -1 if i % 2 == 1 else 1
        
        j = K - i * (M + 1)
        # The second term is C(N + j - 1, j) which is C(N + j - 1, N - 1)
        # But we must be careful if N=0? Constraints say N>=1.
        # If N=1, C(j, 0) = 1.
        # Formula: C(N + j - 1, j)
        
        n_comb = N + j - 1
        r_comb = j
        
        term2 = nCr_mod2(n_comb, r_comb)
        
        term = (term1 * term2) % MOD
        if sign == -1:
            total_ways = (total_ways - term + MOD) % MOD
        else:
            total_ways = (total_ways + term) % MOD

    print(total_ways)

if __name__ == "__main__":
    solve()