MOD = 10**9 + 7

def count_random_pictures(n, m):
    if m == 1:
        return 2 ** n % MOD
    
    # Initialize the first row possibilities
    dp = [[0] * 2 for _ in range(m)]
    dp[0][0] = 1  # All black
    dp[0][1] = 1  # All white
    
    for j in range(1, m):
        new_dp = [[0] * 2 for _ in range(m)]
        new_dp[j][0] = (dp[j-1][0] + dp[j-1][1]) % MOD  # Current column is black
        new_dp[j][1] = (dp[j-1][0] + dp[j-1][1]) % MOD  # Current column is white
        dp = new_dp
    
    total_pictures = sum(dp[m-1]) % MOD
    
    # Each row can be independently chosen in 2^(m-1) ways
    return pow(2, (n-1) * (m-1), MOD) * total_pictures % MOD

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])

# Output the result
print(count_random_pictures(n, m))