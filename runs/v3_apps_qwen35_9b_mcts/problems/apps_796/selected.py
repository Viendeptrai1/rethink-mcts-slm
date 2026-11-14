import sys

# Set recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    k = int(input_data[1])
    
    MOD = 10**9 + 7
    
    # If k is 1, every cell must be 1. 
    # Row min is 1 (satisfied), Col min is 1 (satisfied).
    # Only 1 way.
    if k == 1:
        print(1)
        return
    
    # Precompute factorials and inverse factorials for combinations
    # We need combinations up to n (since we choose subsets of rows/cols)
    # n <= 250, so this is very small.
    
    fact = [1] * (n + 1)
    inv = [1] * (n + 1)
    
    for i in range(1, n + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD
        
    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD
    
    # We use Principle of Inclusion-Exclusion (PIE).
    # Let S be the set of all grids with values in [1, k].
    # Condition A_i: Row i has minimum 1.
    # Condition B_j: Col j has minimum 1.
    # We want the number of grids satisfying ALL A_i and ALL B_j.
    # By PIE: Sum_{I subset of rows, J subset of cols} (-1)^(|I|+|J|) * N(I, J)
    # where N(I, J) is the number of grids where for all i in I, row i does NOT have min 1,
    # and for all j in J, col j does NOT have min 1.
    # Wait, standard PIE for "all conditions satisfied":
    # Total - (at least one fails) + (at least two fail) ...
    # Let P_i be the property that Row i fails (min != 1).
    # Let Q_j be the property that Col j fails (min != 1).
    # We want grids with none of these properties.
    # Sum_{S subset of {rows U cols}} (-1)^|S| * Count(grids where all properties in S hold).
    
    # If a set of rows R_fail and cols C_fail are required to FAIL (i.e., min != 1):
    # For a row to fail (min != 1), all elements in that row must be >= 2.
    # For a col to fail (min != 1), all elements in that col must be >= 2.
    # Intersection of these constraints:
    # Cells in rows R_fail must be >= 2.
    # Cells in cols C_fail must be >= 2.
    # What about cells not in R_fail and not in C_fail?
    # They have no specific constraint from the "failure" conditions, so they can be 1..k.
    # However, we must be careful. The condition "Row i fails" means min(row i) >= 2.
    # This implies EVERY cell in row i is >= 2.
    # Similarly for columns.
    # So if we fix a set of rows R_fail and cols C_fail to fail:
    # - All cells in rows R_fail must be in [2, k].
    # - All cells in cols C_fail must be in [2, k].
    # - Cells at intersection (r in R_fail, c in C_fail) are covered by both, still [2, k].
    # - Cells in rows R_fail but cols not in C_fail: must be [2, k].
    # - Cells in cols C_fail but rows not in R_fail: must be [2, k].
    # - Cells in neither R_fail nor C_fail: can be [1, k].
    
    # Let r = |R_fail|, c = |C_fail|.
    # Number of cells forced to be >= 2:
    # Total cells = n*n.
    # Cells allowed to be 1..k: (n-r)*(n-c).
    # Cells forced to be 2..k: n*n - (n-r)*(n-c).
    # Count = (k-1)^(forced) * k^(allowed).
    # Let A = k-1, B = k.
    # Count(r, c) = A^(n*n - (n-r)*(n-c)) * B^((n-r)*(n-c)).
    # Simplify exponent of A: n^2 - (n^2 - nc - nr + rc) = nc + nr - rc.
    # So Count(r, c) = (k-1)^(nr + nc - rc) * k^((n-r)*(n-c)).
    
    # We sum over all r from 0 to n, c from 0 to n.
    # Number of ways to choose r rows: C(n, r)
    # Number of ways to choose c cols: C(n, c)
    # Sign: (-1)^(r+c)
    
    ans = 0
    A = k - 1
    B = k
    
    # Precompute powers might be slow if done naively inside loop? 
    # n is small (250), so n^2 is 62500. pow(A, exp, MOD) is log(exp). 
    # Total iterations 250*250 = 62500. Each pow takes ~log(62500) ~ 16 ops. 
    # Total ops ~ 10^6, perfectly fine.
    
    for r in range(n + 1):
        for c in range(n + 1):
            # Calculate exponent for A and B
            # forced = n*n - (n-r)*(n-c)
            # allowed = (n-r)*(n-c)
            
            term_rows = n - r
            term_cols = n - c
            
            allowed = (term_rows * term_cols) % (MOD - 1) # Exponent modulo phi(MOD) = MOD-1? 
            # Actually, we can just compute exponent as integer then pow. 
            # Since exponent can be large, we should take mod (MOD-1) for the base exponentiation?
            # Fermat's Little Theorem: a^(p-1) = 1 mod p. So exponents can be mod (MOD-1).
            # However, the exponent itself is n*n - ... which is at most 62500. 
            # So we don't need to mod the exponent, just use it directly. It's small.
            
            allowed_exp = term_rows * term_cols
            forced_exp = n * n - allowed_exp
            
            ways = (pow(A, forced_exp, MOD) * pow(B, allowed_exp, MOD)) % MOD
            
            ways = (ways * nCr(n, r)) % MOD
            ways = (ways * nCr(n, c)) % MOD
            
            if (r + c) % 2 == 1:
                ans = (ans - ways + MOD) % MOD
            else:
                ans = (ans + ways) % MOD
                
    print(ans)

if __name__ == '__main__':
    solve()