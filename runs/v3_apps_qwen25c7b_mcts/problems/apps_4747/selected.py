import sys
from fractions import Fraction

def max_expected_score(n, k):
    dp = [[Fraction(0)] * (k + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        dp[i][1] = Fraction(i)
    
    for rolls in range(2, k + 1):
        for current_side in range(1, n + 1):
            for next_side in range(1, n + 1):
                dp[current_side][rolls] += dp[next_side][rolls - 1] / n
    
    return dp[n][k]

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    result = max_expected_score(n, k)
    print(result)