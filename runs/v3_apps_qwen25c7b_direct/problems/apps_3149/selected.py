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
    
    vertices = []
    for _ in range(n):
        x = float(data[index + 5 + 2 * _])
        y = float(data[index + 6 + 2 * _])
        vertices.append((x, y))
    
    g = 9.81
    
    min_time = float('inf')
    min_index = -1
    
    for i, (x0, y0) in enumerate(vertices):
        vx = v0 * cos(theta_rad)
        vy = v0 * sin(theta_rad)
        
        ax = -omega * y0
        ay = omega * x0
        
        t = None
        if ax != 0:
            t = (w - x0) / ax
        
        if t is not None and t > 0:
            xf = x0 + vx * t + 0.5 * ax * t**2
            yf = y0 + vy * t + 0.5 * ay * t**2
            
            if yf >= 0:
                if t < min_time:
                    min_time = t
                    min_index = i + 1
    
    print(min_index, min_time)

find_first_corner_to_hit_wall()