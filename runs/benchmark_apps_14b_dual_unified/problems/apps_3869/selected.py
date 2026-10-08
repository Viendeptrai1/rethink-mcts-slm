import math
from typing import List, Tuple

def get_intersection_points(w: float, h: float, alpha: float) -> List[Tuple[float, float]]:
    alpha_rad = math.radians(alpha)
    cos_alpha = math.cos(alpha_rad)
    sin_alpha = math.sin(alpha_rad)
    
    # Define the vertices of the original rectangle
    vertices = [
        (w / 2, h / 2),
        (w / 2, -h / 2),
        (-w / 2, -h / 2),
        (-w / 2, h / 2)
    ]
    
    # Rotate the vertices
    rotated_vertices = [(x * cos_alpha - y * sin_alpha, x * sin_alpha + y * cos_alpha) for x, y in vertices]
    
    # Define the edges of the original rectangle
    edges = [
        (vertices[0], vertices[1]),
        (vertices[1], vertices[2]),
        (vertices[2], vertices[3]),
        (vertices[3], vertices[0])
    ]
    
    # Define the edges of the rotated rectangle
    rotated_edges = [
        (rotated_vertices[0], rotated_vertices[1]),
        (rotated_vertices[1], rotated_vertices[2]),
        (rotated_vertices[2], rotated_vertices[3]),
        (rotated_vertices[3], rotated_vertices[0])
    ]
    
    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
    
    def intersect(A, B, C, D):
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
    
    def line_intersection(A, B, C, D):
        t = ((A[0] - C[0]) * (D[1] - C[1]) - (A[1] - C[1]) * (D[0] - C[0])) / ((A[0] - B[0]) * (D[1] - C[1]) - (A[1] - B[1]) * (D[0] - C[0]))
        u = ((A[0] - C[0]) * (B[1] - A[1]) - (A[1] - C[1]) * (B[0] - A[0])) / ((A[0] - B[0]) * (D[1] - C[1]) - (A[1] - B[1]) * (D[0] - C[0]))
        if 0 <= t <= 1 and 0 <= u <= 1:
            return (A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1]))
        return None
    
    intersection_points = []
    for edge1 in edges:
        for edge2 in rotated_edges:
            point = line_intersection(edge1[0], edge1[1], edge2[0], edge2[1])
            if point:
                intersection_points.append(point)
    
    # Remove duplicate points
    unique_points = list(set(intersection_points))
    
    # Sort points by angle
    def angle(point):
        return math.atan2(point[1], point[0])
    
    unique_points.sort(key=angle)
    
    return unique_points

def polygon_area(points: List[Tuple[float, float]]) -> float:
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    area = abs(area) / 2.0
    return area

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    w = float(data[0])
    h = float(data[1])
    alpha = float(data[2])
    
    intersection_points = get_intersection_points(w, h, alpha)
    area = polygon_area(intersection_points)
    print(f"{area:.9f}")

if __name__ == "__main__":
    main()