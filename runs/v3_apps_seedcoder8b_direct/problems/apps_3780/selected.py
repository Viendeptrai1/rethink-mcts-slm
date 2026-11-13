import sys
import math

def min_time_to_destination(x1, y1, x2, y2, v_max, t, wind1, wind2):
    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def time_to_reach_destination(x1, y1, x2, y2, vx, vy, v_max):
        dist = distance(x1, y1, x2, y2)
        if vx == vy == 0:
            return float('inf')
        speed = math.sqrt(vx ** 2 + vy ** 2)
        if speed > v_max:
            return float('inf')
        return dist / speed

    def optimal_time(x1, y1, x2, y2, v_max, t, wind1, wind2):
        vx1, vy1 = wind1
        vx2, vy2 = wind2

        # Calculate time to reach destination with initial wind
        time_with_wind1 = time_to_reach_destination(x1, y1, x2, y2, vx1, vy1, v_max)

        # Calculate time to reach destination with second wind
        time_with_wind2 = time_to_reach_destination(x1, y1, x2, y2, vx2, vy2, v_max)

        # If the destination is reachable with either wind, return the minimum time
        if time_with_wind1 < float('inf') or time_with_wind2 < float('inf'):
            return min(time_with_wind1, time_with_wind2)

        # If neither wind can reach the destination, return infinity
        return float('inf')

    return optimal_time(x1, y1, x2, y2, v_max, t, wind1, wind2)

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
    wx1 = int(data[8])
    wy1 = int(data[9])
    
    vx2 = int(data[10])
    vy2 = int(data[11])
    
    result = min_time_to_destination(x1, y1, x2, y2, v_max, t, (vx1, vy1), (vx2, vy2))
    print(result)

if __name__ == "__main__":
    main()