import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    a = list(map(int, data[index:index + n]))
    index += n
    
    segments = []
    for _ in range(m):
        l = int(data[index]) - 1
        r = int(data[index + 1]) - 1
        segments.append((l, r))
        index += 2
    
    # Initialize the dp table
    dp = [[0] * (1 << m) for _ in range(n)]
    parent = [[None] * (1 << m) for _ in range(n)]
    
    # Base case
    for i in range(n):
        dp[i][0] = a[i]
    
    # Fill the dp table
    for mask in range(1, 1 << m):
        for i in range(n):
            for j in range(m):
                if mask & (1 << j):
                    l, r = segments[j]
                    if l <= i <= r:
                        new_mask = mask ^ (1 << j)
                        if dp[i][mask] < dp[i][new_mask] - 1:
                            dp[i][mask] = dp[i][new_mask] - 1
                            parent[i][mask] = (i, new_mask)
    
    # Find the maximum difference
    max_diff = float('-inf')
    best_mask = 0
    for i in range(n):
        for mask in range(1 << m):
            if dp[i][mask] - min(dp[j][mask] for j in range(n)) > max_diff:
                max_diff = dp[i][mask] - min(dp[j][mask] for j in range(n))
                best_mask = mask
    
    # Reconstruct the path
    result = []
    current = best_mask
    for i in range(n):
        if current == 0:
            break
        if parent[i][current] is not None:
            prev_i, prev_mask = parent[i][current]
            for j in range(m):
                if (prev_mask ^ current) & (1 << j):
                    result.append(j + 1)
                    break
            current = prev_mask
    
    # Output the result
    print(max_diff)
    print(len(result))
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()