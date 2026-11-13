from sys import stdin, stdout
import math

MOD = 10**9 + 7

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result = (result * i) % MOD
    return result

def inverse_mod(a, m):
    return pow(a, m - 2, m)

def binomial_coefficient(n, k, mod):
    if k > n:
        return 0
    num = factorial(n)
    denom = (factorial(k) * factorial(n - k)) % mod
    return (num * inverse_mod(denom, mod)) % mod

def solve():
    n, k = map(int, stdin.readline().split())
    weights = list(map(int, stdin.readline().split()))
    
    total_weight = sum(weights)
    total_partitions = binomial_coefficient(n, k, MOD)
    
    result = 0
    for i in range(k):
        result += (total_partitions * binomial_coefficient(n, i + 1, MOD) * (total_weight // (i + 1))) % MOD
    
    stdout.write(str(result % MOD) + '\n')

if __name__ == "__main__":
    solve()