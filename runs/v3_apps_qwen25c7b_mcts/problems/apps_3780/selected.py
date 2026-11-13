import sys
from math import sqrt, atan2, cos, sin

def min_time_to_rescue(x1, y1, x2, y2, vmax, t, winds):
    def distance(x1, y1, x2, y2):
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def move(x, y, vx, vy, wx, wy, dt):
        return x + dt * (vx + wx), y + dt * (vy + wy)
    
    def time_to_reach_target(x, y, vx, vy, wx, wy, tx, ty):
        dx, dy = tx - x, ty - y
        dvx, dvy = vx + wx, vy + wy
        a = dvx**2 + dvy**2
        b = 2 * (dx*dvx + dy*dvy)
        c = dx**2 + dy**2
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return float('inf')
        t1 = (-b + sqrt(discriminant)) / (2*a)
        t2 = (-b - sqrt(discriminant)) / (2*a)
        if t1 >= 0:
            return t1
        elif t2 >= 0:
            return t2
        else:
            return float('inf')
    
    x, y = x1, y1
    total_time = 0
    
    for i in range(t):
        wx, wy = winds[i]
        dt = time_to_reach_target(x, y, 0, 0, wx, wy, x2, y2)
        if dt == float('inf'):
            break
        x, y = move(x, y, 0, 0, wx, wy, dt)
        total_time += dt
    
    wx, wy = winds[t]
    dt = time_to_reach_target(x, y, 0, 0, wx, wy, x2, y2)
    if dt != float('inf'):
        total_time += dt
    
    return total_time

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    x1 = int(data[0])
    y1 = int(data[1])
    x2 = int(data[2])
    y2 = int(data[3])
    vmax = int(data[4])
    t = int(data[5])
    
    winds = []
    for i in range(2*t):
        wx = int(data[6 + 2*i])
        wy = int(data[7 + 2*i])
        winds.append((wx, wy))
    
    result = min_time_to_rescue(x1, y1, x2, y2, vmax, t, winds)
    print(result)