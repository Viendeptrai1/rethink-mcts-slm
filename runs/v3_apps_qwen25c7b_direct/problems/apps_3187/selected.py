import sys
from typing import List

def min_total_distance(citizens: List[List[int]], d: int) -> str:
    def binary_search(points: List[int], target: int) -> int:
        left, right = 0, len(points) - 1
        while left <= right:
            mid = (left + right) // 2
            if points[mid] == target:
                return mid
            elif points[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return left

    def find_median(points: List[int]) -> int:
        points.sort()
        n = len(points)
        if n % 2 == 1:
            return points[n // 2]
        else:
            return (points[n // 2 - 1] + points[n // 2]) // 2

    def count_within_distance(x: int, y: int) -> int:
        count = 0
        for cx, cy in citizens:
            if abs(cx - x) + abs(cy - y) <= d:
                count += 1
        return count

    xs = [citizen[0] for citizen in citizens]
    ys = [citizen[1] for citizen in citizens]

    median_x = find_median(xs)
    median_y = find_median(ys)

    if count_within_distance(median_x, median_y) >= len(citizens):
        return str(len(citizens))
    
    return "impossible"

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    citizens = []
    index = 1
    for _ in range(n):
        x = int(data[index])
        y = int(data[index + 1])
        citizens.append([x, y])
        index += 2
    
    d = int(data[index])

    result = min_total_distance(citizens, d)
    print(result)