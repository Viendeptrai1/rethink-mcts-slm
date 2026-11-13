def count_ways(N, M, K):
    MOD = 10**6 + 7
    
    # dp[i][j] will store the number of ways to distribute j items into i bins
    dp = [[0] * (K + 1) for _ in range(N + 1)]
    
    # Base case: There's one way to distribute 0 items into 0 bins
    dp[0][0] = 1
    
    for i in range(1, N + 1):
        for j in range(K + 1):
            # Ways to distribute j items into i bins without using the i-th bin
            dp[i][j] = dp[i - 1][j]
            
            # Ways to distribute j items into i bins using the i-th bin
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i][j - 1]) % MOD
            
            # Subtract the overcounted cases where the i-th bin is empty
            if j > M:
                dp[i][j] = (dp[i][j] - dp[i - 1][j - M - 1] + MOD) % MOD
    
    return dp[N][K]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    N, M, K = map(int, data.split())
    print(count_ways(N, M, K))