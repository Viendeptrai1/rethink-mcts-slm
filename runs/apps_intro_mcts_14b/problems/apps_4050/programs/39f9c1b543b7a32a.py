import sys
from collections import defaultdict

def find_max_blocks(n, a):
    # Dictionary to store the prefix sums and their last occurrence
    prefix_sums = defaultdict(int)
    prefix_sums[0] = -1
    current_sum = 0
    dp = [0] * n
    prev_block_end = [-1] * n
    
    for i in range(n):
        current_sum += a[i]
        if current_sum in prefix_sums:
            j = prefix_sums[current_sum]
            if dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev_block_end[i] = j
        else:
            dp[i] = dp[i - 1]
            prev_block_end[i] = prev_block_end[i - 1]
        
        prefix_sums[current_sum] = i
    
    # Backtrack to find the blocks
    k = dp[-1]
    blocks = []
    i = n - 1
    while k > 0:
        j = prev_block_end[i]
        blocks.append((j + 2, i + 1))
        i = j
        k -= 1
    
    return k, blocks[::-1]

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