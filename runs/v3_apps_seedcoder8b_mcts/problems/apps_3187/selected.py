def find_optimal_intersection(n, citizens, d):
    def total_distance(x, y):
        return sum(abs(x - cx) + abs(y - cy) for cx, cy in citizens)

    def is_possible(x, y):
        return total_distance(x, y) <= d * n

    # Extract x and y coordinates
    x_coords = sorted(cx for cx, cy in citizens)
    y_coords = sorted(cy for cx, cy in citizens)

    # Median points
    median_x = x_coords[n // 2]
    median_y = y_coords[n // 2]

    # Check if the median point is a valid intersection
    if is_possible(median_x, median_y):
        return total_distance(median_x, median_y)

    # Binary search for the smallest possible total distance
    low, high = 0, 2 * 10**9
    best_distance = float('inf')

    while low <= high:
        mid = (low + high) // 2
        possible = False

        # Check all possible intersections within the current mid distance
        for x in range(max(0, median_x - mid), median_x + mid + 1):
            if possible:
                break
            for y in range(max(0, median_y - mid), median_y + mid + 1):
                if is_possible(x, y):
                    best_distance = min(best_distance, total_distance(x, y))
                    possible = True
                    break

        if possible:
            high = mid - 1
        else:
            low = mid + 1

    return best_distance if best_distance != float('inf') else "impossible"

# Read input
n = int(input().strip())
citizens = [tuple(map(int, input().strip().split())) for _ in range(n)]
d = int(input().strip())

# Find and print the result
result = find_optimal_intersection(n, citizens, d)
print(result)