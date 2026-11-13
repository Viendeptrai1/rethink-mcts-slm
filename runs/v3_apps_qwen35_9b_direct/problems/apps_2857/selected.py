import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    points = []
    for _ in range(n):
        x = int(next(iterator))
        y = int(next(iterator))
        points.append((x, y))

    # We need to count triplets (A, B, C) such that:
    # - A and B share the same x-coordinate (vertical leg)
    # - A and C share the same y-coordinate (horizontal leg)
    # - B and C do not share the same x or y coordinate (otherwise it's degenerate or not a right triangle with legs parallel to axes in the standard way)
    # Actually, the condition simplifies: if we pick a point A as the right-angle vertex,
    # we need to choose one point B with the same x as A, and one point C with the same y as A.
    # The triplet {A, B, C} forms a right triangle with legs parallel to axes.
    # Note: The problem asks for the number of ways to choose three points. The set {A, B, C} is unique regardless of order.
    # By iterating over each point as the potential right-angle vertex, we count each valid triangle exactly once.

    # Precompute counts for each x and each y
    x_counts = {}
    y_counts = {}

    for x, y in points:
        x_counts[x] = x_counts.get(x, 0) + 1
        y_counts[y] = y_counts.get(y, 0) + 1

    total_triangles = 0

    for x, y in points:
        # Number of other points with the same x-coordinate
        count_x = x_counts[x] - 1
        # Number of other points with the same y-coordinate
        count_y = y_counts[y] - 1
        
        # If there is at least one point sharing x and at least one sharing y,
        # we can form count_x * count_y triangles where this point is the right-angle vertex.
        if count_x > 0 and count_y > 0:
            total_triangles += count_x * count_y

    print(total_triangles)

if __name__ == '__main__':
    solve()