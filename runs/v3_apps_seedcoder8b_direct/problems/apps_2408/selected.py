from itertools import combinations
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

    intersecting_pairs = 0
    for (p1, p2) in combinations(points, 2):
        m1 = slope(p1, p2)
        for (p3, p4) in combinations(points, 2):
            if p3 == p1 or p3 == p2 or p4 == p1 or p4 == p2:
                continue
            m2 = slope(p3, p4)
            if m1 == m2:
                intersecting_pairs += 1

    return intersecting_pairs

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    points = [(int(data[i]), int(data[i+1])) for i in range(1, len(data), 2)]
    
    result = count_intersecting_wires(n, points)
    print(result)