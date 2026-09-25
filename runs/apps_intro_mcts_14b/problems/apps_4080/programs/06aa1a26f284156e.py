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
    
    # Create a dictionary to store the segments that affect each position
    pos_to_segments = defaultdict(list)
    for i, (l, r) in enumerate(segments):
        pos_to_segments[l].append(i)
        pos_to_segments[r + 1].append(i)
    
    # Initialize the dp table
    dp = [[0] * (1 << m) for _ in range(n)]
    chosen_segments = [[[] for _ in range(1 << m)] for _ in range(n)]
    
    # Base case
    for mask in range(1 << m):
        dp[0][mask] = a[0]
        for i in pos_to_segments[0]:
            if mask & (1 << i):
                dp[0][mask] -= 1
    
    # Fill the dp table
    for i in range(1, n):
        for mask in range(1 << m):
            dp[i][mask] = dp[i - 1][mask]
            chosen_segments[i][mask] = chosen_segments[i - 1][mask]
            for j in pos_to_segments[i]:
                if mask & (1 << j):
                    new_mask = mask ^ (1 << j)
                    if dp[i][mask] < dp[i - 1][new_mask] - 1:
                        dp[i][mask] = dp[i - 1][new_mask] - 1
                        chosen_segments[i][mask] = chosen_segments[i - 1][new_mask] + [j]
    
    # Find the maximum difference
    max_diff = 0
    best_mask = 0
    for mask in range(1 << m):
        max_val = max(dp[n - 1][mask], dp[0][mask])
        min_val = min(dp[n - 1][mask], dp[0][mask])
        diff = max_val - min_val
        if diff > max_diff:
            max_diff = diff
            best_mask = mask
    
    # Collect the chosen segments
    result_segments = chosen_segments[n - 1][best_mask]
    
    # Output the result
    print(max_diff)
    print(len(result_segments))
    print(' '.join(map(str, [x + 1 for x in result_segments])))

if __name__ == "__main__":
    main()