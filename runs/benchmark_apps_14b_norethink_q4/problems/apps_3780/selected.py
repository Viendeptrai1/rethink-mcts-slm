import sys
import math
from scipy.optimize import minimize

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def travel_time(x1, y1, x2, y2, v_max, t, v_wind1, v_wind2):
    def objective(t1):
        # Time spent flying with the first wind
        t2 = max(0, t - t1)
        # Position after t1 seconds with the first wind
        x_t1 = x1 + t1 * v_wind1[0]
        y_t1 = y1 + t1 * v_wind1[1]
        # Remaining distance to cover after t1 seconds
        remaining_distance = distance(x_t1, y_t1, x2, y2)
        # Time spent flying with the second wind
        t2_required = remaining_distance / v_max
        # Total time
        return t1 + t2 + t2_required
    
    # Initial guess for t1
    initial_guess = [t / 2]
    # Constraints: 0 <= t1 <= t
    bounds = [(0, t)]
    # Minimize the travel time
    result = minimize(objective, initial_guess, bounds=bounds)
    return result.fun

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    x1 = int(data[0])
    y1 = int(data[1])
    x2 = int(data[2])
    y2 = int(data[3])
    v_max = int(data[4])
    t = int(data[5])
    v_wind1 = (int(data[6]), int(data[7]))
    v_wind2 = (int(data[8]), int(data[9]))
    
    result = travel_time(x1, y1, x2, y2, v_max, t, v_wind1, v_wind2)
    print(result)

if __name__ == "__main__":
    main()