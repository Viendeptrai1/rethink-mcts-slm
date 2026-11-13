import math
import sys

def find_release_point(b, tx, ty):
    def spiral(phi):
        return b * phi, phi

    def polar_to_cartesian(r, theta):
        return r * math.cos(theta), r * math.sin(theta)

    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def intersects_spiral(x1, y1, x2, y2, phi):
        r, theta = spiral(phi)
        px, py = polar_to_cartesian(r, theta)
        return distance(x1, y1, px, py) < 1e-6 or distance(x2, y2, px, py) < 1e-6

    target_distance = math.sqrt(tx**2 + ty**2)
    target_angle = math.atan2(ty, tx)

    left, right = 0, target_distance / b
    while right - left > 1e-6:
        mid = (left + right) / 2
        r, theta = spiral(mid / b)
        x, y = polar_to_cartesian(r, theta)

        if intersects_spiral(0, 0, x, y, mid / b):
            left = mid
        else:
            right = mid

    r, phi = spiral(right / b)
    x, y = polar_to_cartesian(r, phi)

    # Adjust the angle to hit the target
    dx, dy = tx - x, ty - y
    angle = math.atan2(dy, dx)
    distance = math.sqrt(dx**2 + dy**2)
    
    x += distance * math.cos(angle)
    y += distance * math.sin(angle)

    return x, y

if __name__ == "__main__":
    b, tx, ty = map(float, input().split())
    x, y = find_release_point(b, tx, ty)
    print(f"{x:.10f} {y:.10f}")