def solve():
    import sys
    input = sys.stdin.read
    MOD = 998244353

    data = input().split()
    N = int(data[0])
    points = [(int(data[i * 2 + 1]), int(data[i * 2 + 2])) for i in range(N)]

    # Sort points by x, then by y
    points.sort()

    # To store the number of subsets that include each point
    count = [0] * N

    # Iterate over each point as the top-right corner of a rectangle
    for i in range(N):
        x_i, y_i = points[i]
        # Initialize the minimum and maximum y-coordinates for the current rectangle
        min_y = y_i
        max_y = y_i
        # Count the number of points that can form a rectangle with points[i] as the top-right corner
        for j in range(i):
            x_j, y_j = points[j]
            # Update the min and max y-coordinates
            min_y = min(min_y, y_j)
            max_y = max(max_y, y_j)
            # Count the number of points that can form a rectangle with points[i] as the top-right corner
            count[i] = (count[i] + 1) % MOD

    # Calculate the sum of f(T) over all non-empty subsets
    total_sum = 0
    for i in range(N):
        total_sum = (total_sum + count[i]) % MOD

    # Print the result
    print(total_sum)