from sys import stdin, stdout

def find_earliest_takeoff_time(n, s, landings):
    # Convert landings to total minutes since midnight
    landings_minutes = [h * 60 + m for h, m in landings]
    
    # Check if we can take off immediately after the last landing
    if landings_minutes[-1] + s < 24 * 60:
        return landings_minutes[-1] + s
    
    # Check for gaps between consecutive landings
    for i in range(1, n):
        gap = landings_minutes[i] - landings_minutes[i-1] - 1
        if gap >= 2 * s + 1:
            return landings_minutes[i-1] + s + 1
    
    # If no suitable gap found, take off after the last landing with the required spacing
    return landings_minutes[-1] + s + 1

# Read input
n, s = map(int, stdin.readline().split())
landings = [tuple(map(int, stdin.readline().split())) for _ in range(n)]

# Find and print the earliest takeoff time
takeoff_time = find_earliest_takeoff_time(n, s, landings)
stdout.write(f"{takeoff_time // 60} {takeoff_time % 60}\n")