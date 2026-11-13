def triangle_area(a, b, c):
    # Check if the sides form a valid triangle
    if (a + b > c) and (a + c > b) and (b + c > a):
        # Calculate semi-perimeter
        s = (a + b + c) / 2
        # Calculate area using Heron's formula
        area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
        # Return area rounded to 2 decimal points
        return round(area, 2)
    else:
        return -1