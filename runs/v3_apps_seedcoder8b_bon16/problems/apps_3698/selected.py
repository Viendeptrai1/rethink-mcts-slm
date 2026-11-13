MOD = 10**9 + 7

def count_special_numbers(n, k):
    binary = bin(n)[2:]
    length = len(binary)
    dp = [[[0] * (k + 1) for _ in range(2)] for _ in range(length + 1)]
    dp[0][0][0] = 1

    for i in range(1, length + 1):
        for j in range(2):
            for l in range(k + 1):
                if j == 0 and binary[i-1] == '1':
                    dp[i][1][l] = (dp[i][1][l] + dp[i-1][0][l]) % MOD
                    if l > 0:
                        dp[i][0][l-1] = (dp[i][0][l-1] + dp[i-1][0][l]) % MOD
                else:
                    dp[i][j][l] = (dp[i][j][l] + dp[i-1][j][l]) % MOD
                    if l > 0:
                        dp[i][j][l-1] = (dp[i][j][l-1] + dp[i-1][j][l]) % MOD

    result = sum(dp[length][j][k] for j in range(2)) % MOD
    return result

# Read input
n = int(input().strip(), 2)
k = int(input().strip())

# Calculate and print result
print(count_special_numbers(n, k))