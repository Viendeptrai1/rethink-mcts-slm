import sys

def find_blocks(n, a):
    total_sum = sum(a)
    max_k = n
    result = []

    for k in range(1, n + 1):
        if total_sum % k == 0:
            target_sum = total_sum // k
            current_sum = 0
            start = 0
            blocks = []

            for end in range(n):
                current_sum += a[end]
                if current_sum == target_sum:
                    blocks.append((start + 1, end + 1))
                    current_sum = 0
                    start = end + 1

            if len(blocks) == k:
                return blocks

    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    blocks = find_blocks(n, a)
    print(len(blocks))
    for block in blocks:
        print(block[0], block[1])

if __name__ == "__main__":
    main()