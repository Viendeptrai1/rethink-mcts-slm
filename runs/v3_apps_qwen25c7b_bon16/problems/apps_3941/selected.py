from collections import defaultdict

def can_open_all_doors(n, m, rooms, switches):
    # Create a dictionary to store the switches controlling each door
    door_switches = defaultdict(list)
    
    # Populate the dictionary with switch information
    for i in range(m):
        _, *switch_rooms = switches[i]
        for room in switch_rooms:
            door_switches[room].append(i)
    
    # Function to toggle a switch
    def toggle(switch):
        for room in switches[switch][1:]:
            rooms[room - 1] ^= 1
    
    # Try toggling pairs of switches to see if we can unlock all doors
    for i in range(m):
        for j in range(i + 1, m):
            toggle(i)
            toggle(j)
            if all(rooms):
                return True
            toggle(j)
            toggle(i)
    
    return False

# Input reading
n, m = map(int, input().split())
rooms = list(map(int, input().split()))
switches = []
for _ in range(m):
    switches.append(list(map(int, input().split())))

# Output the result
if can_open_all_doors(n, m, rooms, switches):
    print("YES")
else:
    print("NO")