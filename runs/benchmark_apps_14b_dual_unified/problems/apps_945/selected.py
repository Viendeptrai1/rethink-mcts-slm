import sys
from typing import List

def check_self_intersections(n: int, points: List[int]) -> str:
    points.sort()
    active_semi_circles = []
    
    for i in range(1, n):
        x1, x2 = points[i-1], points[i]
        center = (x1 + x2) / 2
        radius = abs(x2 - x1) / 2
        
        for j in range(len(active_semi_circles)):
            c, r = active_semi_circles[j]
            if abs(center - c) < r + radius:
                return "yes"
        
        active_semi_circles.append((center, radius))
    
    return "no"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    points = list(map(int, data[1:]))
    
    result = check_self_intersections(n, points)
    print(result)

if __name__ == "__main__":
    main()