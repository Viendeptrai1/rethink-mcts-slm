import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    M = int(input_data[1])
    K = int(input_data[2])
    
    MOD = 1000007
    
    if K == 0:
        print(1)
        return
    
    if K > N * M:
        print(0)
        return
    
    # We need to compute sum_{i=0}^{min(K, N)} C(K, i) * C(N*M - K + i - 1, i) ??? 
    # Actually, this is a classic stars and bars with upper bounds problem.
    # Generating function: (1 + x + x^2 + ... + x^M)^N = ((1 - x^(M+1)) / (1 - x))^N
    # We want the coefficient of x^K.
    # = (1 - x^(M+1))^N * (1 - x)^(-N)
    # Expand (1 - x^(M+1))^N = sum_{j=0}^{N} C(N, j) * (-1)^j * x^(j*(M+1))
    # Expand (1 - x)^(-N) = sum_{t=0}^{inf} C(N + t - 1, t) * x^t
    # Coefficient of x^K is sum_{j} [ C(N, j) * (-1)^j * C(N + (K - j*(M+1)) - 1, K - j*(M+1)) ]
    # where the term is valid only if K - j*(M+1) >= 0.
    
    ans = 0
    max_j = K // (M + 1)
    if max_j > N:
        max_j = N
    
    for j in range(max_j + 1):
        exponent = K - j * (M + 1)
        if exponent < 0:
            continue
        
        # Term: C(N, j) * (-1)^j * C(N + exponent - 1, exponent)
        # Compute C(n, k) mod MOD
        
        # Helper for combinations
        def nCr_mod(n, r, mod):
            if r < 0 or r > n:
                return 0
            if r == 0 or r == n:
                return 1
            if r > n // 2:
                r = n - r
            
            # Since mod is not necessarily prime (10^6+7 is prime? Let's check: 1000007)
            # 1000007 is a prime number.
            # We can precompute factorials or compute on the fly since N, K <= 10^5.
            # However, n in C(N+exponent-1, exponent) can be up to ~2*10^5.
            # We need factorials up to ~200000.
            return 0 # Placeholder, will implement below

    # Precompute factorials
    limit = N + K + 100
    fact = [1] * limit
    inv = [1] * limit
    for i in range(2, limit):
        fact[i] = (fact[i-1] * i) % MOD
    
    inv[limit-1] = pow(fact[limit-1], MOD - 2, MOD)
    for i in range(limit-2, 1, -1):
        inv[i] = (inv[i+1] * (i+1)) % MOD
    
    def nCr_fast(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    for j in range(max_j + 1):
        exponent = K - j * (M + 1)
        if exponent < 0:
            continue
        
        term1 = nCr_fast(N, j)
        term2 = nCr_fast(N + exponent - 1, exponent)
        term = (term1 * term2) % MOD
        
        if j % 2 == 1:
            ans = (ans - term + MOD) % MOD
        else:
            ans = (ans + term) % MOD
    
    print(ans)

if __name__ == "__main__":
    solve()