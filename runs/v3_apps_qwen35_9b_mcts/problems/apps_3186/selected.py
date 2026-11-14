import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    M = int(input_data[1])
    K = int(input_data[2])
    
    MOD = 1000007
    
    if K > N * M:
        print(0)
        return
    
    # We need the coefficient of x^K in (1 - x^(M+1))^N * (1 - x)^(-N)
    # (1 - x)^( -N ) = sum_{i=0}^{inf} C(N+i-1, i) x^i
    # (1 - x^(M+1))^N = sum_{j=0}^{N} C(N, j) * (-1)^j * x^(j*(M+1))
    
    # Coefficient of x^K is sum_{j} [ C(N, j) * (-1)^j * C(N + (K - j*(M+1)) - 1, K - j*(M+1)) ]
    # where the second term is valid only if K - j*(M+1) >= 0
    
    limit = K // (M + 1)
    if limit > N:
        limit = N
    
    ans = 0
    
    # Precompute factorials for combinations
    max_val = N + K + 5
    fact = [1] * (max_val + 1)
    inv = [1] * (max_val + 1)
    
    for i in range(2, max_val + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[max_val] = pow(fact[max_val], MOD - 2, MOD)
    for i in range(max_val - 1, 1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD
        
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD
    
    for j in range(limit + 1):
        term = nCr_mod(N, j)
        rem = K - j * (M + 1)
        ways = nCr_mod(N + rem - 1, rem)
        term = (term * ways) % MOD
        
        if j % 2 == 1:
            ans = (ans - term + MOD) % MOD
        else:
            ans = (ans + term) % MOD
            
    print(ans)

if __name__ == "__main__":
    solve()