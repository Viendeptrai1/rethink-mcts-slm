import sys

def find_max_disjoint_blocks(n, a):
    # Calculate prefix sums
    prefix_sums = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sums[i] = prefix_sums[i - 1] + a[i - 1]
    
    # Dictionary to store the sum and corresponding blocks
    sum_blocks = {}
    
    # Try to find blocks with the same sum
    for start in range(1, n + 1):
        for end in range(start, n + 1):
            block_sum = prefix_sums[end] - prefix_sums[start - 1]
            if block_sum not in sum_blocks:
                sum_blocks[block_sum] = []
            sum_blocks[block_sum].append((start, end))
    
    # Find the maximum number of disjoint blocks
    max_blocks = []
    for blocks in sum_blocks.values():
        if len(blocks) > len(max_blocks):
            max_blocks = blocks
    
    # Print the result
    print(len(max_blocks))
    for block in max_blocks:
        print(block[0], block[1])

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Find and print the maximum disjoint blocks
find_max_disjoint_blocks(n, a)