def solve():
    import sys
    input = sys.stdin.read
    MOD = 998244353

    data = input().split()
    N = int(data[0])
    points = [(int(data[i * 2 + 1]), int(data[i * 2 + 2])) for i in range(N)]

    # Sort points by x, then by y
    points.sort()

    # Precompute powers of 2 up to N
    power_of_2 = [1] * (N + 1)
    for i in range(1, N + 1):
        power_of_2[i] = (power_of_2[i - 1] * 2) % MOD

    # Calculate the sum of f(T) for all non-empty subsets
    total_sum = 0
    for i in range(N):
        for j in range(i, N):
            # For each pair of points (i, j), calculate the number of subsets
            # that include all points between i and j in both x and y
            total_sum += power_of_2[j - i]
            total_sum %= MOD

    print(total_sum)