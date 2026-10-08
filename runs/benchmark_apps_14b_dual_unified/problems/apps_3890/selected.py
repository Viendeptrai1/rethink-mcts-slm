MOD = 1000000007

def count_ways(n, k):
    if k == 1:
        return 1
    
    def factorial_mod(x):
        result = 1
        for i in range(2, x + 1):
            result = (result * i) % MOD
        return result
    
    def inv_mod(x):
        return pow(x, MOD - 2, MOD)
    
    def nCr_mod(n, r):
        return (factorial_mod(n) * inv_mod(factorial_mod(r)) % MOD * inv_mod(factorial_mod(n - r))) % MOD
    
    def count_cycles(n, k):
        if n == k:
            return 1
        return (count_cycles(n - 1, k) + count_cycles(n - 1, k - 1)) % MOD
    
    total_ways = 0
    for i in range(k, n + 1):
        total_ways = (total_ways + nCr_mod(n, i) * count_cycles(i, k)) % MOD
    
    return total_ways

# Read input
n, k = map(int, input().split())

# Output the result
print(count_ways(n, k))