def max_happiness(n, m, moods, subarrays):
    # Calculate the contribution of each subarray to the flowers' moods
    subarray_contributions = []
    for l, r in subarrays:
        contribution = sum(moods[i - 1] for i in range(l, r + 1))
        subarray_contributions.append(contribution)

    # Use dynamic programming to find the maximum happiness
    # dp[i] will store the maximum happiness we can achieve by considering the first i subarrays
    dp = [0] * (m + 1)

    for i in range(1, m + 1):
        # Option 1: Do not include the i-th subarray
        dp[i] = dp[i - 1]
        # Option 2: Include the i-th subarray
        dp[i] = max(dp[i], dp[i - 1] + subarray_contributions[i - 1])

    return dp[m]

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
moods = list(map(int, data[2:n + 2]))
subarrays = []

index = n + 2
for _ in range(m):
    l = int(data[index])
    r = int(data[index + 1])
    subarrays.append((l, r))
    index += 2

# Calculate and print the result
result = max_happiness(n, m, moods, subarrays)
print(result)