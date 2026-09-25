def right_angle_triangle(a, b, c):
    # Sort the sides to ensure the largest side is last
    sides = sorted([a, b, c])
    # Check the Pythagorean theorem: a^2 + b^2 = c^2
    return sides[0]**2 + sides[1]**2 == sides[2]**2