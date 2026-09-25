import sys

def find_max_blocks(n, a):
    total_sum = sum(a)
    max_blocks = 0
    best_blocks = []

    # Try all possible block sums
    for block_sum in range(1, total_sum // 2 + 1):
        if total_sum % block_sum != 0:
            continue
        target_blocks = total_sum // block_sum
        used = [False] * n
        current_blocks = []

        # Try to form blocks with the current block_sum
        for i in range(n):
            if used[i]:
                continue
            current_sum = 0
            for j in range(i, n):
                current_sum += a[j]
                if current_sum == block_sum:
                    current_blocks.append((i + 1, j + 1))
                    for k in range(i, j + 1):
                        used[k] = True
                    break

        if len(current_blocks) == target_blocks:
            if len(current_blocks) > max_blocks:
                max_blocks = len(current_blocks)
                best_blocks = current_blocks

    return max_blocks, best_blocks

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    k, blocks = find_max_blocks(n, a)
    print(k)
    for block in blocks:
        print(block[0], block[1])

if __name__ == "__main__":
    main()