import sys
import math

def min_time_to_destination(x1, y1, x2, y2, v_max, t, wind1, wind2):
    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def time_to_reach_destination(x1, y1, x2, y2, vx, vy, v_max):
        dx, dy = x2 - x1, y2 - y1
        dot_product = dx * vx + dy * vy
        if dot_product < 0:
            return float('inf')
        v_rel = math.sqrt(vx ** 2 + vy ** 2)
        if v_rel > v_max:
            return float('inf')
        return distance(x1, y1, x2, y2) / v_rel

    vx1, vy1 = wind1
    vx2, vy2 = wind2

    # Calculate time to reach destination with initial wind
    time_with_wind1 = time_to_reach_destination(x1, y1, x2, y2, vx1, vy1, v_max)

    # Calculate time to reach destination with second wind
    time_with_wind2 = time_to_reach_destination(x1, y1, x2, y2, vx2, vy2, v_max)

    # Return the minimum time
    return min(time_with_wind1, time_with_wind2)

def main():
    input = sys.stdin.read
    data = input().split()
    
    x1 = int(data[0])
    y1 = int(data[1])
    x2 = int(data[2])
    y2 = int(data[3])
    v_max = int(data[4])
    t = int(data[5])
    
    vx1 = int(data[6])
    vy1 = int(data[7])
    vx2 = int(data[8])
    vy2 = int(data[9])
    
    wind1 = (vx1, vy1)
    wind2 = (vx2, vy2)
    
    result = min_time_to_destination(x1, y1, x2, y2, v_max, t, wind1, wind2)
    print(result)

if __name__ == "__main__":
    main()