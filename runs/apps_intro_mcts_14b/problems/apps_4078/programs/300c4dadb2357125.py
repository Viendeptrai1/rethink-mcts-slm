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
    
    # Initialize DP table
    dp = [[float('inf'), float('-inf')] for _ in range(n)]
    dp[0] = [a[0], a[0]]
    
    # Track the segments used to achieve the DP values
    prev_segments = [[] for _ in range(n)]
    
    for i in range(1, n):
        dp[i] = [a[i], a[i]]
        for j, (l, r) in enumerate(segments):
            if l <= i <= r:
                new_min = min(dp[i][0], dp[l][0] - (i - l + 1))
                new_max = max(dp[i][1], dp[l][1] - (i - l + 1))
                if new_min < dp[i][0] or (new_min == dp[i][0] and new_max > dp[i][1]):
                    dp[i] = [new_min, new_max]
                    prev_segments[i] = prev_segments[l] + [j]
    
    # Find the maximum difference
    max_diff = 0
    best_index = 0
    for i in range(n):
        diff = dp[i][1] - dp[i][0]
        if diff > max_diff:
            max_diff = diff
            best_index = i
    
    # Backtrack to find the segments used
    used_segments = prev_segments[best_index]
    
    # Output the result
    print(max_diff)
    print(len(used_segments))
    print(" ".join(map(lambda x: str(x + 1), used_segments)))

if __name__ == "__main__":
    main()