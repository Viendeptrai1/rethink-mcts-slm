import math
import sys

def find_release_point(b, tx, ty):
    def spiral_r(phi):
        return b * phi

    def spiral_x(phi):
        return spiral_r(phi) * math.cos(phi)

    def spiral_y(phi):
        return spiral_r(phi) * math.sin(phi)

    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def intersects_spiral(x, y, phi_start, phi_end):
        for phi in [phi_start, phi_end]:
            if distance(x, y, spiral_x(phi), spiral_y(phi)) < 1e-3:
                return True
        return False

    # Binary search for the correct phi
    left, right = 0, 2 * math.pi
    while right - left > 1e-7:
        mid = (left + right) / 2
        x, y = spiral_x(mid), spiral_y(mid)
        if distance(x, y, tx, ty) < spiral_r(mid):
            right = mid
        else:
            left = mid

    # Find the phi where the distance to the target is minimal
    phi_release = (left + right) / 2
    x_release, y_release = spiral_x(phi_release), spiral_y(phi_release)

    # Ensure the release point does not intersect the spiral
    while intersects_spiral(x_release, y_release, phi_release - 0.1, phi_release + 0.1):
        phi_release += 0.1
        x_release, y_release = spiral_x(phi_release), spiral_y(phi_release)

    return x_release, y_release

def main():
    input_data = sys.stdin.read().strip()
    b, tx, ty = map(float, input_data.split())
    x_release, y_release = find_release_point(b, tx, ty)
    print(f"{x_release:.10f} {y_release:.10f}")

if __name__ == "__main__":
    main()