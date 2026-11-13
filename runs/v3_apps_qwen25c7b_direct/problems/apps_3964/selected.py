from collections import deque

def count_good_plans(n, m, b, mod, a):
    dp = [[[-1] * (b + 1) for _ in range(m + 1)] for _ in range(n + 1)]
    
    def dfs(i, j, k):
        if i == n:
            return 1 if j == 0 and k == 0 else 0
        if dp[i][j][k] != -1:
            return dp[i][j][k]
        
        total = 0
        for x in range(j + 1):
            if k >= x * a[i]:
                total = (total + dfs(i + 1, j - x, k - x * a[i])) % mod
        
        dp[i][j][k] = total
        return dp[i][j][k]
    
    return dfs(0, m, b)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    b = int(data[2])
    mod = int(data[3])
    a = list(map(int, data[4:]))
    
    result = count_good_plans(n, m, b, mod, a)
    print(result)