def right_angle_triangle(a, b, c):
    # Sort the sides to ensure 'c' is the longest side
    sides = sorted([a, b, c])
    # Check the Pythagorean theorem
    return sides[0]**2 + sides[1]**2 == sides[2]**2