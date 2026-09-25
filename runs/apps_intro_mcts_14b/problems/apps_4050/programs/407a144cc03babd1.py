import sys

def find_blocks(n, a):
    total_sum = sum(a)
    max_k = 0
    best_blocks = []

    # Try all possible block sums
    for block_sum in range(1, total_sum + 1):
        if total_sum % block_sum != 0:
            continue
        k = total_sum // block_sum
        if k > max_k:
            max_k = k
            blocks = []
            current_sum = 0
            start = 1
            for i in range(n):
                current_sum += a[i]
                if current_sum == block_sum:
                    blocks.append((start, i + 1))
                    current_sum = 0
                    start = i + 2
            best_blocks = blocks

    return max_k, best_blocks

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