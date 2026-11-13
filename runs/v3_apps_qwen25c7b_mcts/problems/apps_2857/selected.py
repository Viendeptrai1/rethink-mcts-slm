from collections import Counter
import sys

def count_right_triangles(points):
    x_count = Counter(point[0] for point in points)
    y_count = Counter(point[1] for point in points)

    total_triangles = 0

    for point in points:
        x, y = point
        # Count pairs of points with the same x but different y
        total_triangles += (x_count[x] - 1) * (y_count[y])
        # Count pairs of points with the same y but different x
        total_triangles += (y_count[y] - 1) * (x_count[x])

    return total_triangles

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    points = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]
    
    result = count_right_triangles(points)
    print(result)