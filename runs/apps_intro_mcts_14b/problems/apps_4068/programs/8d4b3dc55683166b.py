import sys

MOD = 1_000_000_007

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    if M == 0:
        # If there are no broken steps, the number of ways is simply the Fibonacci sequence
        dp = [0] * (N + 1)
        dp[0] = 1
        dp[1] = 1
        for i in range(2, N + 1):
            dp[i] = (dp[i - 1] + dp[i - 2]) % MOD
        print(dp[N])
        return
    
    broken_steps = set(map(int, data[2:2 + M]))
    
    dp = [0] * (N + 1)
    dp[0] = 1
    
    for i in range(1, N + 1):
        if i in broken_steps:
            dp[i] = 0
        else:
            dp[i] = dp[i - 1]
            if i > 1:
                dp[i] = (dp[i] + dp[i - 2]) % MOD
    
    print(dp[N])

if __name__ == "__main__":
    main()