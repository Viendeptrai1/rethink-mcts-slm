import sys
from itertools import combinations

def count_intersections(n, points):
    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def intersect(A, B, C, D):
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    intersections = 0
    for (x1, y1), (x2, y2) in combinations(points, 2):
        for (x3, y3), (x4, y4) in combinations(points, 2):
            if (x1, y1) != (x3, y3) and (x1, y1) != (x4, y4) and (x2, y2) != (x3, y3) and (x2, y2) != (x4, y4):
                if intersect((x1, y1), (x2, y2), (x3, y3), (x4, y4)):
                    intersections += 1

    return intersections

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    points = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]
    
    result = count_intersections(n, points)
    print(result)

if __name__ == "__main__":
    main()