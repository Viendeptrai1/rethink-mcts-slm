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
    
    dp = [[float('inf'), float('-inf')] for _ in range(n)]
    dp[0] = [a[0], a[0]]
    
    for i in range(1, n):
        dp[i] = [min(dp[i - 1][0], a[i]), max(dp[i - 1][1], a[i])]
    
    for j in range(m):
        l, r = segments[j]
        new_dp = [dp[i][:] for i in range(n)]
        
        for i in range(l, r + 1):
            new_dp[i][0] = min(new_dp[i][0], dp[i][0] - 1)
            new_dp[i][1] = max(new_dp[i][1], dp[i][1] - 1)
        
        for i in range(r + 1, n):
            new_dp[i][0] = min(new_dp[i - 1][0], new_dp[i][0])
            new_dp[i][1] = max(new_dp[i - 1][1], new_dp[i][1])
        
        for i in range(l - 1, -1, -1):
            new_dp[i][0] = min(new_dp[i + 1][0], new_dp[i][0])
            new_dp[i][1] = max(new_dp[i + 1][1], new_dp[i][1])
        
        if new_dp[-1][1] - new_dp[-1][0] > dp[-1][1] - dp[-1][0]:
            dp = new_dp[:]
    
    max_diff = dp[-1][1] - dp[-1][0]
    
    chosen_segments = []
    current_diff = max_diff
    current_max = dp[-1][1]
    current_min = dp[-1][0]
    
    for j in range(m - 1, -1, -1):
        l, r = segments[j]
        if dp[r][1] - dp[r][0] == current_diff:
            chosen_segments.append(j + 1)
            current_max = dp[r][1]
            current_min = dp[r][0]
            for i in range(r, l - 1, -1):
                current_max = max(current_max, dp[i][1] + 1)
                current_min = min(current_min, dp[i][0] + 1)
            for i in range(r + 1, n):
                current_max = max(current_max, dp[i][1])
                current_min = min(current_min, dp[i][0])
            for i in range(l - 1, -1, -1):
                current_max = max(current_max, dp[i][1])
                current_min = min(current_min, dp[i][0])
            current_diff = current_max - current_min
    
    print(max_diff)
    print(len(chosen_segments))
    print(*chosen_segments[::-1])

if __name__ == "__main__":
    main()