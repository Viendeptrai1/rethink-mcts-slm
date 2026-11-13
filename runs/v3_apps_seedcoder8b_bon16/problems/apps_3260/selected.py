def count_permutations_with_runs(n, k, p):
    # Initialize dp array.
    # dp[i][j] will be the number of permutations of length i with a last run of length j.
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: a single element permutation has one run of length 1.
    dp[1][1] = 1
    
    for i in range(2, n + 1):
        for j in range(1, min(i, k) + 1):
            # Case where the current run extends the last run by 1
            dp[i][j] = dp[i - 1][j - 1]
            # Case where we start a new run with length 1
            dp[i][1] += dp[i - 1][j]
            dp[i][1] %= p

    # Sum up all cases for permutations of length n with runs of at most k
    result = sum(dp[n][j] for j in range(1, k + 1)) % p
    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, k, p = map(int, data.split())
    print(count_permutations_with_runs(n, k, p))