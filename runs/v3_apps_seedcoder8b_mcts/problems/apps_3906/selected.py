MOD = 10**9 + 7

def count_random_pictures(n, m):
    if n > m:
        n, m = m, n

    # Initialize dp arrays
    dp_prev = [1, 1]  # dp_prev[0] for ending with black, dp_prev[1] for ending with white
    dp_curr = [0, 0]

    for _ in range(1, n):
        dp_curr[0] = dp_prev[1]
        dp_curr[1] = dp_prev[0]
        dp_prev, dp_curr = dp_curr, dp_prev

    result = 1
    for _ in range(m):
        result = (result * (dp_prev[0] + dp_prev[1])) % MOD
        dp_curr[0] = dp_prev[1]
        dp_curr[1] = dp_prev[0]
        dp_prev, dp_curr = dp_curr, dp_prev

    return result

if __name__ == "__main__":
    n, m = map(int, input().split())
    print(count_random_pictures(n, m))