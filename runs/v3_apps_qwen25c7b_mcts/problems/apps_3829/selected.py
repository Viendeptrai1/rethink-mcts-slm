import sys

def expected_max(m, n):
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][1] = i
    
    for j in range(2, n + 1):
        for i in range(1, m + 1):
            dp[i][j] = sum(dp[k][j-1] for k in range(i, m + 1)) / m
    
    return dp[m][n]

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    m = int(data[0])
    n = int(data[1])
    result = expected_max(m, n)
    print(f"{result:.10f}")