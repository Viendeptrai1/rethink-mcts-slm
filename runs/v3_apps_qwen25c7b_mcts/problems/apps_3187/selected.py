import sys
from typing import List

def min_total_distance(n: int, houses: List[List[int]], d: int) -> str:
    def is_valid_median(x: int, y: int) -> bool:
        return all(abs(house[0] - x) + abs(house[1] - y) <= d for house in houses)

    xs = sorted([house[0] for house in houses])
    ys = sorted([house[1] for house in houses])

    if len(xs) % 2 == 1:
        median_x = xs[len(xs) // 2]
    else:
        median_x = (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) // 2

    if len(ys) % 2 == 1:
        median_y = ys[len(ys) // 2]
    else:
        median_y = (ys[len(ys) // 2 - 1] + ys[len(ys) // 2]) // 2

    if is_valid_median(median_x, median_y):
        return str(sum(abs(house[0] - median_x) + abs(house[1] - median_y) for house in houses))
    else:
        return "impossible"

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    houses = [[int(data[2 * i + 1]), int(data[2 * i + 2])] for i in range(n)]
    d = int(data[2 * n + 1])
    
    result = min_total_distance(n, houses, d)
    print(result)