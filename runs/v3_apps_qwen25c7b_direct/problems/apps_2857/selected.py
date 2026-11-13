from collections import defaultdict

def count_right_triangles(N, points):
    x_count = defaultdict(int)
    y_count = defaultdict(int)
    
    for x, y in points:
        x_count[x] += 1
        y_count[y] += 1
    
    total_triangles = 0
    
    for x, y in points:
        total_triangles += (x_count[x] - 1) * (y_count[y] - 1)
    
    return total_triangles

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
points = [(int(data[i*2+1]), int(data[i*2+2])) for i in range(N)]

print(count_right_triangles(N, points))