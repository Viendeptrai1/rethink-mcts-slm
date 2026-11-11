import sys

def max_happiness(n, m, a, subarrays):
    # Initialize the dp table
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Fill the dp table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            l, r = subarrays[j - 1]
            if l <= i <= r:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - 1] + a[i - 1])
            else:
                dp[i][j] = dp[i - 1][j]
    
    return dp[n][m]

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:2 + n]))
subarrays = []
index = 2 + n
for _ in range(m):
    l = int(data[index])
    r = int(data[index + 1])
    subarrays.append((l, r))
    index += 2

# Calculate and print the result
result = max_happiness(n, m, a, subarrays)
print(result)