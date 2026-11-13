from sys import stdin, stdout

def find_takeoff_time(n, s):
    landings = [tuple(map(int, stdin.readline().split())) for _ in range(n)]
    
    # Check if we can insert takeoff before the first landing
    if landings[0][0] * 60 + landings[0][1] > s:
        return 0, 0
    
    # Check for gaps between consecutive landings
    for i in range(1, n):
        gap = (landings[i][0] * 60 + landings[i][1]) - (landings[i-1][0] * 60 + landings[i-1][1])
        if gap > 2 * s + 1:
            return landings[i-1][0], landings[i-1][1] + s + 1
    
    # If no valid gap found, insert takeoff after the last landing with the required safety margin
    last_landing = landings[-1]
    takeoff_hour = last_landing[0] + (last_landing[1] + s + 1) // 60
    takeoff_minute = (last_landing[1] + s + 1) % 60
    return takeoff_hour, takeoff_minute

# Read input
n, s = map(int, stdin.readline().split())

# Find and print the takeoff time
takeoff_time = find_takeoff_time(n, s)
stdout.write(f"{takeoff_time[0]} {takeoff_time[1]}\n")