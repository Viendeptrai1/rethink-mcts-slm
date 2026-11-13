import sys
from math import sin, cos, radians, sqrt

def find_first_corner_to_hit_wall():
    # Read input
    data = sys.stdin.read().split()
    index = 0
    
    n = int(data[index])
    omega = float(data[index + 1])
    v0 = float(data[index + 2])
    theta_deg = int(data[index + 3])
    w = float(data[index + 4])
    
    theta_rad = radians(theta_deg)
    
    corners = []
    for _ in range(n):
        x_i = float(data[index + 5 + 2 * _])
        y_i = float(data[index + 6 + 2 * _])
        corners.append((x_i, y_i))
    
    g = 9.81
    
    min_time = float('inf')
    min_index = -1
    
    for i, (x_i, y_i) in enumerate(corners):
        # Initial velocity components
        v0_x = v0 * cos(theta_rad)
        v0_y = v0 * sin(theta_rad)
        
        # Time to reach the wall
        t = (w - x_i) / v0_x
        
        # Position of the corner at time t
        x_t = x_i + v0_x * t
        y_t = y_i + v0_y * t - 0.5 * g * t**2
        
        if y_t >= 0:
            if t < min_time:
                min_time = t
                min_index = i + 1
    
    print(min_index, min_time)

find_first_corner_to_hit_wall()