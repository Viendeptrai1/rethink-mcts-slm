import itertools
import math

def is_valid_polygon(sides):
    # Check if the given sides can form a valid polygon using the triangle inequality theorem
    for i in range(len(sides)):
        if sum(sides) - sides[i] <= sides[i]:
            return False
    return True

def polygon_area(sides):
    # Calculate the area of a polygon using Brahmagupta's formula for cyclic quadrilaterals
    # or Heron's formula for triangles
    n = len(sides)
    if n == 3:
        # Triangle
        a, b, c = sides
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))
    elif n == 4:
        # Quadrilateral
        a, b, c, d = sides
        s = (a + b + c + d) / 2
        return math.sqrt((s - a) * (s - b) * (s - c) * (s - d) - a * b * c * d * math.cos(math.pi / 2) ** 2)
    else:
        return 0

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