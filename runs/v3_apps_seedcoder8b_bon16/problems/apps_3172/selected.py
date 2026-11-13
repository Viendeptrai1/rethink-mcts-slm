import sys
import math
from itertools import combinations

def max_fruits_on_line(fruits):
    def is_on_line(p1, p2, p3):
        """Check if point p3 is on the line segment p1p2."""
        return abs((p2[1] - p1[1]) * (p3[0] - p1[0]) - (p2[0] - p1[0]) * (p3[1] - p1[1])) < 1e-9

    def distance(p1, p2):
        """Calculate the Euclidean distance between two points."""
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def point_to_line_distance(p, p1, p2):
        """Calculate the distance from point p to the line segment p1p2."""
        if p1 == p2:
            return distance(p, p1)
        # Calculate projection of p onto line p1p2
        x0, y0 = p
        x1, y1 = p1
        x2, y2 = p2
        num = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        den = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        return num / den

    max_count = 1

    for (p1, p2) in combinations(fruits, 2):
        # Count the number of points that are on the line p1p2
        count = 0
        for p in fruits:
            if is_on_line(p1, p2, p):
                count += 1
            else:
                # Check if the point is within the circle (consider the boundary)
                if point_to_line_distance(p, p1, p2) <= 1.0:
                    count += 1
        max_count = max(max_count, count)

    return max_count

def main():
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    n = int(data[0].strip())
    fruits = []
    
    for i in range(1, n + 1):
        x, y = map(float, data[i].strip().split())
        fruits.append((x, y))
    
    result = max_fruits_on_line(fruits)
    print(result)

if __name__ == "__main__":
    main()