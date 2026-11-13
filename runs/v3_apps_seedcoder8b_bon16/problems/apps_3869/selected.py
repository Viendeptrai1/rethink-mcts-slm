import math

def area_of_overlap(w, h, alpha):
    # Convert alpha from degrees to radians
    alpha_rad = math.radians(alpha)
    
    # Calculate the rotation matrix for a 2D rotation by angle alpha
    cos_alpha = math.cos(alpha_rad)
    sin_alpha = math.sin(alpha_rad)
    
    # Determine the bounding box of the rotated rectangle
    # The rotated corners of the rectangle
    x1, y1 = w / 2, h / 2
    x2, y2 = -w / 2, h / 2
    x3, y3 = -w / 2, -h / 2
    x4, y4 = w / 2, -h / 2
    
    # Rotate the corners
    rx1, ry1 = x1 * cos_alpha - y1 * sin_alpha, x1 * sin_alpha + y1 * cos_alpha
    rx2, ry2 = x2 * cos_alpha - y2 * sin_alpha, x2 * sin_alpha + y2 * cos_alpha
    rx3, ry3 = x3 * cos_alpha - y3 * sin_alpha, x3 * sin_alpha + y3 * cos_alpha
    rx4, ry4 = x4 * cos_alpha - y4 * sin_alpha, x4 * sin_alpha + y4 * cos_alpha
    
    # Determine the minimum and maximum x and y coordinates for the bounding box
    min_x = min(rx1, rx2, rx3, rx4)
    max_x = max(rx1, rx2, rx3, rx4)
    min_y = min(ry1, ry2, ry3, ry4)
    max_y = max(ry1, ry2, ry3, ry4)
    
    # Calculate the width and height of the bounding box
    bbox_width = max_x - min_x
    bbox_height = max_y - min_y
    
    # Calculate the area of the bounding box
    bbox_area = bbox_width * bbox_height
    
    # Calculate the area of the intersection of the two rectangles
    # The overlap region has an area that is the product of the width and height of the overlapping region
    intersection_width = min(w, bbox_width)
    intersection_height = min(h, bbox_height)
    intersection_area = intersection_width * intersection_height
    
    return intersection_area

# Read input
import sys
input = sys.stdin.read
data = input().strip().split()
w = int(data[0])
h = int(data[1])
alpha = int(data[2])

# Calculate the area of the overlap
result = area_of_overlap(w, h, alpha)

# Print the result with precision
print(f"{result:.9f}")