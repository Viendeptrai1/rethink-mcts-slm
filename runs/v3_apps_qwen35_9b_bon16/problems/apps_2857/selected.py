import sys
from collections import defaultdict

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

    # We need to count triplets (A, B, C) such that they form a right triangle
    # with legs parallel to the axes.
    # This means one vertex is the "corner" (let's call it P), and the other two (Q and R)
    # share the same x-coordinate as P and the same y-coordinate as P respectively.
    # Specifically:
    # P = (x, y)
    # Q = (x, y_q) where y_q != y
    # R = (x_r, y) where x_r != x
    # The triangle PQR has the right angle at P.

    # Approach:
    # For each point P=(x, y), we need to know:
    # 1. How many other points have the same x-coordinate (vertical neighbors)?
    # 2. How many other points have the same y-coordinate (horizontal neighbors)?
    #
    # If a point P has 'v' other points with the same x and 'h' other points with the same y,
    # then the number of right triangles with the right angle at P is v * h.
    #
    # Total triangles = sum(v * h) for all points P.

    # Count points by x-coordinate
    x_counts = defaultdict(int)
    for x, y in points:
        x_counts[x] += 1

    # Count points by y-coordinate
    y_counts = defaultdict(int)
    for x, y in points:
        y_counts[y] += 1

    total_triangles = 0

    for x, y in points:
        # Number of points with same x (excluding self)
        v = x_counts[x] - 1
        # Number of points with same y (excluding self)
        h = y_counts[y] - 1
        
        total_triangles += v * h

    print(total_triangles)

if __name__ == '__main__':
    solve()