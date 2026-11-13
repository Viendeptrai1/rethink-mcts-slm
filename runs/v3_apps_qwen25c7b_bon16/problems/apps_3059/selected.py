import sys
from typing import List

def min_expected_time(n: int, r: int, m: int, tricks: List[List[int]]) -> float:
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    for i in range(1, n + 1):
        dp[i] = i + dp[i - 1]
    
    for t, p, d in tricks:
        ndp = dp[:]
        for j in range(t, n + 1):
            ndp[j] = min(ndp[j], dp[j - t] + (j - t) * (1 - p) + d + dp[t])
        dp = ndp
    
    return min(dp[n:] + [dp[-1]])

input = sys.stdin.read
data = input().split()
n = int(data[0])
r = int(data[1])
m = int(data[2])

tricks = []
for i in range(m):
    t = int(data[3 + 3 * i])
    p = float(data[4 + 3 * i])
    d = int(data[5 + 3 * i])
    tricks.append([t, p, d])

result = min_expected_time(n, r, m, tricks)
print(result)