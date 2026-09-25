import sys

def find_max_disjoint_blocks(n, a):
    max_blocks = []
    max_sum = 0
    max_count = 0
    
    # Try all possible block sums
    for target_sum in range(-10**5 * n, 10**5 * n + 1):
        current_sum = 0
        start = 0
        count = 0
        blocks = []
        
        for end in range(n):
            current_sum += a[end]
            
            while current_sum > target_sum and start <= end:
                current_sum -= a[start]
                start += 1
            
            if current_sum == target_sum:
                blocks.append((start + 1, end + 1))
                current_sum -= a[start]
                start += 1
                count += 1
        
        if count > max_count:
            max_count = count
            max_blocks = blocks
            max_sum = target_sum
    
    return max_blocks

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    blocks = find_max_disjoint_blocks(n, a)
    
    print(len(blocks))
    for block in blocks:
        print(block[0], block[1])

if __name__ == "__main__":
    main()