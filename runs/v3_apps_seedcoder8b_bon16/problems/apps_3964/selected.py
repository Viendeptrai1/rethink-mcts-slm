def count_good_plans(n, m, b, mod, bugs_per_programmer):
    # dp[i][j] will be the number of ways to distribute j lines among i programmers
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    # Fill the dp array
    for i in range(1, n + 1):
        for j in range(m + 1):
            for k in range(j + 1):
                dp[i][j] = (dp[i][j] + dp[i - 1][j - k]) % mod

    # Now we need to count the good plans
    # good_dp[i][j][k] will be the number of ways to distribute j lines among i programmers with total bugs <= k
    good_dp = [[[0] * (b + 1) for _ in range(m + 1)] for _ in range(n + 1)]
    good_dp[0][0][0] = 1
    
    # Fill the good_dp array
    for i in range(1, n + 1):
        for j in range(m + 1):
            for k in range(b + 1):
                for x in range(j + 1):
                    if k >= x * bugs_per_programmer[i - 1]:
                        good_dp[i][j][k] = (good_dp[i][j][k] + good_dp[i - 1][j - x][k - x * bugs_per_programmer[i - 1]]) % mod

    # Sum up all good plans for exactly m lines and total bugs <= b
    result = sum(good_dp[n][m][k] for k in range(b + 1)) % mod
    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    b = int(data[2])
    mod = int(data[3])
    bugs_per_programmer = list(map(int, data[4:4 + n]))
    
    print(count_good_plans(n, m, b, mod, bugs_per_programmer))