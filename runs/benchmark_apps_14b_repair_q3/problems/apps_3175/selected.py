import itertools
import math

def is_valid_polygon(sides):
    # Check if the given sides can form a valid polygon using the triangle inequality theorem
    for i in range(len(sides)):
        if sides[i] >= sum(sides) - sides[i]:
            return False
    return True

def polygon_area(sides):
    # Calculate the area using Brahmagupta's formula for cyclic quadrilaterals
    # This is a simplified version for polygons with up to 4 sides
    n = len(sides)
    if n == 3:
        # Heron's formula for triangles
        s = sum(sides) / 2
        area = math.sqrt(s * (s - sides[0]) * (s - sides[1]) * (s - sides[2]))
    elif n == 4:
        # Brahmagupta's formula for cyclic quadrilaterals
        s = sum(sides) / 2
        area = math.sqrt((s - sides[0]) * (s - sides[1]) * (s - sides[2]) * (s - sides[3]))
    else:
        # For polygons with more than 4 sides, we need a more complex approach
        # Here we use a simple approximation by sorting and forming a convex hull
        sides = sorted(sides)
        area = 0
        for i in range(n):
            x1, y1 = 0, sides[i]
            x2, y2 = sides[(i + 1) % n], 0
            area += x1 * y2 - y1 * x2
        return abs(area) / 2
    return area

def max_polygon_area(segments):
    max_area = 0
    n = len(segments)
    for r in range(3, n + 1):
        for combination in itertools.combinations(segments, r):
            if is_valid_polygon(combination):
                area = polygon_area(combination)
                if area > max_area:
                    max_area = area
    return max_area

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    segments = list(map(int, data[1:]))
    result = max_polygon_area(segments)
    print(f"{result:.3f}")

if __name__ == "__main__":
    main()