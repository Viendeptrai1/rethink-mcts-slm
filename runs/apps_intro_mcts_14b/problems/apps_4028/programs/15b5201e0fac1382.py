import sys

MOD = 10**9 + 7

def count_valid_sequences(n, s):
    # Calculate the number of valid sequences of length 2n containing s as a substring
    len_s = len(s)
    
    # dp[i][j] will store the number of valid sequences of length i with j unmatched opening brackets
    dp = [[0] * (n + 1) for _ in range(2 * n + 1)]
    dp[0][0] = 1
    
    # Fill the dp table for sequences before s
    for i in range(len_s):
        if s[i] == '(':
            for j in range(n):
                dp[i + 1][j + 1] = (dp[i + 1][j + 1] + dp[i][j]) % MOD
        else:
            for j in range(1, n + 1):
                dp[i + 1][j - 1] = (dp[i + 1][j - 1] + dp[i][j]) % MOD
    
    # dp_before[len_s][j] will store the number of valid sequences of length len_s with j unmatched opening brackets
    dp_before = [dp[len_s][j] for j in range(n + 1)]
    
    # dp_after[i][j] will store the number of valid sequences of length i with j unmatched opening brackets
    dp_after = [[0] * (n + 1) for _ in range(2 * n - len_s + 1)]
    dp_after[0][0] = 1
    
    # Fill the dp table for sequences after s
    for i in range(len_s, 2 * n):
        if s[i - len_s] == '(':
            for j in range(n):
                dp_after[i - len_s + 1][j + 1] = (dp_after[i - len_s + 1][j + 1] + dp_after[i - len_s][j]) % MOD
        else:
            for j in range(1, n + 1):
                dp_after[i - len_s + 1][j - 1] = (dp_after[i - len_s + 1][j - 1] + dp_after[i - len_s][j]) % MOD
    
    # Calculate the total number of valid sequences containing s as a substring
    result = 0
    for j in range(n + 1):
        result = (result + dp_before[j] * dp_after[2 * n - len_s][j]) % MOD
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result = count_valid_sequences(n, s)
    print(result)

if __name__ == "__main__":
    main()