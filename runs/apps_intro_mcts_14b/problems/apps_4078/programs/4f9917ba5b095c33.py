import sys
from collections import defaultdict

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m = read_ints()
    a = read_ints()
    segments = [read_ints() for _ in range(m)]
    
    # Initialize DP table
    dp = [[-float('inf')] * (1 << m) for _ in range(n + 1)]
    dp[0][0] = 0
    
    # Precompute the effect of each segment
    segment_effect = [defaultdict(int) for _ in range(n + 1)]
    for i, (l, r) in enumerate(segments):
        for j in range(l, r + 1):
            segment_effect[j][1 << i] -= 1
    
    # Fill DP table
    for i in range(1, n + 1):
        for mask in range(1 << m):
            dp[i][mask] = max(dp[i][mask], dp[i - 1][mask])
            if dp[i - 1][mask ^ (1 << (i - 1))] != -float('inf'):
                dp[i][mask] = max(dp[i][mask], dp[i - 1][mask ^ (1 << (i - 1))] + segment_effect[i][mask])
    
    # Find the maximum difference
    max_diff = -float('inf')
    best_mask = 0
    for mask in range(1 << m):
        current_min = min(a[i] + segment_effect[i + 1][mask] for i in range(n))
        current_max = max(a[i] + segment_effect[i + 1][mask] for i in range(n))
        if current_max - current_min > max_diff:
            max_diff = current_max - current_min
            best_mask = mask
    
    # Reconstruct the solution
    selected_segments = []
    for i in range(m):
        if best_mask & (1 << i):
            selected_segments.append(i + 1)
    
    # Output the result
    print(max_diff)
    print(len(selected_segments))
    print(*selected_segments)

if __name__ == "__main__":
    main()