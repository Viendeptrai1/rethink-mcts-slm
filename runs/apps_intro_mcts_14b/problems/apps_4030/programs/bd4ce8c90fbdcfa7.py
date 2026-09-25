import sys

def min_colors_to_sort(s):
    n = len(s)
    dp = [1] * n
    color = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if s[i] >= s[j] and dp[i] < dp[j] + 1:
                dp[i] = dp[j] + 1
                color[i] = color[j]
        if dp[i] == 1:
            color[i] = max(color) + 1
    
    return max(dp), color

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    res, c = min_colors_to_sort(s)
    
    print(res)
    print(" ".join(map(str, c)))

if __name__ == "__main__":
    main()