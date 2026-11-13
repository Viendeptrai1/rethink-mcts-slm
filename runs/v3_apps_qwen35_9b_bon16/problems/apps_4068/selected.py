import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    N = int(next(iterator))
    M = int(next(iterator))

    broken = set()
    for _ in range(M):
        broken.add(int(next(iterator)))

    MOD = 1_000_000_007

    dp = [0] * (N + 1)
    dp[0] = 1

    for i in range(1, N + 1):
        if i in broken:
            dp[i] = 0
            continue

        ways = 0
        if i - 1 >= 0:
            ways = (ways + dp[i - 1]) % MOD
        if i - 2 >= 0:
            ways = (ways + dp[i - 2]) % MOD
        dp[i] = ways

    print(dp[N])

if __name__ == "__main__":
    solve()