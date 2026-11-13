def has_self_intersection(n, points):
    points.sort()
    for i in range(2, n):
        if points[i-2] < points[i]:
            return "yes"
    return "no"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
points = list(map(int, data[1:]))

print(has_self_intersection(n, points))