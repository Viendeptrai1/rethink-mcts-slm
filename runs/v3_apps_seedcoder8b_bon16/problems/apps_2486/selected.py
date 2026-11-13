def solve():
    N, K = map(int, input().split())
    a = list(map(int, input().split()))

    # Calculate prefix sums
    prefix_sum = [0] * (N + 1)
    for i in range(N):
        prefix_sum[i + 1] = prefix_sum[i] + a[i]

    unnecessary = 0
    for i in range(N):
        # Check if removing card i makes the set good
        left_sum = prefix_sum[i]
        right_sum = prefix_sum[N] - prefix_sum[i + 1]
        
        if left_sum + right_sum >= K:
            unnecessary += 1

    print(unnecessary)

if __name__ == "__main__":
    solve()