import math

def calculate_area(w, h, alpha):
    # Convert angle from degrees to radians
    alpha_rad = math.radians(alpha)
    
    # Vertices of the first rectangle (centered at origin)
    vertices1 = [
        (w/2, h/2),
        (-w/2, h/2),
        (-w/2, -h/2),
        (w/2, -h/2)
    ]
    
    # Rotate the vertices of the first rectangle
    vertices2 = []
    for x, y in vertices1:
        new_x = x * math.cos(alpha_rad) - y * math.sin(alpha_rad)
        new_y = x * math.sin(alpha_rad) + y * math.cos(alpha_rad)
        vertices2.append((new_x, new_y))
    
    # Function to check if a point is inside a rectangle
    def is_point_in_rectangle(point, rect_vertices):
        x, y = point
        x1, y1 = rect_vertices[0]
        x2, y2 = rect_vertices[1]
        x3, y3 = rect_vertices[2]
        x4, y4 = rect_vertices[3]
        
        # Check if the point is inside the bounding box
        if not (min(x1, x2, x3, x4) <= x <= max(x1, x2, x3, x4) and
                min(y1, y2, y3, y4) <= y <= max(y1, y2, y3, y4)):
            return False
        
        # Check if the point is on the same side of all edges
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        d1 = sign((x, y), vertices1[0], vertices1[1]) * sign((x, y), vertices1[1], vertices1[2])
        d2 = sign((x, y), vertices1[1], vertices1[2]) * sign((x, y), vertices1[2], vertices1[3])
        d3 = sign((x, y), vertices1[2], vertices1[3]) * sign((x, y), vertices1[3], vertices1[0])
        d4 = sign((x, y), vertices1[3], vertices1[0]) * sign((x, y), vertices1[0], vertices1[1])
        
        return d1 >= 0 and d2 >= 0 and d3 >= 0 and d4 >= 0
    
    # Find the intersection points
    intersection_points = []
    for i in range(4):
        for j in range(4):
            x1, y1 = vertices1[i]
            x2, y2 = vertices1[(i + 1) % 4]
            x3, y3 = vertices2[j]
            x4, y4 = vertices2[(j + 1) % 4]
            
            # Check if lines are parallel
            if (x2 - x1) * (y4 - y3) == (y2 - y1) * (x4 - x3):
                continue
            
            # Calculate intersection point
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
            u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
            
            if 0 <= t <= 1 and 0 <= u <= 1:
                intersection_points.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
    
    # Add the vertices that are inside the other rectangle
    for vertex in vertices1:
        if is_point_in_rectangle(vertex, vertices2):
            intersection_points.append(vertex)
    for vertex in vertices2:
        if is_point_in_rectangle(vertex, vertices1):
            intersection_points.append(vertex)
    
    # Remove duplicate points
    intersection_points = list(set(intersection_points))
    
    # Sort points to form a polygon
    def angle_with_x_axis(point):
        x, y = point
        return math.atan2(y, x)
    
    intersection_points.sort(key=angle_with_x_axis)
    
    # Calculate the area of the polygon using the shoelace formula
    n = len(intersection_points)
    area = 0
    for i in range(n):
        x1, y1 = intersection_points[i]
        x2, y2 = intersection_points[(i + 1) % n]
        area += x1 * y2 - y1 * x2
    
    return abs(area) / 2

# Read input
import sys
input = sys.stdin.read
data = input().split()
w = int(data[0])
h = int(data[1])
alpha = int(data[2])

# Calculate and print the area
area = calculate_area(w, h, alpha)
print(f"{area:.9f}")