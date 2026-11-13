import math

def triangle_area(a, b, c):
    # Check if sides form a valid triangle
    if (a + b > c) and (a + c > b) and (b + c > a):
        # Calculate semi-perimeter
        s = (a + b + c) / 2
        # Calculate area using Heron's formula
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return round(area, 2)
    else:
        return -1