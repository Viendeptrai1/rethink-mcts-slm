def count_ways_to_climb(N, M, broken_steps):
    MOD = 1_000_000_007
    dp = [0] * (N + 1)
    dp[0] = 1  # Base case: one way to be on the ground (step 0)

    broken_set = set(broken_steps)

    for i in range(1, N + 1):
        if i not in broken_set:
            if i - 1 >= 0:
                dp[i] += dp[i - 1]
            if i - 2 >= 0:
                dp[i] += dp[i - 2]
            dp[i] %= MOD

    return dp[N]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    broken_steps = list(map(int, data[2:2 + M]))
    
    result = count_ways_to_climb(N, M, broken_steps)
    print(result)

if __name__ == "__main__":
    main()