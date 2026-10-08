MOD = 10**9 + 7

def count_valid_subsets(N, S):
    dp = [[0] * 3 for _ in range(N + 1)]
    dp[0][0] = 1
    
    for i in range(1, N + 1):
        digit = int(S[i - 1])
        for j in range(3):
            dp[i][j] = dp[i - 1][j]
            if digit != 0:
                dp[i][j] = (dp[i][j] + dp[i - 1][(j + digit) % 3]) % MOD
    
    return (dp[N][0] - 1 + MOD) % MOD

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    S = data[1]
    result = count_valid_subsets(N, S)
    print(result)