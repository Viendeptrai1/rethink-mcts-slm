import itertools
import math

def is_valid_polygon(sides):
    # Check if the given sides can form a valid polygon using the triangle inequality theorem
    for i in range(len(sides)):
        if sum(sides) - sides[i] <= sides[i]:
            return False
    return True

def polygon_area(sides):
    # Calculate the area of a polygon using Heron's formula
    n = len(sides)
    s = sum(sides) / 2
    area = 0
    for i in range(n):
        j = (i + 1) % n
        k = (i + 2) % n
        area += sides[i] * sides[j] * math.sin(math.acos((sides[i]**2 + sides[j]**2 - sides[k]**2) / (2 * sides[i] * sides[j])))
    return area / 2

def max_polygon_area(segments):
    max_area = 0
    for r in range(3, len(segments) + 1):
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