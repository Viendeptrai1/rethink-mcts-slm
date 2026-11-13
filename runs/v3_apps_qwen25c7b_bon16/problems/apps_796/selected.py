import sys
from math import comb

MOD = 10**9 + 7

def count_ways(n, k):
    if n == 1:
        return 1
    dp = [[0] * (k+1) for _ in range(k+1)]
    dp[1][1] = 1
    for i in range(2, k+1):
        dp[i][1] = dp[i-1][1] + (i-1)
        dp[1][i] = dp[1][i-1] + (i-1)
        for j in range(2, k+1):
            dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
    return dp[k][k]

def main():
    n, k = map(int, sys.stdin.readline().split())
    result = count_ways(n, k)
    print(result)

if __name__ == "__main__":
    main()