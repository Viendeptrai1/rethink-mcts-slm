import sys

MOD = 10**9 + 7

def count_sequences(N, K):
    dp = [[0] * (N + 1) for _ in range(K + 1)]
    
    for j in range(1, N + 1):
        dp[1][j] = 1
    
    for i in range(2, K + 1):
        for j in range(1, N + 1):
            for k in range(1, N // j + 1):
                if j * k <= N:
                    dp[i][j] = (dp[i][j] + dp[i - 1][k]) % MOD
    
    return sum(dp[K]) % MOD

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    K = int(data[1])
    result = count_sequences(N, K)
    print(result)