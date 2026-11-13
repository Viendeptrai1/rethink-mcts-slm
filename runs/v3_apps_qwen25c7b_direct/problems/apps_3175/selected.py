import sys
from itertools import combinations

def max_polygon_area(segments):
    def shoelace_formula(coords):
        n = len(coords)
        area = 0.5 * abs(sum(x * y - y * x for x, y in zip(coords, coords[1:] + coords[:1])))
        return area

    def is_convex(coords):
        n = len(coords)
        sign = None
        for i in range(n):
            dx1, dy1 = coords[(i + 1) % n][0] - coords[i][0], coords[(i + 1) % n][1] - coords[i][1]
            dx2, dy2 = coords[(i + 2) % n][0] - coords[i][0], coords[(i + 2) % n][1] - coords[i][1]
            cross_product = dx1 * dy2 - dy1 * dx2
            if cross_product != 0:
                if sign is None:
                    sign = cross_product > 0
                elif sign != (cross_product > 0):
                    return False
        return True

    max_area = 0
    for r in range(3, len(segments) + 1):
        for combo in combinations(segments, r):
            coords = [(sum(combo[:i]), sum(combo[i:])) for i in range(r)]
            if is_convex(coords):
                area = shoelace_formula(coords)
                if area > max_area:
                    max_area = area
    return max_area

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    segments = list(map(int, data[1:]))
    result = max_polygon_area(segments)
    print(f"{result:.5f}")