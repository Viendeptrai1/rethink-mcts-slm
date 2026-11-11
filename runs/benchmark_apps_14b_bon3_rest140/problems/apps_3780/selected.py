import math
from scipy.optimize import minimize

def distance(x, y):
    return math.sqrt(x**2 + y**2)

def travel_time(v_max, t, wind1, wind2, start, end):
    def objective(velocity):
        vx, vy = velocity
        # First segment
        dx1 = start[0] + vx * t + wind1[0] * t - end[0]
        dy1 = start[1] + vy * t + wind1[1] * t - end[1]
        dist1 = distance(dx1, dy1)
        time1 = t + dist1 / v_max
        
        # Second segment
        dx2 = start[0] + vx * time1 + wind2[0] * time1 - end[0]
        dy2 = start[1] + vy * time1 + wind2[1] * time1 - end[1]
        dist2 = distance(dx2, dy2)
        time2 = time1 + dist2 / v_max
        
        return time2
    
    constraints = ({'type': 'ineq', 'fun': lambda v: v_max**2 - (v[0]**2 + v[1]**2)})
    result = minimize(objective, [0, 0], constraints=constraints)
    return result.fun

# Reading input
import sys
input = sys.stdin.read
data = input().split()

x1, y1, x2, y2 = map(int, data[:4])
v_max, t = map(int, data[4:6])
wind1 = tuple(map(int, data[6:8]))
wind2 = tuple(map(int, data[8:10]))

# Calculating the minimum time
min_time = travel_time(v_max, t, wind1, wind2, (x1, y1), (x2, y2))
print(min_time)