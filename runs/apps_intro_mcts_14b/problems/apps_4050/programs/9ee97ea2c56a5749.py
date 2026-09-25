import sys
from collections import defaultdict

def find_max_blocks(n, a):
    # Calculate prefix sums
    prefix_sum = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + a[i - 1]
    
    # Dictionary to store the last occurrence of each prefix sum
    last_occurrence = {}
    # DP array to store the maximum number of blocks ending at each index
    dp = [0] * (n + 1)
    # Array to store the previous index for reconstruction
    prev = [-1] * (n + 1)
    
    for i in range(1, n + 1):
        dp[i] = dp[i - 1]
        if prefix_sum[i] in last_occurrence:
            j = last_occurrence[prefix_sum[i]]
            if dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
        last_occurrence[prefix_sum[i]] = i
    
    # Reconstruct the blocks
    k = dp[n]
    blocks = []
    current = n
    while current > 0:
        if prev[current] != -1:
            blocks.append((prev[current] + 1, current))
        current = prev[current]
    
    # Print the result
    print(k)
    for block in reversed(blocks):
        print(block[0], block[1])

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Find and print the maximum number of blocks
find_max_blocks(n, a)