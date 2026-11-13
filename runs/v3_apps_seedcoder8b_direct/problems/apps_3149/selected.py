import sys
import math

def find_first_wall_hit(n, omega, v0, theta, w, vertices):
    g = 9.81  # acceleration due to gravity in m/s^2

    # Convert theta from degrees to radians
    theta_rad = math.radians(theta)

    # Initial velocity components
    vx0 = v0 * math.cos(theta_rad)
    vy0 = v0 * math.sin(theta_rad)

    # Function to calculate the time to hit the wall for a given vertex
    def time_to_wall(x, y):
        if vx0 == 0:
            return float('inf')  # Parallel to the wall, never hits

        # Calculate the time to hit the wall for this vertex
        tx = (w - x) / vx0
        ty = -y * vx0 / (vy0 + 0.5 * g * tx)

        if ty < 0:
            return float('inf')  # The vertex is below the wall at this time

        return max(tx, ty)

    # Calculate the angular displacement for each vertex
    def angular_displacement(t):
        return omega * t

    # Calculate the rotated position of each vertex
    def rotated_position(x, y, t):
        angle = angular_displacement(t)
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        return x * cos_angle - y * sin_angle, x * sin_angle + y * cos_angle

    # Find the vertex that hits the wall first
    min_time = float('inf')
    min_index = -1

    for i in range(n):
        x, y = vertices[i]
        t = time_to_wall(x, y)
        if t < min_time:
            min_time = t
            min_index = i

    # Adjust the position of the cookie to account for its rotation at the time of impact
    x_hit, y_hit = rotated_position(vertices[min_index][0], vertices[min_index][1], min_time)

    # Output the result
    print(f"{min_index + 1} {min_time:.6f}")

def main():
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    omega = float(data[1])
    v0 = float(data[2])
    theta = int(data[3])
    w = float(data[4])

    vertices = []
    index = 5
    for _ in range(n):
        x = float(data[index])
        y = float(data[index + 1])
        vertices.append((x, y))
        index += 2

    find_first_wall_hit(n, omega, v0, theta, w, vertices)

if __name__ == "__main__":
    main()