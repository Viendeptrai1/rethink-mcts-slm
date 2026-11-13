import math
import sys

def find_release_point(b, tx, ty):
    def spiral_r(phi):
        return b * phi

    def spiral_x(phi):
        return spiral_r(phi) * math.cos(phi)

    def spiral_y(phi):
        return spiral_r(phi) * math.sin(phi)

    def distance_to_spiral(x, y):
        # Calculate the distance from a point (x, y) to the closest point on the spiral
        def distance(phi):
            px, py = spiral_x(phi), spiral_y(phi)
            return math.sqrt((px - x) ** 2 + (py - y) ** 2)

        # Use a simple numerical method to find the closest point on the spiral
        phi_min = 0
        phi_max = 2 * math.pi
        tolerance = 1e-7
        while phi_max - phi_min > tolerance:
            mid = (phi_min + phi_max) / 2
            if distance(mid - tolerance) < distance(mid + tolerance):
                phi_max = mid
            else:
                phi_min = mid
        return distance((phi_min + phi_max) / 2)

    # Binary search for the angle where the avatar should detach
    phi_min = 0
    phi_max = 2 * math.pi
    tolerance = 1e-7
    while phi_max - phi_min > tolerance:
        mid = (phi_min + phi_max) / 2
        avatar_x, avatar_y = spiral_x(mid), spiral_y(mid)
        if distance_to_spiral(avatar_x, avatar_y) < distance_to_spiral(tx, ty):
            phi_max = mid
        else:
            phi_min = mid

    # Calculate the release point
    release_phi = (phi_min + phi_max) / 2
    release_x, release_y = spiral_x(release_phi), spiral_y(release_phi)
    return release_x, release_y

def main():
    input_data = sys.stdin.read().strip()
    b, tx, ty = map(float, input_data.split())
    release_x, release_y = find_release_point(b, tx, ty)
    print(f"{release_x:.10f} {release_y:.10f}")

if __name__ == "__main__":
    main()