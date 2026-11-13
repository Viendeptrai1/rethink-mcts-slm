import sys

# Set recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(2000)

MOD = 10**9 + 7

def solve():
    # Read input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    k = int(input_data[1])
    
    if n == 1:
        # If n=1, we have a single cell. It must be 1 (min of row and col is 1).
        # So only 1 way if k >= 1. Since k>=1 always, answer is 1.
        print(1)
        return

    # We need to count the number of n x n grids with entries in [1, k]
    # such that min(row i) = 1 for all i, and min(col j) = 1 for all j.
    #
    # Let S be the set of valid grids where every row has a 1 and every col has a 1.
    #
    # Approach using Inclusion-Exclusion Principle on columns:
    # Total grids where every row has at least one 1.
    # For a single row, the number of ways to fill it with numbers in [1, k] 
    # such that there is at least one 1 is: (k^n) - (k-1)^n.
    # Since rows are independent, total ways where every row has a 1 is:
    #   Total_Row_Valid = (k^n - (k-1)^n)^n
    #
    # However, we also need every column to have at least one 1.
    # Let's use Inclusion-Exclusion on the columns.
    # Let U be the set of grids where every row has at least one 1.
    # We want to exclude grids where at least one column has NO 1s.
    #
    # Let P_j be the property that column j contains no 1s.
    # We want to find the number of grids in U that satisfy NONE of P_j.
    # By PIE: Sum_{S subset of cols} (-1)^|S| * N(S)
    # where N(S) is the number of grids in U where for all j in S, column j has no 1s.
    #
    # If a specific set S of columns (size s) must have no 1s, then for each cell in those columns,
    # the value must be in [2, k]. There are (k-1) choices per cell in those columns.
    # The cells in the columns NOT in S can be any value in [1, k], BUT we still have the constraint
    # that EVERY ROW must have at least one 1.
    #
    # Wait, the constraint "every row has at least one 1" applies to the whole grid.
    # If we fix that columns in S have no 1s, then for a row to have a 1, that 1 MUST appear in a column NOT in S.
    # So, for each row, the entries in columns S must be in [2, k] (k-1 choices),
    # and the entries in columns not in S must be chosen such that at least one of them is 1.
    #
    # For a single row:
    #   - Entries in S columns: (k-1)^s ways.
    #   - Entries in complement columns (size n-s): We need at least one 1 in these.
    #     Total ways for complement part: k^(n-s).
    #     Ways with NO 1 in complement part: (k-1)^(n-s).
    #     So valid ways for complement part: k^(n-s) - (k-1)^(n-s).
    #   - Total ways for one row given S: (k-1)^s * (k^(n-s) - (k-1)^(n-s)).
    #
    # Since there are n rows and they are independent:
    #   N(S) = [ (k-1)^s * (k^(n-s) - (k-1)^(n-s)) ]^n
    #
    # The term depends only on s = |S|. There are C(n, s) such sets.
    # Answer = Sum_{s=0 to n} (-1)^s * C(n, s) * [ (k-1)^s * (k^(n-s) - (k-1)^(n-s)) ]^n
    #
    # Let's verify for n=2, k=2:
    # s=0: C(2,0) * [ 1 * (2^2 - 1^2) ]^2 = 1 * (3)^2 = 9
    # s=1: -C(2,1) * [ 1^1 * (2^1 - 1^1) ]^2 = -2 * (1)^2 = -2
    # s=2: +C(2,2) * [ 1^2 * (2^0 - 1^0) ]^2 = 1 * (1-1)^2 = 0
    # Total = 9 - 2 + 0 = 7. Correct.
    
    def power(a, b):
        res = 1
        a %= MOD
        while b > 0:
            if b % 2 == 1:
                res = (res * a) % MOD
            a = (a * a) % MOD
            b //= 2
        return res

    # Precompute factorials for combinations
    # n <= 250, so we can precompute up to 250.
    max_n = n
    fact = [1] * (max_n + 1)
    inv = [1] * (max_n + 1)
    
    for i in range(1, max_n + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[max_n] = power(fact[max_n], MOD - 2)
    for i in range(max_n - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD
        
    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    ans = 0
    
    # Precompute powers if needed, but n is small enough to compute on fly or optimize
    # We iterate s from 0 to n
    for s in range(n + 1):
        # Term inside the bracket for one row
        # part1 = (k-1)^s
        # part2 = k^(n-s) - (k-1)^(n-s)
        # row_ways = part1 * part2
        
        if s == 0:
            term_s = 1
            term_n_minus_s = (power(k, n) - power(k - 1, n) + MOD) % MOD
            row_ways = (term_s * term_n_minus_s) % MOD
        elif s == n:
            # (k-1)^n * (k^0 - (k-1)^0) = (k-1)^n * (1-1) = 0
            # Unless k=1, but if k=1, k-1=0. 
            # If k=1: (0)^n * (1-1) = 0.
            # If k>1: (non-zero) * 0 = 0.
            row_ways = 0
        else:
            term_s = power(k - 1, s)
            term_n_minus_s = (power(k, n - s) - power(k - 1, n - s) + MOD) % MOD
            row_ways = (term_s * term_n_minus_s) % MOD
            
        # N(S) = (row_ways)^n
        n_s = power(row_ways, n)
        
        comb = nCr(n, s)
        
        if s % 2 == 1:
            term = (comb * n_s) % MOD
            ans = (ans - term + MOD) % MOD
        else:
            term = (comb * n_s) % MOD
            ans = (ans + term) % MOD

    print(ans)

if __name__ == '__main__':
    solve()