def count_right_triangles(N, points):
    from collections import defaultdict

    # We'll use dictionaries to count occurrences of x and y coordinates
    x_count = defaultdict(int)
    y_count = defaultdict(int)
    
    for x, y in points:
        x_count[x] += 1
        y_count[y] += 1

    triangle_count = 0
    
    # Iterate through each point as the potential right angle vertex
    for x, y in points:
        # Calculate the number of triangles that can be formed
        # with this point as the right angle
        # By multiplying x occurrences and y occurrences
        triangle_count += (x_count[x] - 1) * (y_count[y] - 1)
    
    return triangle_count

# Reading input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
points = []
index = 1
for _ in range(N):
    x = int(data[index])
    y = int(data[index + 1])
    points.append((x, y))
    index += 2

# Calculate and print the number of right triangles
print(count_right_triangles(N, points))