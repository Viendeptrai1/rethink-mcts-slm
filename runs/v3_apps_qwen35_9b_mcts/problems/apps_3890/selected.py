import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])
    
    MOD = 1000000007
    
    # Precompute factorials and inverse factorials for combinations
    # Since k is small (<= 8), we can compute combinations directly or precompute up to k
    # We need combinations C(k-1, c-1)
    
    def nCr_mod(n, r, mod):
        if r < 0 or r > n:
            return 0
        num = 1
        den = 1
        for i in range(r):
            num = (num * (n - i)) % mod
            den = (den * (i + 1)) % mod
        return (num * pow(den, mod - 2, mod)) % mod
    
    # The formula derived:
    # Sum over c (cycle size containing node 1) from 1 to k:
    # C(k-1, c-1) * (c-1)! * c^(k-c) * (n-k)^(n-k)
    #
    # Explanation:
    # 1. Choose c-1 nodes from the remaining k-1 nodes to be in the cycle with node 1: C(k-1, c-1)
    # 2. Arrange these c nodes into a cycle containing 1: (c-1)! ways
    # 3. The remaining k-c nodes in {1..k} must eventually reach the cycle. 
    #    In a functional graph where every node has out-degree 1, if we fix the cycle,
    #    the number of ways to attach the remaining k-c nodes such that they all reach the cycle
    #    is c^(k-c). (Each of the k-c nodes can point to any of the c cycle nodes, and recursively
    #    the structure ensures they flow into the cycle).
    # 4. For the nodes {k+1..n} (total n-k nodes), they must NOT reach 1.
    #    This means no node in {k+1..n} can point to any node in {1..k}.
    #    Therefore, each of the n-k nodes must point to one of the other n-k nodes.
    #    This gives (n-k)^(n-k) possibilities.
    
    term2 = pow(n - k, n - k, MOD)
    
    total_ways = 0
    
    for c in range(1, k + 1):
        # C(k-1, c-1)
        comb = nCr_mod(k - 1, c - 1, MOD)
        
        # (c-1)!
        fact_c_minus_1 = 1
        for i in range(1, c):
            fact_c_minus_1 = (fact_c_minus_1 * i) % MOD
            
        # c^(k-c)
        pow_c = pow(c, k - c, MOD)
        
        term = (comb * fact_c_minus_1) % MOD
        term = (term * pow_c) % MOD
        term = (term * term2) % MOD
        
        total_ways = (total_ways + term) % MOD
        
    print(total_ways)

if __name__ == '__main__':
    solve()