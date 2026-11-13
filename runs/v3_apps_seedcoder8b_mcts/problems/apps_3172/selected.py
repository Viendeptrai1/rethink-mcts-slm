import sys
import math
from itertools import combinations

def max_sliced_fruits(n, fruits):
    def is_sliced(p1, p2, fruit):
        # Check if the line p1p2 intersects the circle centered at 'fruit'
        x1, y1 = p1
        x2, y2 = p2
        x, y = fruit
        # Calculate the coefficients of the line equation ax + by + c = 0
        a = y2 - y1
        b = x1 - x2
        c = x2 * y1 - x1 * y2
        # Calculate the distance from the center of the circle to the line
        distance = abs(a * x + b * y + c) / math.sqrt(a**2 + b**2)
        # A fruit is sliced if the distance is less than or equal to the radius
        return distance <= 1.0

    max_slices = 0
    # Check all pairs of points to form a line
    for p1, p2 in combinations(fruits, 2):
        slices = 0
        for fruit in fruits:
            if is_sliced(p1, p2, fruit):
                slices += 1
        max_slices = max(max_slices, slices)
    return max_slices

def main():
    input = sys.stdin.read
    data = input().strip().split('\n')
    n = int(data[0])
    fruits = [tuple(map(float, line.split())) for line in data[1:n+1]]
    result = max_sliced_fruits(n, fruits)
    print(result)

if __name__ == "__main__":
    main()