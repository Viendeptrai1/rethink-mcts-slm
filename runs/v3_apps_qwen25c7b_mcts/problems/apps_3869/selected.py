import math

def calculate_intersection_area(w, h, alpha):
    # Convert angle to radians
    alpha_rad = math.radians(alpha)
    
    # Vertices of the first rectangle
    rect1_vertices = [
        (-w/2, -h/2), (-w/2, h/2), (w/2, h/2), (w/2, -h/2)
    ]
    
    # Rotate vertices of the first rectangle by alpha
    rotated_rect1_vertices = [(x * math.cos(alpha_rad) - y * math.sin(alpha_rad),
                               x * math.sin(alpha_rad) + y * math.cos(alpha_rad)) for x, y in rect1_vertices]
    
    # Function to check if point is inside a polygon
    def is_point_in_polygon(point, polygon):
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
    
    # Vertices of the second rectangle (original rectangle)
    rect2_vertices = [
        (-w/2, -h/2), (-w/2, h/2), (w/2, h/2), (w/2, -h/2)
    ]
    
    # Find intersection points
    intersection_points = []
    for v1, v2 in zip(rect1_vertices, rect1_vertices[1:] + rect1_vertices[:1]):
        for v3, v4 in zip(rect2_vertices, rect2_vertices[1:] + rect2_vertices[:1]):
            x1, y1 = v1
            x2, y2 = v2
            x3, y3 = v3
            x4, y4 = v4
            
            denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denominator == 0:
                continue
            
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
            
            if 0 <= t <= 1 and 0 <= u <= 1:
                intersection_points.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
    
    # Remove duplicate points
    intersection_points = list(set(intersection_points))
    
    # If there are less than 3 intersection points, the intersection is empty
    if len(intersection_points) < 3:
        return 0
    
    # Calculate the area using the shoelace formula
    area = 0
    n = len(intersection_points)
    for i in range(n):
        j = (i + 1) % n
        area += intersection_points[i][0] * intersection_points[j][1]
        area -= intersection_points[j][0] * intersection_points[i][1]
    area = abs(area) / 2.0
    
    return area

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    w = int(data[0])
    h = int(data[1])
    alpha = int(data[2])
    result = calculate_intersection_area(w, h, alpha)
    print(result)