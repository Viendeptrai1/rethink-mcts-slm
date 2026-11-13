import math

def rectangle_intersection_area(w, h, alpha):
    # Convert angle from degrees to radians
    alpha_rad = math.radians(alpha)
    
    # Calculate the corners of the first rectangle
    corners1 = [
        (-w/2, -h/2),
        (w/2, -h/2),
        (w/2, h/2),
        (-w/2, h/2)
    ]
    
    # Calculate the corners of the second rectangle after rotation
    corners2 = []
    for x, y in corners1:
        x_rot = x * math.cos(alpha_rad) - y * math.sin(alpha_rad)
        y_rot = x * math.sin(alpha_rad) + y * math.cos(alpha_rad)
        corners2.append((x_rot, y_rot))
    
    # Function to find the intersection of two line segments
    def line_intersection(p1, p2, p3, p4):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        
        denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        if denom == 0:
            return None  # Lines are parallel
        
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
        
        if 0 <= ua <= 1 and 0 <= ub <= 1:
            x = x1 + ua * (x2 - x1)
            y = y1 + ua * (y2 - y1)
            return (x, y)
        return None
    
    # Find all intersection points
    intersections = []
    for i in range(4):
        for j in range(4):
            intersection = line_intersection(corners1[i], corners1[(i+1)%4], corners2[j], corners2[(j+1)%4])
            if intersection:
                intersections.append(intersection)
    
    # Remove duplicate points
    intersections = list(set(intersections))
    
    # If there are less than 3 intersection points, rectangles do not intersect
    if len(intersections) < 3:
        return 0.0
    
    # Sort intersection points by polar angle
    center = (0, 0)
    def polar_angle(point):
        return math.atan2(point[1] - center[1], point[0] - center[0])
    
    intersections.sort(key=polar_angle)
    
    # Calculate the area of the polygon formed by intersection points
    area = 0.0
    for i in range(len(intersections)):
        x1, y1 = intersections[i]
        x2, y2 = intersections[(i+1) % len(intersections)]
        area += x1 * y2 - x2 * y1
    
    return abs(area) / 2

# Read input
w, h, alpha = map(int, input().split())

# Calculate and print the result
result = rectangle_intersection_area(w, h, alpha)
print(f"{result:.9f}")