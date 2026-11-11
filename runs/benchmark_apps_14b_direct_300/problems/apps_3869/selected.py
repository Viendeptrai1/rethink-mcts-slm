import math

def intersecting_area(w, h, alpha):
    # Convert angle from degrees to radians
    alpha = math.radians(alpha)
    
    # Calculate the half-widths and half-heights
    hw1, hh1 = w / 2, h / 2
    hw2, hh2 = hh1, hw1
    
    # Calculate the intersection area
    if alpha == 0 or alpha == 90 or alpha == 180:
        return min(w, hw2) * min(h, hh2)
    
    # Calculate the intersection points
    x1 = abs(hw1 * math.cos(alpha) + hh1 * math.sin(alpha))
    y1 = abs(hw1 * math.sin(alpha) - hh1 * math.cos(alpha))
    x2 = abs(hw2 * math.cos(alpha) + hh2 * math.sin(alpha))
    y2 = abs(hw2 * math.sin(alpha) - hh2 * math.cos(alpha))
    
    # Calculate the intersection area
    area = 2 * min(x1, x2) * min(y1, y2)
    return area

# Read input
w, h, alpha = map(int, input().split())

# Calculate and print the result
print(intersecting_area(w, h, alpha))