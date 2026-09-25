import sys
from collections import defaultdict

def count_median_pairs(n, m, a):
    # Transform the array to -1, 0, 1 based on comparison with m
    transformed = [0 if x == m else (-1 if x < m else 1) for x in a]
    
    # Prefix sum array
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + transformed[i]
    
    # Count occurrences of each prefix sum
    prefix_count = defaultdict(int)
    for i in range(n + 1):
        prefix_count[prefix_sum[i]] += 1
    
    # Calculate the number of valid subarrays
    count = 0
    for i in range(n + 1):
        # We need prefix_sum[j] - prefix_sum[i] <= 0 and prefix_sum[j] - prefix_sum[i] >= -1
        # This translates to prefix_sum[i] + 0 and prefix_sum[i] + 1
        count += prefix_count[prefix_sum[i]]
        count += prefix_count[prefix_sum[i] + 1]
    
    # Each subarray is counted twice, so we divide by 2
    return count // 2

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:]))

# Output the result
print(count_median_pairs(n, m, a))