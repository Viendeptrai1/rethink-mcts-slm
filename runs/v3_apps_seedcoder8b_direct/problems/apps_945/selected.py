def has_self_intersections(n, points):
    # Sort the points based on their x-coordinates
    points.sort()

    # Function to check if two semi-circles intersect
    def semi_circles_intersect(x1, x2, x3, x4):
        # Calculate the midpoints and radii
        mid1, mid2 = (x1 + x2) / 2, (x3 + x4) / 2
        r1, r2 = abs(x2 - x1) / 2, abs(x4 - x3) / 2

        # Check if the semi-circles intersect
        return abs(mid1 - mid2) <= r1 + r2

    # Check for intersections between consecutive semi-circles
    for i in range(n - 3):
        if semi_circles_intersect(points[i], points[i + 1], points[i + 1], points[i + 2]):
            return "yes"

    return "no"

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
points = list(map(int, data[1:n+1]))

# Output the result
print(has_self_intersections(n, points))