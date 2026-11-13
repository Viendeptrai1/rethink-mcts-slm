def check_self_intersection(points):
    n = len(points)
    for i in range(2, n):
        for j in range(i-2, -1, -1):
            if points[i-1] < points[j+1] < points[i] or points[i-1] > points[j+1] > points[i]:
                return "yes"
    return "no"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
points = list(map(int, data[1:]))

print(check_self_intersection(points))