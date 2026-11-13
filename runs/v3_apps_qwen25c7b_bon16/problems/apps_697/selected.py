MOD = 998244853

def calculate_maximal_prefix_sum(n, m):
    if n == 0:
        return 0
    if m == 0:
        return n * (n + 1) // 2 % MOD
    
    total_sum = 0
    for k in range(1, n + 1):
        max_prefix_sum = max(k, (k * (k - 1)) // 2)
        total_sum += (max_prefix_sum * choose(n, k) * choose(m, n - k)) % MOD
    
    return total_sum % MOD

def choose(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(1, k + 1):
        result = result * (n - i + 1) % MOD
        result = result * pow(i, MOD - 2, MOD) % MOD
    return result

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])

print(calculate_maximal_prefix_sum(n, m))