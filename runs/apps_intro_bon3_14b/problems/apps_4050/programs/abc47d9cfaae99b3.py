import sys
from collections import defaultdict

def find_max_disjoint_blocks(n, a):
    total_sum = sum(a)
    max_blocks = 0
    best_partition = []

    # Try all possible block sizes
    for block_size in range(1, n + 1):
        if total_sum % block_size != 0:
            continue
        target_sum = total_sum // block_size
        current_sum = 0
        start = 1
        blocks = []

        for end in range(1, n + 1):
            current_sum += a[end - 1]
            if end - start + 1 == block_size:
                if current_sum == target_sum:
                    blocks.append((start, end))
                current_sum -= a[start - 1]
                start += 1

        if len(blocks) > max_blocks:
            max_blocks = len(blocks)
            best_partition = blocks

    print(max_blocks)
    for block in best_partition:
        print(block[0], block[1])

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Find and print the maximum disjoint blocks
find_max_disjoint_blocks(n, a)