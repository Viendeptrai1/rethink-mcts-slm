def count_sequences(N, K):
    MOD = 10**9 + 7
    
    # Initialize a 2D DP array where dp[i][j] represents the number of sequences of length i ending with number j
    dp = [[0] * (N + 1) for _ in range(K + 1)]
    
    # Base case: sequences of length 1
    for j in range(1, N + 1):
        dp[1][j] = 1
    
    # Fill the DP table
    for i in range(2, K + 1):
        for j in range(1, N + 1):
            for x in range(1, N + 1):
                if j * x <= N:
                    dp[i][j] = (dp[i][j] + dp[i - 1][x]) % MOD
    
    # Sum up all sequences of length K
    result = sum(dp[K][j] for j in range(1, N + 1)) % MOD
    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    N, K = map(int, data.split())
    print(count_sequences(N, K))