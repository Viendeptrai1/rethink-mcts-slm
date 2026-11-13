def find_square_vertices(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    x3 = x2 - dy
    y3 = y2 + dx
    x4 = x1 - dy
    y4 = y1 + dx
    return x3, y3, x4, y4

# Read input
import sys
input = sys.stdin.read
data = list(map(int, input().split()))

# Extract coordinates
x1, y1, x2, y2 = data

# Find the other two vertices
x3, y3, x4, y4 = find_square_vertices(x1, y1, x2, y2)

# Print the result
print(f"{x3} {y3} {x4} {y4}")