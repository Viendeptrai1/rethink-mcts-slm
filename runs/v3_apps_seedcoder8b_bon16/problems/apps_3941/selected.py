def can_unlock_all_doors(n, m, room_status, switches):
    # Create a list to track the toggles required for each room
    toggle_count = [0] * (n + 1)

    # Process each switch
    for switch in switches:
        toggle_rooms = switch[1:]
        # Each switch affects the toggle count for each room it controls
        for room in toggle_rooms:
            toggle_count[room] += 1

    # Check the resulting status of each room after all switches have been toggled
    for i in range(1, n + 1):
        # Calculate the final status of the room
        final_status = (room_status[i - 1] + toggle_count[i]) % 2
        # If any room is still locked, return NO
        if final_status == 0:
            return "NO"

    return "YES"

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse inputs
n = int(data[0])
m = int(data[1])
room_status = list(map(int, data[2:n+2]))
switches = []
index = n + 2
for _ in range(m):
    k = int(data[index])
    switch_rooms = list(map(int, data[index + 1: index + 1 + k]))
    switches.append([k] + switch_rooms)
    index += 1 + k

# Get the result
result = can_unlock_all_doors(n, m, room_status, switches)

# Print the result
print(result)