import sys

MOD = 1_000_000_007

def count_ways(N, M, broken_steps):
    # Initialize a list to store the number of ways to reach each step
    dp = [0] * (N + 1)
    dp[0] = 1  # There's one way to be at the ground (doing nothing)

    # Fill the dp array
    for i in range(1, N + 1):
        if i not in broken_steps:
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
    broken_steps = set(map(int, data[2:2+M]))

    result = count_ways(N, M, broken_steps)
    print(result)

if __name__ == "__main__":
    main()