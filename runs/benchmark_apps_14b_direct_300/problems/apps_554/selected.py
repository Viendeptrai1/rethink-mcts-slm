import sys

def max_happiness(n, m, a, subarrays):
    # Initialize the dp array where dp[i] represents the maximum happiness we can get considering the first i subarrays
    dp = [0] * (1 << m)
    
    # Iterate over all possible subsets of subarrays
    for mask in range(1 << m):
        current_happiness = 0
        # Count how many times each flower appears in the current subset of subarrays
        count = [0] * n
        for j in range(m):
            if mask & (1 << j):
                l, r = subarrays[j]
                for k in range(l-1, r):
                    count[k] += 1
        # Calculate the happiness for the current subset
        for i in range(n):
            current_happiness += a[i] * count[i]
        # Update the dp array
        dp[mask] = current_happiness
    
    # The answer is the maximum value in the dp array
    return max(dp)

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:2+n]))
subarrays = []
index = 2 + n
for _ in range(m):
    l = int(data[index])
    r = int(data[index+1])
    subarrays.append((l, r))
    index += 2

# Print the result
print(max_happiness(n, m, a, subarrays))