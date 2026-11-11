def max_happiness(n, m, a, subarrays):
    # Initialize a DP table where dp[i][j] represents the maximum happiness
    # we can achieve using the first i subarrays and considering the first j flowers.
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Iterate over each subarray
    for i in range(1, m + 1):
        l, r = subarrays[i - 1]
        # Calculate the contribution of this subarray to the happiness
        contribution = 0
        for j in range(l, r + 1):
            contribution += a[j - 1]
        
        # Update the DP table
        for j in range(n + 1):
            if j >= l:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - l] + contribution)
            else:
                dp[i][j] = dp[i - 1][j]
    
    return dp[m][n]

# Read input
import sys
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