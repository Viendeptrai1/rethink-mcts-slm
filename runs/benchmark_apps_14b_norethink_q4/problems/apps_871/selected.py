def find_earliest_takeoff(n, s, landings):
    def time_to_minutes(h, m):
        return h * 60 + m
    
    def minutes_to_time(minutes):
        h = minutes // 60
        m = minutes % 60
        return h, m
    
    # Convert all landing times to minutes from start
    landing_times = [time_to_minutes(h, m) for h, m in landings]
    
    # Check for a gap between landings
    for i in range(1, n):
        prev_landing = landing_times[i - 1]
        current_landing = landing_times[i]
        
        if current_landing - prev_landing > 2 * s + 1:
            # Found a suitable gap
            takeoff_time = prev_landing + s + 1
            return minutes_to_time(takeoff_time)
    
    # Check if we can insert takeoff after the last landing
    if 1440 - landing_times[-1] > s:
        takeoff_time = landing_times[-1] + s + 1
        return minutes_to_time(takeoff_time)
    
    # If no suitable time is found, we need to wait for the next day
    return 24, 0

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
s = int(data[1])
landings = []
for i in range(n):
    h = int(data[2 + 2 * i])
    m = int(data[3 + 2 * i])
    landings.append((h, m))

# Find the earliest takeoff time
h, m = find_earliest_takeoff(n, s, landings)

# Print the result
print(h, m)