import sys

def max_expected_score(n, k):
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        dp[i][1] = i
    
    for rolls in range(2, k + 1):
        for sides in range(1, n + 1):
            dp[sides][rolls] = sum(dp[dice][rolls - 1] for dice in range(sides)) / sides
    
    return dp[n][k]

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    result = max_expected_score(n, k)
    print(f"{result:.7f}")