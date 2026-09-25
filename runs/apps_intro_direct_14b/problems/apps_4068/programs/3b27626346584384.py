import sys

MOD = 1_000_000_007

def count_ways(N, M, broken_steps):
    # Initialize a list to store the number of ways to reach each step
    dp = [0] * (N + 1)
    dp[0] = 1  # There's one way to be at the ground (doing nothing)

    # Convert broken steps to a set for O(1) lookups
    broken_set = set(broken_steps)

    # Fill the dp array
    for i in range(1, N + 1):
        if i in broken_set:
            dp[i] = 0
        else:
            dp[i] = (dp[i - 1] + (dp[i - 2] if i > 1 else 0)) % MOD

    return dp[N]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    N = int(data[0])
    M = int(data[1])
    broken_steps = list(map(int, data[2:2 + M]))

    result = count_ways(N, M, broken_steps)
    print(result)

if __name__ == "__main__":
    main()