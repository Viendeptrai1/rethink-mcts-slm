import sys

def max_expression_value(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    # Initialize base cases
    for i in range(0, n, 2):
        dp[i][i] = int(s[i])
    
    # Fill the dp table
    for length in range(3, n + 1, 2):
        for i in range(0, n - length + 1, 2):
            j = i + length - 1
            for k in range(i + 1, j, 2):
                left = dp[i][k-1]
                right = dp[k+1][j]
                op = s[k]
                
                if op == '+':
                    dp[i][j] = max(dp[i][j], left + right)
                else:  # op == '*'
                    dp[i][j] = max(dp[i][j], left * right)
    
    return dp[0][n-1]

# Read input
s = sys.stdin.readline().strip()

# Calculate and print result
print(max_expression_value(s))