MOD = 10**6 + 7

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    K = int(data[2])
    
    # Initialize a DP table where dp[i][j] represents the number of ways to choose j items from i types
    dp = [[0] * (K + 1) for _ in range(N + 1)]
    
    # Base case: There's one way to choose 0 items from any number of types (by choosing nothing)
    for i in range(N + 1):
        dp[i][0] = 1
    
    # Fill the DP table
    for i in range(1, N + 1):
        for j in range(1, K + 1):
            # We can either choose 0 to min(j, M) items from the current type
            for k in range(min(j, M) + 1):
                dp[i][j] = (dp[i][j] + dp[i - 1][j - k]) % MOD
    
    # The answer is the number of ways to choose K items from N types
    print(dp[N][K])

if __name__ == "__main__":
    main()