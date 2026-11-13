def find_earliest_takeoff(n, s, landings):
    # Convert all landings to minutes since the start of the day
    landings_in_minutes = [h * 60 + m for h, m in landings]
    
    # Check the time before the first landing
    if landings_in_minutes[0] >= s:
        return 0, 0
    
    # Check between each pair of landings
    for i in range(1, n):
        if landings_in_minutes[i] - landings_in_minutes[i - 1] >= 2 * s:
            # Calculate the earliest possible takeoff time
            takeoff_time = landings_in_minutes[i - 1] + s
            return divmod(takeoff_time, 60)
    
    # Check the time after the last landing
    last_landing = landings_in_minutes[-1]
    if 1440 - last_landing >= s:  # 1440 minutes in a day
        return divmod(last_landing + s, 60)
    
    # If no suitable time is found, return 24:00
    return 24, 0

# Read input
n, s = map(int, input().split())
landings = [tuple(map(int, input().split())) for _ in range(n)]

# Find and print the earliest takeoff time
h, m = find_earliest_takeoff(n, s, landings)
print(h, m)