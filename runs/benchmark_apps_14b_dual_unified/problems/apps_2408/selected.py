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
            if (points[i][0] == points[j][0] and points[i][1] == points[j][1]):
                continue
            lines.add(tuple(sorted((points[i], points[j]))))
    
    intersections = 0
    for (A, B), (C, D) in combinations(lines, 2):
        if intersect(A, B, C, D):
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