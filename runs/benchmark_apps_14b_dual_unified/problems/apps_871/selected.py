def find_earliest_takeoff(n, s, landings):
    # Convert landing times to minutes since start
    landing_times = [h * 60 + m for h, m in landings]
    
    # Check for possible takeoff times
    for i in range(len(landing_times) + 1):
        if i == 0:
            # Before the first landing
            if landing_times[0] >= s:
                return (0, 0)
        elif i == len(landing_times):
            # After the last landing
            if 24 * 60 - landing_times[-1] > s:
                return (23, 59)
        else:
            # Between two landings
            if landing_times[i] - landing_times[i - 1] > 2 * s:
                takeoff_time = landing_times[i - 1] + s
                return (takeoff_time // 60, takeoff_time % 60)
    
    # If no valid time found, return (24, 50) as per the problem statement
    return (24, 50)

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
s = int(data[1])
landings = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(n)]

# Find and print the earliest takeoff time
h, m = find_earliest_takeoff(n, s, landings)
print(h, m)