MOD = 1000000007

def count_ways(n, k):
    def factorial_mod(x):
        result = 1
        for i in range(2, x + 1):
            result = (result * i) % MOD
        return result

    def inv_mod(x):
        return pow(x, MOD - 2, MOD)

    def nCr_mod(n, r):
        if r > n:
            return 0
        return (factorial_mod(n) * inv_mod(factorial_mod(r)) % MOD * inv_mod(factorial_mod(n - r)) % MOD) % MOD

    def count_cycles(n):
        if n == 1:
            return 1
        result = 0
        for i in range(1, n):
            result = (result + nCr_mod(n - 1, i - 1) * count_cycles(i) * count_cycles(n - i)) % MOD
        return result

    total_ways = 0
    for i in range(k + 1, n + 1):
        total_ways = (total_ways + count_cycles(i)) % MOD

    return total_ways

n, k = map(int, input().split())
print(count_ways(n, k))