MOD = 10**9 + 7

def count_sequences(N, K):
    # Initialize a 2D list to store the number of ways to form sequences of length i ending with j
    dp = [[0] * (N + 1) for _ in range(K + 1)]

    # Base case: There's exactly one way to form a sequence of length 1 for each ending number
    for j in range(1, N + 1):
        dp[1][j] = 1

    # Fill the dp table for sequences of length 2 to K
    for i in range(2, K + 1):
        for j in range(1, N + 1):
            for k in range(1, N + 1):
                if j * k <= N:
                    dp[i][j] = (dp[i][j] + dp[i-1][k]) % MOD

    # Sum up all ways to form sequences of length K
    result = sum(dp[K][j] for j in range(1, N + 1)) % MOD
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    N, K = map(int, data.split())
    print(count_sequences(N, K))

if __name__ == "__main__":
    main()