MOD = 998244353

def count_remaining_robots(N, robots):
    robots.sort()
    dp = [1] * (N + 1)
    
    for i in range(1, N):
        if robots[i][0] > robots[i - 1][0] + robots[i - 1][1]:
            dp[i] = dp[i - 1]
        else:
            dp[i] = (dp[i - 1] + dp[i - 2]) % MOD
    
    return (dp[N - 1] + dp[N - 2]) % MOD

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    robots = []
    index = 1
    for _ in range(N):
        X = int(data[index])
        D = int(data[index + 1])
        robots.append((X, D))
        index += 2
    
    result = count_remaining_robots(N, robots)
    print(result)