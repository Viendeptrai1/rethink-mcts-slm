import sys

def count_permutations(n, k, p):
    MOD = p
    
    # Initialize dp table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: There's one way to arrange a single element
    dp[1][1] = 1
    
    # Fill the dp table
    for i in range(2, n + 1):
        for j in range(1, k + 1):
            # Extend the previous run
            dp[i][j] = dp[i - 1][j - 1]
            
            # Start a new run
            if j < k:
                dp[i][1] = (dp[i][1] + dp[i - 1][j]) % MOD
    
    # Sum up all valid permutations of length n
    result = sum(dp[n]) % MOD
    
    return result

# Read input
input_line = sys.stdin.read().strip()
n, k, p = map(int, input_line.split())

# Output the result
print(count_permutations(n, k, p))