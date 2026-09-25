import sys
from collections import defaultdict

def find_max_blocks(n, a):
    max_blocks = []
    max_k = 0
    
    for block_size in range(1, n + 1):
        block_sums = defaultdict(list)
        
        for start in range(n - block_size + 1):
            end = start + block_size - 1
            block_sum = sum(a[start:end + 1])
            block_sums[block_sum].append((start + 1, end + 1))
        
        for blocks in block_sums.values():
            if len(blocks) > max_k:
                max_k = len(blocks)
                max_blocks = blocks
    
    return max_k, max_blocks

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    k, blocks = find_max_blocks(n, a)
    
    print(k)
    for l, r in blocks:
        print(l, r)

if __name__ == "__main__":
    main()