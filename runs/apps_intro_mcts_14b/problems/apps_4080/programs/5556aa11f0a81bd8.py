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
    
    # Initialize DP tables
    max_dp = [float('-inf')] * n
    min_dp = [float('inf')] * n
    
    # Base case: no segments applied
    for i in range(n):
        max_dp[i] = a[i]
        min_dp[i] = a[i]
    
    # Apply each segment
    for l, r in segments:
        new_max_dp = max_dp[:]
        new_min_dp = min_dp[:]
        
        for i in range(l, r + 1):
            new_max_dp[i] = max(new_max_dp[i], max_dp[i] - 1)
            new_min_dp[i] = min(new_min_dp[i], min_dp[i] - 1)
        
        max_dp = new_max_dp
        min_dp = new_min_dp
    
    # Calculate the maximum difference
    max_diff = max(max_dp[i] - min_dp[i] for i in range(n))
    
    # Find the subset of segments that achieves this maximum difference
    used_segments = []
    current_max_dp = max_dp[:]
    current_min_dp = min_dp[:]
    
    for l, r in reversed(segments):
        new_max_dp = current_max_dp[:]
        new_min_dp = current_min_dp[:]
        
        for i in range(l, r + 1):
            new_max_dp[i] = max(new_max_dp[i], current_max_dp[i] - 1)
            new_min_dp[i] = min(new_min_dp[i], current_min_dp[i] - 1)
        
        if max(new_max_dp[i] - new_min_dp[i] for i in range(n)) == max_diff:
            used_segments.append((l + 1, r + 1))
            current_max_dp = new_max_dp
            current_min_dp = new_min_dp
    
    # Output the result
    print(max_diff)
    print(len(used_segments))
    for l, r in used_segments:
        print(l, r)

if __name__ == "__main__":
    main()