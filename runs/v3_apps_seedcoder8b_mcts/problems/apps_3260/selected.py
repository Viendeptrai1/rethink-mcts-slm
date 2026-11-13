def count_permutations_with_runs(n, k, p):
    # dp[i][j] will store the number of permutations of length i with the last run of length j
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: A single permutation of length 1 has exactly one run of length 1
    dp[1][1] = 1
    
    # Fill the dp table
    for i in range(2, n + 1):
        for j in range(1, k + 1):
            # If the last run is of length j, we can extend it
            dp[i][j] = dp[i - 1][j] * j % p
            
            # If the last run is of length j-1, we can start a new run of length j
            if j > 1:
                dp[i][j] = (dp[i][j] + dp[i - 1][j - 1]) % p
            
            # Add permutations where the last run is of length 1
            dp[i][1] = (dp[i][1] + dp[i - 1][j]) % p
    
    # Sum up all permutations of length n with runs of length at most k
    result = sum(dp[n][j] for j in range(1, k + 1)) % p
    
    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, k, p = map(int, data.split())
    print(count_permutations_with_runs(n, k, p))