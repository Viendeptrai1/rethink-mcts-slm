import math
import sys

def main():
    import sys
    import math

    def read_input():
        import sys
        return sys.stdin.read().split()

    data = read_input()
    idx = 0

    n = int(data[idx])
    idx += 1
    omega = float(data[idx])
    idx += 1
    v0 = float(data[idx])
    idx += 1
    theta = float(data[idx])
    idx += 1
    w = float(data[idx])
    idx += 1

    vertices = []
    for _ in range(n):
        x = float(data[idx])
        idx += 1
        y = float(data[idx])
        idx += 1
        vertices.append((x, y))

    g = 9.81
    theta_rad = math.radians(theta)
    vx = v0 * math.cos(theta_rad)
    vy = v0 * math.sin(theta_rad)

    def time_to_wall(x, y, vx, vy):
        if vx == 0:
            return float('inf')
        t = (w - x) / vx
        return t if t >= 0 else float('inf')

    def corner_time(i, vertices, omega, vx, vy, g):
        x, y = vertices[i]
        t = time_to_wall(x, y, vx, vy)
        if t == float('inf'):
            return float('inf'), i
        xf = x + vx * t
        yf = y + vy * t - 0.5 * g * t * t
        angle = omega * t
        cos_angle = math.cos(angle)
        sin_angle = -math.sin(angle)  # Negative because it's clockwise
        xf_rotated = xf * cos_angle - yf * sin_angle
        yf_rotated = xf * sin_angle + yf * cos_angle
        return t, i

    min_t = float('inf')
    min_i = -1
    for i in range(n):
        t, i = corner_time(i, vertices, omega, vx, vy, g)
        if t < min_t:
            min_t = t
            min_i = i

    print(min_i + 1, "{:.6f}".format(min_t))

if __name__ == "__main__":
    main()