import sys
from collections import defaultdict

MOD = 10**9 + 7

def count_sequences(n, s):
    # Calculate the number of ways to form a valid sequence of length i with j unmatched opening brackets
    dp = [[0] * (n + 1) for _ in range(2 * n + 1)]
    dp[0][0] = 1
    
    for i in range(1, 2 * n + 1):
        for j in range(n + 1):
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i - 1][j - 1]) % MOD
            if j < n:
                dp[i][j] = (dp[i][j] + dp[i - 1][j + 1]) % MOD
    
    # Calculate the number of ways to form a valid sequence of length 2n - len(s)
    remaining_length = 2 * n - len(s)
    dp_remaining = [[0] * (n + 1) for _ in range(remaining_length + 1)]
    dp_remaining[0][0] = 1
    
    for i in range(1, remaining_length + 1):
        for j in range(n + 1):
            if j > 0:
                dp_remaining[i][j] = (dp_remaining[i][j] + dp_remaining[i - 1][j - 1]) % MOD
            if j < n:
                dp_remaining[i][j] = (dp_remaining[i][j] + dp_remaining[i - 1][j + 1]) % MOD
    
    # Calculate the number of valid sequences containing s as a substring
    result = 0
    for i in range(len(s)):
        if s[i] == '(':
            result = (result + dp_remaining[len(s) - i - 1][i + 1]) % MOD
        else:
            result = (result + dp_remaining[len(s) - i - 1][i]) % MOD
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result = count_sequences(n, s)
    print(result)

if __name__ == "__main__":
    main()