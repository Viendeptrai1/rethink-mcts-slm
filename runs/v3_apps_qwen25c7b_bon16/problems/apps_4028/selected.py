MOD = 10**9 + 7

def count_regular_bracket_sequences(n, s):
    m = len(s)
    if m > 2 * n or m % 2 != 0:
        return 0
    
    dp = [[0] * (m + 1) for _ in range(m + 1)]
    dp[0][0] = 1
    
    for i in range(m):
        for j in range(i + 1):
            if s[i] == '(':
                dp[j + 1][i + 1] += dp[j][i]
                dp[j + 1][i + 1] %= MOD
            else:
                dp[j][i + 1] += dp[j][i]
                dp[j][i + 1] %= MOD
                if j > 0:
                    dp[j - 1][i + 1] += dp[j][i]
                    dp[j - 1][i + 1] %= MOD
    
    result = 0
    open_needed = 0
    close_needed = 0
    balance = 0
    
    for i in range(m):
        if s[i] == '(':
            open_needed += 1
        else:
            close_needed += 1
        
        balance += 1 if s[i] == '(' else -1
    
        if balance < 0:
            break
    
    if balance == 0:
        result = 1
    
    for i in range(open_needed, min(close_needed, 2 * n), 2):
        result *= dp[i // 2][m - 1]
        result %= MOD
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Output the result
print(count_regular_bracket_sequences(n, s))