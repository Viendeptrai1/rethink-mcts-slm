import sys
from collections import defaultdict

def main():
    import sys
    import heapq
    import itertools

    def read_ints():
        return list(map(int, sys.stdin.readline().split()))

    n, m = read_ints()
    a = read_ints()
    segments = [read_ints() for _ in range(m)]

    # Initialize the dp table
    dp = [[float('inf')] * (1 << m) for _ in range(n + 1)]
    dp[0][0] = 0

    # Precompute the effect of each segment
    segment_effect = [defaultdict(int) for _ in range(n + 1)]
    for j, (l, r) in enumerate(segments):
        for i in range(l, r + 1):
            segment_effect[i][1 << j] -= 1

    # Fill the dp table
    for i in range(1, n + 1):
        for mask in range(1 << m):
            dp[i][mask] = min(dp[i][mask], dp[i - 1][mask])
            if i > 1:
                dp[i][mask] = min(dp[i][mask], dp[i - 1][mask ^ (1 << (i - 2))])

    # Calculate the maximum and minimum values
    max_val = float('-inf')
    min_val = float('inf')
    best_mask = 0

    for mask in range(1 << m):
        current_max = float('-inf')
        current_min = float('inf')
        for i in range(1, n + 1):
            current_max = max(current_max, a[i - 1] + sum(segment_effect[i][1 << j] for j in range(m) if mask & (1 << j)))
            current_min = min(current_min, a[i - 1] + sum(segment_effect[i][1 << j] for j in range(m) if mask & (1 << j)))
        if current_max - current_min > max_val - min_val:
            max_val = current_max
            min_val = current_min
            best_mask = mask

    # Output the result
    print(max_val - min_val)
    q = bin(best_mask).count('1')
    print(q)
    if q > 0:
        result = []
        for j in range(m):
            if best_mask & (1 << j):
                result.append(j + 1)
        print(*result)

if __name__ == "__main__":
    main()