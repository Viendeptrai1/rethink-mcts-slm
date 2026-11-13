import sys

# Increase recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(2000)

def solve():
    # Read input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    k = int(input_data[1])
    
    MOD = 10**9 + 7
    
    # If k = 1, every cell must be 1.
    # Min of every row is 1 (satisfied). Min of every col is 1 (satisfied).
    # Only 1 way.
    if k == 1:
        print(1)
        return
    
    # We use inclusion-exclusion principle.
    # Total ways without row/col constraints: k^(n*n)
    # But it's easier to count by the number of rows and columns that do NOT contain 1.
    # Let i be the number of rows that do NOT contain 1.
    # Let j be the number of columns that do NOT contain 1.
    # For a valid grid, we must have i = 0 and j = 0.
    #
    # Consider a subset of rows R (size i) and columns C (size j) that are "bad" (no 1s).
    # The cells in these rows must be in [2, k].
    # The cells in these columns must be in [2, k].
    # The intersection cells (R x C) are in [2, k].
    # The cells in R but not in C must be in [2, k].
    # The cells in C but not in R must be in [2, k].
    # The cells not in R and not in C can be anything in [1, k].
    #
    # Actually, let's rephrase:
    # We choose i rows to be "all >= 2".
    # We choose j columns to be "all >= 2".
    # For the chosen i rows, every cell in them must be >= 2.
    # For the chosen j columns, every cell in them must be >= 2.
    # The remaining cells (not in chosen rows and not in chosen columns) can be anything [1, k].
    #
    # Number of ways for fixed i, j:
    # Choose i rows: C(n, i)
    # Choose j cols: C(n, j)
    # Cells in chosen rows (n*j + i*n - i*j cells? No.)
    # Let's count cells:
    # Total cells = n*n.
    # Cells that MUST be >= 2:
    #   - All cells in the i chosen rows: i * n
    #   - All cells in the j chosen cols: j * n
    #   - But the intersection (i*j cells) is counted twice.
    #   - So cells forced >= 2 = i*n + j*n - i*j.
    # Cells that can be anything [1, k]:
    #   - The complement set: (n-i)*(n-j).
    #
    # So for fixed i, j:
    # Ways = C(n, i) * C(n, j) * (k-1)^(i*n + j*n - i*j) * k^((n-i)*(n-j))
    #
    # By Inclusion-Exclusion, the number of valid grids is:
    # Sum_{i=0 to n} Sum_{j=0 to n} (-1)^(i+j) * [Ways(i, j)]
    #
    # We need to compute this sum modulo 10^9+7.
    # Constraints: n <= 250. O(n^2) is acceptable.
    
    # Precompute factorials for combinations
    MAX_N = n + 1
    fact = [1] * MAX_N
    inv = [1] * MAX_N
    for x in range(2, MAX_N):
        fact[x] = (fact[x-1] * x) % MOD
    
    inv[MAX_N-1] = pow(fact[MAX_N-1], MOD - 2, MOD)
    for x in range(MAX_N-2, 1, -1):
        inv[x] = (inv[x+1] * (x+1)) % MOD
    
    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD
    
    # Precompute powers if needed, but n*n is up to 62500, k is large.
    # We need powers of (k-1) and k.
    # Exponents can be up to n*n = 62500.
    # We can compute powers on the fly or precompute.
    # Since we iterate i, j, the exponent changes.
    # Let's precompute powers of (k-1) and k up to n*n.
    
    limit = n * n
    pow_k_minus_1 = [1] * (limit + 1)
    pow_k = [1] * (limit + 1)
    
    base1 = (k - 1) % MOD
    base2 = k % MOD
    
    curr = 1
    for x in range(1, limit + 1):
        curr = (curr * base1) % MOD
        pow_k_minus_1[x] = curr
        
    curr = 1
    for x in range(1, limit + 1):
        curr = (curr * base2) % MOD
        pow_k[x] = curr
        
    ans = 0
    
    for i in range(n + 1):
        for j in range(n + 1):
            # Calculate exponent for (k-1)
            # Cells forced >= 2: i*n + j*n - i*j
            exp1 = i * n + j * n - i * j
            
            # Cells free to be [1, k]: (n-i)*(n-j)
            exp2 = (n - i) * (n - j)
            
            term = (nCr(n, i) * nCr(n, j)) % MOD
            term = (term * pow_k_minus_1[exp1]) % MOD
            term = (term * pow_k[exp2]) % MOD
            
            if (i + j) % 2 == 1:
                ans = (ans - term + MOD) % MOD
            else:
                ans = (ans + term) % MOD
                
    print(ans)

if __name__ == '__main__':
    solve()