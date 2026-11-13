def find_earliest_takeoff(n, s, landings):
    # Convert landings to minutes since the start of the day
    landings_in_minutes = [(h * 60 + m) for h, m in landings]
    
    # Check for the earliest possible takeoff time
    for takeoff_time in range(24 * 60 + 1):  # Check up to 24 hours later
        can_insert = True
        for landing in landings_in_minutes:
            if abs(takeoff_time - landing) < s:
                can_insert = False
                break
        if can_insert:
            # Convert back to hours and minutes
            h, m = divmod(takeoff_time, 60)
            return h, m

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
s = int(data[1])
landings = [(int(data[i * 2 + 2]), int(data[i * 2 + 3])) for i in range(n)]

# Find and print the earliest takeoff time
h, m = find_earliest_takeoff(n, s, landings)
print(h, m)