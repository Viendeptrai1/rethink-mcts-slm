import math

def triangle_area(a, b, c):
    """
    Calculate the area of a triangle given its side lengths.
    
    Args:
    a (float): Length of the first side.
    b (float): Length of the second side.
    c (float): Length of the third side.
    
    Returns:
    float: The area of the triangle rounded to 2 decimal points if the sides form a valid triangle, otherwise -1.
    """
    if a + b <= c or a + c <= b or b + c <= a:
        return -1
    
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return round(area, 2)