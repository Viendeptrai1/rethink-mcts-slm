import sys
from collections import defaultdict

def find_max_blocks(n, a):
    prefix_sums = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sums[i] = prefix_sums[i - 1] + a[i - 1]
    
    max_blocks = 0
    best_blocks = []
    
    for block_size in range(1, n + 1):
        blocks = defaultdict(list)
        for start in range(1, n + 1):
            if start + block_size - 1 <= n:
                end = start + block_size - 1
                block_sum = prefix_sums[end] - prefix_sums[start - 1]
                blocks[block_sum].append((start, end))
        
        for block_sum, block_list in blocks.items():
            if len(block_list) > max_blocks:
                max_blocks = len(block_list)
                best_blocks = block_list
    
    print(max_blocks)
    for l, r in best_blocks:
        print(l, r)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    find_max_blocks(n, a)