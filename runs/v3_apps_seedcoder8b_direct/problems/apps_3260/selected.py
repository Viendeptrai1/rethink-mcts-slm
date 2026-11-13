def count_permutations_with_runs(n, k, p):
    # dp[i][j] will store the number of permutations of length i with the last run of length j
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: There's exactly one permutation of length 0 (the empty permutation)
    dp[0][0] = 1
    
    # Fill the dp table
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            # Add a new run of length j
            dp[i][j] = dp[i - j][0]
            
            # Extend existing runs
            for l in range(1, j):
                dp[i][j] = (dp[i][j] + dp[i - 1][l]) % p
            
            # Add to permutations of length i-1 with no run
            dp[i][0] = (dp[i][0] + dp[i - 1][0]) % p
    
    # Sum up all permutations of length n with any run length
    result = sum(dp[n][j] for j in range(k + 1)) % p
    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, k, p = map(int, data.split())
    print(count_permutations_with_runs(n, k, p))