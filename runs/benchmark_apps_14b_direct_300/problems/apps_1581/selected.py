MOD = 10**9 + 7

def count_sequences(N, K):
    dp = [[0] * (N + 1) for _ in range(K + 1)]
    
    for i in range(1, N + 1):
        dp[1][i] = 1
    
    for k in range(2, K + 1):
        for i in range(1, N + 1):
            dp[k][i] = sum(dp[k-1][j] for j in range(1, N//i + 1)) % MOD
    
    return sum(dp[K]) % MOD

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    K = int(data[1])
    result = count_sequences(N, K)
    print(result)