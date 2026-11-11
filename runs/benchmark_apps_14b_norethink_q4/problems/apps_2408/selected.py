import sys
from itertools import combinations

def ccw(A, B, C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def count_intersections(n, points):
    lines = set()
    for i in range(n):
        for j in range(i + 1, n):
            if (points[i][0] == points[j][0]):
                slope = float('inf')
                intercept = points[i][0]
            else:
                slope = (points[i][1] - points[j][1]) / (points[i][0] - points[j][0])
                intercept = points[i][1] - slope * points[i][0]
            lines.add((slope, intercept))
    
    intersections = 0
    for (slope1, intercept1), (slope2, intercept2) in combinations(lines, 2):
        if slope1 == slope2:
            continue
        for i in range(n):
            for j in range(i + 1, n):
                if (slope1 == float('inf') and slope2 == float('inf')):
                    if intercept1 == intercept2 and points[i][0] == intercept1 and points[j][0] == intercept1:
                        intersections += 1
                elif slope1 == float('inf'):
                    if points[i][0] == intercept1 and intersect(points[i], points[j], (intercept2, intercept2), (intercept2 + 1, intercept2)):
                        intersections += 1
                elif slope2 == float('inf'):
                    if points[i][0] == intercept2 and intersect(points[i], points[j], (intercept1, intercept1), (intercept1 + 1, intercept1)):
                        intersections += 1
                else:
                    if intersect(points[i], points[j], (intercept1, intercept1), (intercept2, intercept2)):
                        intersections += 1
    
    return intersections

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
    
    result = count_intersections(n, points)
    print(result)

if __name__ == "__main__":
    main()