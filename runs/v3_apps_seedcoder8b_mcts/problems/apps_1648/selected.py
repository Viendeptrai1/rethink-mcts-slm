def count_arrangements(N, K):
    MOD = 10**9 + 7
    
    # dp[i][j][m] = number of ways to arrange i blue balls and j red balls with exactly m moves
    dp = [[[0] * (K + 1) for _ in range(N - K + 1)] for _ in range(K + 1)]
    
    # Base case: 0 blue balls, 0 red balls, 0 moves
    dp[0][0][0] = 1
    
    for i in range(K + 1):
        for j in range(N - K + 1):
            for m in range(K + 1):
                if i > 0:
                    # Add a blue ball
                    if m == 0:
                        dp[i][j][m + 1] = (dp[i][j][m + 1] + dp[i - 1][j][m]) % MOD
                    else:
                        dp[i][j][m] = (dp[i][j][m] + dp[i - 1][j][m]) % MOD
                if j > 0:
                    # Add a red ball
                    dp[i][j][m] = (dp[i][j][m] + dp[i][j - 1][m]) % MOD
    
    # Collect results for each number of moves from 1 to K
    result = [dp[K][N - K][i] for i in range(1, K + 1)]
    
    for count in result:
        print(count)

# Read input
import sys
input = sys.stdin.read
data = input().strip()
N, K = map(int, data.split())

# Call the function with the input
count_arrangements(N, K)