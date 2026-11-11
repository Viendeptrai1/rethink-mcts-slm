import math
import sys

def main():
    import sys
    import math

    def read_input():
        import sys
        return sys.stdin.read().split()

    data = read_input()
    index = 0

    n = int(data[index])
    index += 1
    omega = float(data[index])
    index += 1
    v0 = float(data[index])
    index += 1
    theta = float(data[index])
    index += 1
    w = float(data[index])
    index += 1

    vertices = []
    for _ in range(n):
        x = float(data[index])
        index += 1
        y = float(data[index])
        index += 1
        vertices.append((x, y))

    def calculate_time_to_wall(x0, y0, vx, vy, w):
        if vx == 0:
            return float('inf')
        t = (w - x0) / vx
        return t if t >= 0 else float('inf')

    def calculate_vertex_position(x0, y0, vx, vy, omega, t):
        x = x0 + vx * t
        y = y0 + vy * t - 0.5 * 9.81 * t**2
        angle = omega * t
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        return (x * cos_angle - y * sin_angle, x * sin_angle + y * cos_angle)

    theta_rad = math.radians(theta)
    vx = v0 * math.cos(theta_rad)
    vy = v0 * math.sin(theta_rad)

    min_time = float('inf')
    min_index = -1

    for i in range(n):
        x0, y0 = vertices[i]
        t = calculate_time_to_wall(x0, y0, vx, vy, w)
        if t < min_time:
            min_time = t
            min_index = i + 1

    x0, y0 = vertices[min_index - 1]
    final_x, final_y = calculate_vertex_position(x0, y0, vx, vy, omega, min_time)

    print(min_index, min_time)

if __name__ == "__main__":
    main()