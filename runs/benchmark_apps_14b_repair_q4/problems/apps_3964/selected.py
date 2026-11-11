def count_good_plans(n, m, b, mod, a):
    # Initialize a DP table where dp[i][j][k] represents the number of ways to distribute j lines among i programmers with k total bugs
    dp = [[[0] * (b + 1) for _ in range(m + 1)] for _ in range(n + 1)]
    dp[0][0][0] = 1  # Base case: 1 way to distribute 0 lines among 0 programmers with 0 bugs

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(m + 1):
            for k in range(b + 1):
                for l in range(j + 1):
                    if j - l >= 0 and l * a[i - 1] <= k:
                        dp[i][j][k] = (dp[i][j][k] + dp[i - 1][j - l][k - l * a[i - 1]]) % mod

    # Sum up all the ways to distribute m lines with total bugs <= b
    result = 0
    for k in range(b + 1):
        result = (result + dp[n][m][k]) % mod

    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
b = int(data[2])
mod = int(data[3])
a = list(map(int, data[4:]))

# Calculate and print the result
print(count_good_plans(n, m, b, mod, a))