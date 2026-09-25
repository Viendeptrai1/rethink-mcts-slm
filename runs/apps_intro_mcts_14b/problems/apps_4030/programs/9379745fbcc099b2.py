import sys

def min_colors_to_sort(s):
    n = len(s)
    dp = [1] * n
    colors = [1] * n
    
    for i in range(1, n):
        if s[i] >= s[i - 1]:
            dp[i] = dp[i - 1]
            colors[i] = colors[i - 1]
        else:
            dp[i] = dp[i - 1] + 1
            colors[i] = dp[i]
    
    return dp[-1], colors

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    res, coloring = min_colors_to_sort(s)
    
    print(res)
    print(' '.join(map(str, coloring)))

if __name__ == "__main__":
    main()