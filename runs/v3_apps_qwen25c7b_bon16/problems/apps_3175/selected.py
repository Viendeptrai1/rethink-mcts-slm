import sys
from itertools import combinations
import math

def calculate_area(points):
    n = len(points)
    if n < 3:
        return 0
    max_area = 0
    for comb in combinations(points, 3):
        x1, y1 = comb[0]
        x2, y2 = comb[1]
        x3, y3 = comb[2]
        area = abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0
        if area > max_area:
            max_area = area
    return max_area

def main():
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    lengths = [int(data[i+1]) for i in range(n)]
    
    # Generate all possible points on a unit circle
    points = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]
    
    # Calculate the maximum area using these points
    max_area = 0
    for comb in combinations(points, n):
        area = calculate_area(comb)
        if area > max_area:
            max_area = area
    
    print(max_area)

if __name__ == "__main__":
    main()