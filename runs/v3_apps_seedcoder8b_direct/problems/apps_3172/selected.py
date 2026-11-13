import sys
from math import sqrt, isclose

def max_fruits_sliced(n, fruits):
    def distance(p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def is_on_circle(p, center, radius):
        return isclose(distance(p, center), radius, rel_tol=1e-9)

    def line_intersects_circle(p1, p2, center, radius):
        # Check if the line segment from p1 to p2 intersects the circle
        if is_on_circle(p1, center, radius) or is_on_circle(p2, center, radius):
            return True

        # Vector from p1 to p2
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        # Vector from p1 to center
        a, b = center[0] - p1[0], center[1] - p1[1]

        # Coefficients of the quadratic equation at^2 + bt + c = 0
        a_coeff = dx ** 2 + dy ** 2
        b_coeff = 2 * (a * dx + b * dy)
        c_coeff = a ** 2 + b ** 2 - radius ** 2

        # Discriminant of the quadratic equation
        discriminant = b_coeff ** 2 - 4 * a_coeff * c_coeff

        if discriminant < 0:
            return False

        # Calculate the two solutions for t
        sqrt_discriminant = sqrt(discriminant)
        t1 = (-b_coeff + sqrt_discriminant) / (2 * a_coeff)
        t2 = (-b_coeff - sqrt_discriminant) / (2 * a_coeff)

        # Check if the solutions are within the segment [0, 1]
        return (0 <= t1 <= 1) or (0 <= t2 <= 1)

    max_slices = 0

    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = fruits[i], fruits[j]
            center = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            radius = distance(p1, center)

            slices = 0
            for k in range(n):
                if line_intersects_circle(p1, p2, fruits[k], 0):
                    slices += 1

            max_slices = max(max_slices, slices)

    return max_slices

def main():
    input = sys.stdin.read
    data = input().strip().split()
    
    n = int(data[0])
    fruits = []
    index = 1
    for _ in range(n):
        x = float(data[index])
        y = float(data[index + 1])
        fruits.append((x, y))
        index += 2

    result = max_fruits_sliced(n, fruits)
    print(result)

if __name__ == "__main__":
    main()