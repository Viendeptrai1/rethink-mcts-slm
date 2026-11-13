import sys

MOD = 10**9 + 7

def count_sequences(N, K):
    dp = [[0] * (N + 1) for _ in range(K + 1)]
    dp[0][1] = 1
    
    for i in range(1, K):
        for j in range(1, N + 1):
            dp[i][j] = sum(dp[i-1][k] for k in range(1, min(j, int(N/j)) + 1)) % MOD
    
    return sum(dp[K-1]) % MOD

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    K = int(data[1])
    result = count_sequences(N, K)
    print(result)