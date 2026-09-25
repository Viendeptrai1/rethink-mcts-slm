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
        dp[i][0] = min(dp[i - 1][0], a[i])
        dp[i][1] = max(dp[i - 1][1], a[i])
    
    for k in range(m):
        l, r = segments[k]
        if l == 0:
            dp[r][0] = min(dp[r][0], dp[l][0] - 1)
            dp[r][1] = max(dp[r][1], dp[l][1] - 1)
        else:
            dp[r][0] = min(dp[r][0], min(dp[l - 1][0], dp[r][0]) - 1)
            dp[r][1] = max(dp[r][1], max(dp[l - 1][1], dp[r][1]) - 1)
    
    max_diff = dp[-1][1] - dp[-1][0]
    chosen_segments = []
    
    # Backtrack to find the chosen segments
    current_max = dp[-1][1]
    current_min = dp[-1][0]
    
    for k in range(m - 1, -1, -1):
        l, r = segments[k]
        if l == 0:
            if dp[r][1] - 1 == current_max and dp[r][0] - 1 == current_min:
                chosen_segments.append(k + 1)
                current_max -= 1
                current_min -= 1
        else:
            if dp[r][1] - 1 == current_max and dp[r][0] - 1 == current_min:
                chosen_segments.append(k + 1)
                current_max -= 1
                current_min -= 1
            elif dp[r][1] == current_max and dp[r][0] == current_min:
                continue
            elif dp[l - 1][1] - 1 == current_max and dp[l - 1][0] - 1 == current_min:
                chosen_segments.append(k + 1)
                current_max -= 1
                current_min -= 1
            elif dp[l - 1][1] == current_max and dp[l - 1][0] == current_min:
                continue
    
    print(max_diff)
    print(len(chosen_segments))
    print(*chosen_segments[::-1])

if __name__ == "__main__":
    main()