import sys
from collections import defaultdict

def find_max_blocks(n, a):
    # Calculate prefix sums
    prefix_sum = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + a[i - 1]
    
    # Dictionary to store the last occurrence of each prefix sum
    last_occurrence = {}
    
    # Dictionary to store the blocks for each sum
    blocks_by_sum = defaultdict(list)
    
    # Iterate over the array to find all possible blocks
    for i in range(1, n + 1):
        for j in range(i):
            block_sum = prefix_sum[i] - prefix_sum[j]
            if block_sum != 0:
                continue
            if block_sum not in last_occurrence or j > last_occurrence[block_sum]:
                blocks_by_sum[block_sum].append((j + 1, i))
                last_occurrence[block_sum] = i
    
    # Find the maximum number of blocks
    max_blocks = 0
    best_sum = None
    for block_sum, blocks in blocks_by_sum.items():
        if len(blocks) > max_blocks:
            max_blocks = len(blocks)
            best_sum = block_sum
    
    # Output the result
    print(max_blocks)
    for l, r in blocks_by_sum[best_sum]:
        print(l, r)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Find and print the maximum number of blocks
find_max_blocks(n, a)