MOD = 10**9 + 7

def count_regular_sequences(n, s):
    m = len(s)
    dp = [[[0 for _ in range(n+1)] for _ in range(n+1)] for _ in range(m+1)]
    
    dp[0][0][0] = 1
    
    for i in range(1, m+1):
        for j in range(n+1):
            for k in range(n+1):
                if s[i-1] == '(':
                    if j > 0:
                        dp[i][j][k] = (dp[i][j][k] + dp[i-1][j-1][k]) % MOD
                    if k > 0:
                        dp[i][j][k] = (dp[i][j][k] + dp[i-1][j][k-1]) % MOD
                else:
                    if j < n and k > 0:
                        dp[i][j][k] = (dp[i][j][k] + dp[i-1][j+1][k-1]) % MOD
    
    result = 0
    for j in range(n+1):
        result = (result + dp[m][j][n-j]) % MOD
    
    return result

def main():
    n = int(input())
    s = input().strip()
    print(count_regular_sequences(n, s))

if __name__ == "__main__":
    main()