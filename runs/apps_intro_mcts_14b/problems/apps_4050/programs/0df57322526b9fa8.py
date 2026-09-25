import sys
from collections import defaultdict

def find_blocks(n, a):
    total_sum = sum(a)
    max_blocks = 0
    best_partition = []

    # Try all possible block sums
    for block_sum in range(1, total_sum // 2 + 1):
        if total_sum % block_sum != 0:
            continue
        target_count = total_sum // block_sum
        current_sum = 0
        start = 0
        blocks = []

        for end in range(n):
            current_sum += a[end]
            while current_sum > block_sum:
                current_sum -= a[start]
                start += 1
            if current_sum == block_sum:
                blocks.append((start + 1, end + 1))
                current_sum = 0
                start = end + 1

        if len(blocks) > max_blocks:
            max_blocks = len(blocks)
            best_partition = blocks

    return max_blocks, best_partition

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    k, blocks = find_blocks(n, a)
    print(k)
    for l, r in blocks:
        print(l, r)

if __name__ == "__main__":
    main()