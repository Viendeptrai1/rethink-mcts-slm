import sys
from typing import List

def min_expected_time(n: int, r: int, m: int, tricks: List[List[int]]) -> float:
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    for t, p, d in tricks:
        for j in range(t, n + 1):
            dp[j] = min(dp[j], dp[max(0, j - t)] * (1 - p) + (j - t + d) / p)
    
    return min(dp[n], r)

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    r = int(data[1])
    m = int(data[2])
    
    tricks = []
    index = 3
    for _ in range(m):
        t = int(data[index])
        p = float(data[index + 1])
        d = int(data[index + 2])
        tricks.append([t, p, d])
        index += 3
    
    result = min_expected_time(n, r, m, tricks)
    print(result)