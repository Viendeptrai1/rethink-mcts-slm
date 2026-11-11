def count_good_plans(n, m, b, mod, a):
    # Initialize a DP table where dp[i][j] represents the number of ways to distribute j lines among the first i programmers
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 1  # Base case: 1 way to distribute 0 lines among 0 programmers

    # Iterate over each programmer
    for i in range(1, n + 1):
        # Iterate over each possible number of lines
        for j in range(m + 1):
            # Iterate over each possible number of lines the current programmer can write
            for k in range(j + 1):
                # Check if the total number of bugs does not exceed b
                if k * a[i - 1] <= b:
                    dp[i][j] = (dp[i][j] + dp[i - 1][j - k]) % mod

    return dp[n][m]

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
b = int(data[2])
mod = int(data[3])
a = list(map(int, data[4:]))

# Print the result
print(count_good_plans(n, m, b, mod, a))