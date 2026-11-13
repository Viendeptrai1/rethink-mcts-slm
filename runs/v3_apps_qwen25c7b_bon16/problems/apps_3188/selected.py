import sys

def min_tunnel_cost(N, planets):
    # Extract x, y, and z coordinates into separate lists
    x_coords = sorted([planet[0] for planet in planets])
    y_coords = sorted([planet[1] for planet in planets])
    z_coords = sorted([planet[2] for planet in planets])

    # Calculate the minimum distance differences
    min_x_diff = float('inf')
    min_y_diff = float('inf')
    min_z_diff = float('inf')

    for i in range(1, N):
        min_x_diff = min(min_x_diff, abs(x_coords[i] - x_coords[i - 1]))
        min_y_diff = min(min_y_diff, abs(y_coords[i] - y_coords[i - 1]))
        min_z_diff = min(min_z_diff, abs(z_coords[i] - z_coords[i - 1]))

    # The minimum cost will be the sum of the smallest differences in each dimension
    return min(min_x_diff, min_y_diff, min_z_diff)

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
planets = [(int(data[3 * i + 1]), int(data[3 * i + 2]), int(data[3 * i + 3])) for i in range(N)]

# Compute and print the result
print(min_tunnel_cost(N, planets))