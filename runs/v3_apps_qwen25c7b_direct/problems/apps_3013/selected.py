import math
import sys

def find_release_point(b, tx, ty):
    def spiral_distance(phi):
        r = b * phi
        return r * abs(math.sin(phi)), r * abs(math.cos(phi))

    def target_distance(x, y):
        return (tx - x) ** 2 + (ty - y) ** 2

    def f(phi):
        sx, sy = spiral_distance(phi)
        dx, dy = tx - sx, ty - sy
        return dx * dx + dy * dy

    low, high = 0, 2 * math.pi
    while high - low > 1e-10:
        mid = (low + high) / 2
        if f(mid) < f(low):
            low = mid
        else:
            high = mid

    sx, sy = spiral_distance(low)
    return sx, sy

if __name__ == "__main__":
    b, tx, ty = map(float, sys.stdin.readline().split())
    result = find_release_point(b, tx, ty)
    print(f"{result[0]:.10f} {result[1]:.10f}")