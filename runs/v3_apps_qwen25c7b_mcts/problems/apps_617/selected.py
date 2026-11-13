def max_value_expression(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    for i in range(0, n, 2):
        dp[i][i] = int(s[i])
    
    for length in range(3, n + 1, 2):
        for i in range(0, n - length + 1, 2):
            j = i + length - 1
            for k in range(i + 1, j, 2):
                if s[k] == '+':
                    dp[i][j] = max(dp[i][j], dp[i][k-1] + dp[k+1][j])
                else:
                    dp[i][j] = max(dp[i][j], dp[i][k-1] * dp[k+1][j])
    
    return dp[0][n-1]

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    s = data[0]
    result = max_value_expression(s)
    print(result)