import sys
from math import sin, cos, pi, sqrt

def find_first_corner_hit():
    # Read input
    input_data = sys.stdin.read().split()
    index = 0
    n = int(input_data[index])
    omega = float(input_data[index + 1])
    v0 = float(input_data[index + 2])
    theta = float(input_data[index + 3]) * pi / 180
    w = float(input_data[index + 4])
    index += 5
    
    vertices = []
    for _ in range(n):
        x = float(input_data[index])
        y = float(input_data[index + 1])
        vertices.append((x, y))
        index += 2
    
    g = 9.81
    t_min = float('inf')
    corner_index = -1
    
    for i, (x, y) in enumerate(vertices):
        vx = v0 * cos(theta)
        vy = v0 * sin(theta)
        
        # Adjust initial velocity due to rotation
        vx -= omega * y
        vy += omega * x
        
        # Time of flight until hitting the wall
        if vy > 0:
            t = (w - x) / vx
            y_at_t = y + vy * t - 0.5 * g * t**2
            if y <= y_at_t < 0:
                if t < t_min:
                    t_min = t
                    corner_index = i + 1
    
    print(corner_index, t_min)

find_first_corner_hit()