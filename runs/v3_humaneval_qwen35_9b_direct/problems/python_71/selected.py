import math

def triangle_area(a, b, c):
    # Check if the sides form a valid triangle
    if (a + b > c) and (a + c > b) and (b + c > a):
        # Use Heron's formula to calculate the area
        s = (a + b + c) / 2  # semi-perimeter
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return round(area, 2)
    else:
        return -1