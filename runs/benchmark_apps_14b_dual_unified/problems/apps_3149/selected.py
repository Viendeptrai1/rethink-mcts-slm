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
    vx0 = v0 * math.cos(theta_rad)
    vy0 = v0 * math.sin(theta_rad)
    
    min_time = float('inf')
    min_vertex_index = -1
    
    for i, (x0, y0) in enumerate(vertices):
        for t in [0, 2 * math.pi / omega]:
            x = x0 + vx0 * t - 0.5 * g * (t ** 2) * math.sin(omega * t)
            y = y0 + vy0 * t + 0.5 * g * (t ** 2) * math.cos(omega * t)
            
            if x >= w:
                time_to_wall = (w - x0) / vx0
                if time_to_wall > 0:
                    time_to_wall -= 0.5 * g * (time_to_wall ** 2) * math.sin(omega * time_to_wall)
                    if time_to_wall < min_time:
                        min_time = time_to_wall
                        min_vertex_index = i + 1
    
    print(min_vertex_index, min_time)

if __name__ == "__main__":
    main()