import sys
from math import sqrt, atan2, cos, sin

def min_time_to_rescue(x1, y1, x2, y2, vmax, t, winds):
    def distance(x1, y1, x2, y2):
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def predict_position(x, y, vx, vy, wx, wy, dt):
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
    
    def binary_search(x, y, vx, vy, wx, wy, target_x, target_y, epsilon=1e-6):
        left, right = 0, max(distance(x, y, target_x, target_y), 1)
        while right - left > epsilon:
            mid = (left + right) / 2
            pos_x, pos_y = predict_position(x, y, vx, vy, wx, wy, mid)
            if distance(pos_x, pos_y, target_x, target_y) <= epsilon:
                return mid
            elif distance(pos_x, pos_y, target_x, target_y) < distance(target_x, target_y, target_x, target_y):
                left = mid
            else:
                right = mid
        return left
    
    x, y = x1, y1
    vx, vy = 0, 0
    wx, wy = winds[0]
    total_time = 0
    
    for i in range(t):
        dt = binary_search(x, y, vx, vy, wx, wy, x2, y2)
        x, y = predict_position(x, y, vx, vy, wx, wy, dt)
        total_time += dt
        vx, vy = 0, 0
        wx, wy = winds[i+1]
    
    dt = binary_search(x, y, vx, vy, wx, wy, x2, y2)
    total_time += dt
    
    return total_time

# Read input
input = sys.stdin.read
data = input().split()
x1, y1, x2, y2 = int(data[0]), int(data[1]), int(data[2]), int(data[3])
vmax, t = int(data[4]), int(data[5])
winds = [(int(data[6 + 2*i]), int(data[7 + 2*i])) for i in range(t + 1)]

# Calculate and print the result
result = min_time_to_rescue(x1, y1, x2, y2, vmax, t, winds)
print(result)