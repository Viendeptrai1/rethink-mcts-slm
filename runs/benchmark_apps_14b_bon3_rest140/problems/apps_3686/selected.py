import sys
from collections import defaultdict

def main():
    import sys
    import math
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def slope(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if dx == 0:
            return float('inf')
        g = gcd(dx, dy)
        return (dx // g, dy // g)
    
    def can_hit_all_with_two_shots(points):
        n = len(points)
        if n <= 2:
            return True
        
        slopes = defaultdict(int)
        
        for i in range(n):
            for j in range(i + 1, n):
                s = slope(points[i], points[j])
                slopes[s] += 1
        
        max_slope_count = max(slopes.values())
        
        return max_slope_count >= n - 1
    
    def read_input():
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
        return n, points
    
    n, points = read_input()
    if can_hit_all_with_two_shots(points):
        print("success")
    else:
        print("failure")

if __name__ == "__main__":
    main()