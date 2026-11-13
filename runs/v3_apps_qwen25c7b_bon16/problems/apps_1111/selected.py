MOD = int(1e9) + 7
import math

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result = (result * i) % MOD
    return result

def power(x, y):
    result = 1
    while y > 0:
        if y % 2 == 1:
            result = (result * x) % MOD
        y //= 2
        x = (x * x) % MOD
    return result

def binomial_coefficient(n, k):
    return factorial(n) * pow(factorial(k), -1, MOD) * pow(factorial(n - k), -1, MOD) % MOD

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    weights = list(map(int, data[2:]))
    
    total_weight = sum(weights)
    ways_to_partition = binomial_coefficient(n, k)
    ways_to_arrange_weights_within_subsets = power(total_weight, k)
    
    result = ways_to_partition * ways_to_arrange_weights_within_subsets % MOD
    print(result)

if __name__ == "__main__":
    solve()