MOD = 10**9 + 7

def count_regular_bracket_sequences(n, s):
    m = len(s)
    if m > 2 * n or m % 2 != 0:
        return 0
    
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(n + 1):
        for j in range(m + 1):
            if i > 0:
                dp[i][j] += dp[i - 1][j]
                dp[i][j] %= MOD
            if j > 0 and j < m and s[j - 1] == '(':
                dp[i][j] += dp[i][j - 1]
                dp[i][j] %= MOD
            if j > 0 and j < m and s[j - 1] == ')' and i > 0:
                dp[i][j] += dp[i - 1][j - 1]
                dp[i][j] %= MOD
    
    result = 0
    for i in range(n + 1):
        result += dp[i][m]
        result %= MOD
    
    return result

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    s = data[1]
    print(count_regular_bracket_sequences(n, s))