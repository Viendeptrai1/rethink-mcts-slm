def min_total_distance(citizens, d):
    def binary_search(points, target):
        left, right = 0, len(points) - 1
        while left <= right:
            mid = (left + right) // 2
            if abs(points[mid] - points[len(points)//2]) > target:
                left += 1
            else:
                right -= 1
        return len(points) // 2

    x_points = sorted([citizen[0] for citizen in citizens])
    y_points = sorted([citizen[1] for citizen in citizens])

    best_distance = float('inf')
    for candidate_x in range(x_points[binary_search(x_points, d)], x_points[min(binary_search(x_points, d) + 1, len(x_points))]):
        for candidate_y in range(y_points[binary_search(y_points, d)], y_points[min(binary_search(y_points, d) + 1, len(y_points))]):
            total_distance = sum(abs(candidate_x - x) + abs(candidate_y - y) for x, y in citizens)
            if total_distance < best_distance:
                best_distance = total_distance

    if best_distance == float('inf'):
        return "impossible"
    return best_distance

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
citizens = [(int(data[i*2+1]), int(data[i*2+2])) for i in range(n)]
d = int(data[n*2+1])

result = min_total_distance(citizens, d)
print(result)