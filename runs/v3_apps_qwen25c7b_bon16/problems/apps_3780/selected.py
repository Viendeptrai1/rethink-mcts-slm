import sys
from math import sqrt, atan2, pi

def read_input():
    input = sys.stdin.read
    data = input().split()
    index = 0
    
    x1 = int(data[index])
    index += 1
    y1 = int(data[index])
    index += 1
    x2 = int(data[index])
    index += 1
    y2 = int(data[index])
    index += 1
    
    vmax = int(data[index])
    index += 1
    t = int(data[index])
    index += 1
    
    wind_t = []
    for _ in range(t):
        vx = int(data[index])
        index += 1
        vy = int(data[index])
        index += 1
        wind_t.append((vx, vy))
    
    wind_inf = []
    wx = int(data[index])
    index += 1
    wy = int(data[index])
    index += 1
    wind_inf.append((wx, wy))
    
    return x1, y1, x2, y2, vmax, t, wind_t, wind_inf

def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def min_time_to_reach_target(x1, y1, x2, y2, vmax, t, wind_t, wind_inf):
    dx, dy = x2 - x1, y2 - y1
    dist = distance(x1, y1, x2, y2)
    
    # Calculate the optimal time using binary search
    left, right = 0, dist / vmax
    while right - left > 1e-6:
        mid = (left + right) / 2
        x, y = x1, y1
        
        # Simulate the flight under wind for the first t seconds
        for i in range(min(int(mid), t)):
            ux, uy = wind_t[i]
            tx = min(mid, t) if i == t-1 else t
            x += tx * ux
            y += tx * uy
        
        # Adjust the speed for the remaining time
        remaining_dist = distance(x, y, x2, y2)
        remaining_time = mid - sum(range(min(int(mid), t)))
        max_speed_in_remaining_time = vmax * remaining_time
        
        # Check if we can reach the target within the remaining time
        if remaining_dist <= max_speed_in_remaining_time:
            right = mid
        else:
            left = mid
    
    return right

if __name__ == "__main__":
    x1, y1, x2, y2, vmax, t, wind_t, wind_inf = read_input()
    result = min_time_to_reach_target(x1, y1, x2, y2, vmax, t, wind_t, wind_inf)
    print(result)