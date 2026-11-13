from itertools import combinations
from collections import defaultdict
from math import gcd

def count_intersecting_wires(n, points):
    def slope(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if dx == 0:
            return ('inf', 0)
        if dy == 0:
            return (0, 'inf')
        g = gcd(dx, dy)
        return (dy // g, dx // g)

    lines = defaultdict(int)
    for (p1, p2) in combinations(points, 2):
        sl = slope(p1, p2)
        lines[sl] += 1

    total_intersections = 0
    for count in lines.values():
        total_intersections += count * (count - 1) // 2

    return total_intersections

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    points = []
    index = 1
    for _ in range(n):
        x = int(data[index])
        y = int(data[index + 1])
        points.append((x, y))
        index += 2
    
    result = count_intersecting_wires(n, points)
    print(result)

if __name__ == "__main__":
    main()