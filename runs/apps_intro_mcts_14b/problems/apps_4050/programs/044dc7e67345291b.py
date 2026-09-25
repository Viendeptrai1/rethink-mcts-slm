import sys

def find_max_blocks(n, a):
    # Initialize DP table
    dp = [[0] * n for _ in range(n)]
    block_sums = {}

    # Fill the DP table and track block sums
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += a[j]
            if current_sum in block_sums:
                dp[i][j] = max(dp[i][j], dp[block_sums[current_sum][0]][block_sums[current_sum][1]] + 1)
            else:
                dp[i][j] = 1
            block_sums[current_sum] = (i, j)

    # Find the maximum number of blocks
    max_blocks = 0
    best_i, best_j = 0, 0
    for i in range(n):
        for j in range(i, n):
            if dp[i][j] > max_blocks:
                max_blocks = dp[i][j]
                best_i, best_j = i, j

    # Reconstruct the blocks
    blocks = []
    current_sum = 0
    for i in range(best_i, best_j + 1):
        current_sum += a[i]
        blocks.append((i + 1, i + 1))

    # Print the result
    print(max_blocks)
    for block in blocks:
        print(block[0], block[1])

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Find and print the maximum blocks
find_max_blocks(n, a)