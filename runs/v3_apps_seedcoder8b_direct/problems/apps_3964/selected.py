def count_good_plans(n, m, b, mod, bugs_per_programmer):
    # dp[i][j] will store the number of ways to distribute j lines among i programmers
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 1  # Base case: 1 way to distribute 0 lines among 0 programmers

    for i in range(1, n + 1):
        for j in range(m + 1):
            for k in range(j + 1):
                dp[i][j] = (dp[i][j] + dp[i - 1][j - k]) % mod

    # Now calculate the number of good plans
    good_plans = 0

    for j in range(m + 1):
        total_bugs = sum(bugs_per_programmer[i] * k for i, k in enumerate(divmod(j, n)))
        if total_bugs <= b:
            good_plans = (good_plans + dp[n][j]) % mod

    return good_plans

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    b = int(data[2])
    mod = int(data[3])
    bugs_per_programmer = list(map(int, data[4:4 + n]))
    
    result = count_good_plans(n, m, b, mod, bugs_per_programmer)
    print(result)