import itertools
import math

def polygon_area(sides):
    if len(sides) == 3:
        # Use Heron's formula for triangles
        a, b, c = sorted(sides)
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))
    else:
        # Use the Shoelace formula for polygons with more than 3 sides
        n = len(sides)
        area = 0
        for i in range(n):
            x1, y1 = 0, 0
            x2, y2 = sides[i], 0
            x3, y3 = sides[(i + 1) % n] * math.cos(math.pi * 2 / n), sides[(i + 1) % n] * math.sin(math.pi * 2 / n)
            area += x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
        return abs(area) / 2

def is_valid_polygon(sides):
    # Check if the sides can form a convex polygon
    n = len(sides)
    if n < 3:
        return False
    sides = sorted(sides)
    for i in range(n):
        if sides[i] >= sides[-1] + sides[-2]:
            return False
    return True

def max_polygon_area(segments):
    max_area = 0
    for r in range(3, len(segments) + 1):
        for combination in itertools.combinations(segments, r):
            if is_valid_polygon(combination):
                area = polygon_area(combination)
                if area > max_area:
                    max_area = area
    return max_area

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    segments = list(map(int, data[1:]))
    print(f"{max_polygon_area(segments):.3f}")