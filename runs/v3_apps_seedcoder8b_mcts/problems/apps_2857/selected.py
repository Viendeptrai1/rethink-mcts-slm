def count_right_triangles(N, points):
    from collections import defaultdict

    # Create dictionaries to count points on the same x and y lines
    x_count = defaultdict(int)
    y_count = defaultdict(int)

    # Count occurrences of each x and y coordinate
    for x, y in points:
        x_count[x] += 1
        y_count[y] += 1

    # Initialize the triangle count
    triangle_count = 0

    # Iterate over each point
    for x, y in points:
        # Calculate potential triangles with this point as a vertex
        # The triangle must have one leg parallel to the x-axis and the other parallel to the y-axis
        # The third point will be at (x, y2) or (x2, y) where y2 and x2 are other y and x coordinates respectively
        triangle_count += (x_count[x] - 1) * (y_count[y] - 1)

    return triangle_count

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
N = int(data[0])
points = [(int(data[i]), int(data[i + 1])) for i in range(1, len(data), 2)]

# Calculate and print the number of right triangles
print(count_right_triangles(N, points))