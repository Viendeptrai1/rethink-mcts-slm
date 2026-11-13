def max_original_length(p):
    n = len(p)
    dp = [0] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        for j in range(i):
            if p[j] != '0':  # Ensure no leading zeros
                if j == 0 or p[j-1] == '0':
                    dp[i] = max(dp[i], dp[j] + 1)
                else:
                    v = int(p[j:i])
                    if v > int(p[j-1:i-1]):
                        dp[i] = max(dp[i], dp[j-1] + 1)

    return dp[n]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(max_original_length(input))