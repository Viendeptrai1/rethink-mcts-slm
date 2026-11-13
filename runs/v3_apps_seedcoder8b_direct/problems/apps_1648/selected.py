def count_arrangements(N, K):
    MOD = 10**9 + 7

    # dp[i][j] will store the number of ways to arrange i balls with j blue balls
    # such that Takahashi needs exactly j moves to collect all blue balls.
    dp = [[0] * (K + 1) for _ in range(N + 1)]
    dp[0][0] = 1  # Base case: 1 way to arrange 0 balls with 0 blue balls

    for i in range(1, N + 1):
        for j in range(0, min(i, K) + 1):
            # If we place a red ball, it doesn't affect the number of moves
            dp[i][j] = dp[i - 1][j]
            if j > 0:
                # If we place a blue ball, it can either start a new move or continue an existing one
                dp[i][j] = (dp[i][j] + dp[i - 1][j - 1]) % MOD

    # We need to find the number of arrangements for each i from 1 to K
    result = [dp[N][i] for i in range(1, K + 1)]

    for count in result:
        print(count)

# Read input
import sys
input = sys.stdin.read
data = input().strip()
N, K = map(int, data.split())

count_arrangements(N, K)