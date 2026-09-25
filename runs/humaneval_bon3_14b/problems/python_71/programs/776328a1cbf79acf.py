import math

def triangle_area(a, b, c):
    # Check if the sides form a valid triangle
    if a + b <= c or a + c <= b or b + c <= a:
        return -1
    
    # Calculate the semi-perimeter
    s = (a + b + c) / 2
    
    # Calculate the area using Heron's formula
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    # Round the area to 2 decimal points
    return round(area, 2)

# Example usage:
# print(triangle_area(3, 4, 5))  # Output: 6.00
# print(triangle_area(1, 2, 10)) # Output: -1