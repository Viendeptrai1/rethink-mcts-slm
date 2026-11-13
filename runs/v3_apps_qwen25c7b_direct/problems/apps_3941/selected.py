def can_unlock_all_doors(n, m, doors, switches):
    # Create a list to keep track of the parity of toggles for each door
    toggle_parity = [0] * n
    
    # Process each switch and update the toggle parity for the controlled doors
    for switch in switches:
        num_rooms = switch[0]
        rooms = switch[1:]
        for room in rooms:
            toggle_parity[room - 1] ^= 1
    
    # Check if the final state of each door matches the desired state
    for i in range(n):
        if (doors[i] == 0 and toggle_parity[i] == 0) or (doors[i] == 1 and toggle_parity[i] == 1):
            return "NO"
    
    return "YES"

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

doors = list(map(int, data[2:2+n]))
switches = []

index = 2 + n
for _ in range(m):
    x = int(data[index])
    rooms = list(map(int, data[index+1:index+x+1]))
    switches.append((x, *rooms))
    index += x + 1

# Output result
print(can_unlock_all_doors(n, m, doors, switches))