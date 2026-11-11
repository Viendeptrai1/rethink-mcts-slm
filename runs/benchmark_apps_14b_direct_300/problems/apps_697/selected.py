MOD = 998244853

def count_max_prefix_sums(n, m):
    if n == 0:
        return 0
    if m == 0:
        return n * (n + 1) // 2 % MOD
    
    total_sum = 0
    for k in range(max(0, m - n), min(m, n) + 1):
        total_sum += (n - k) * (n - k + 1) // 2 * (m - k) * (m - k + 1) // 2
        total_sum %= MOD
    
    return total_sum

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
print(count_max_prefix_sums(n, m))