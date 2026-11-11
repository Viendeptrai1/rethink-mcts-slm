def can_unlock_all_doors(n, m, room_states, switches):
    from collections import defaultdict
    
    # Create adjacency list for the bipartite graph
    graph = defaultdict(list)
    
    for i in range(m):
        x = switches[i][0]
        for j in range(1, x + 1):
            room = switches[i][j]
            graph[room].append(i + n)  # Switches are numbered from n+1 to n+m
            graph[i + n].append(room)
    
    # Initialize the state of each switch (0 means off, 1 means on)
    switch_states = [0] * m
    
    # Function to toggle the state of a switch and its connected rooms
    def toggle_switch(switch_index):
        switch_states[switch_index] ^= 1
        for room in graph[switch_index + n]:
            room_states[room - 1] ^= 1
    
    # Try to toggle switches to unlock all doors
    for room in range(n):
        if room_states[room] == 0:  # If the room is locked
            for switch in graph[room + 1]:  # Find a switch that controls this room
                if switch_states[switch - n] == 0:  # If the switch is off
                    toggle_switch(switch - n)
                    break
    
    # Check if all doors are now unlocked
    for state in room_states:
        if state == 0:
            return "NO"
    
    return "YES"

# Read input
n, m = map(int, input().split())
room_states = list(map(int, input().split()))
switches = [list(map(int, input().split())) for _ in range(m)]

# Output the result
print(can_unlock_all_doors(n, m, room_states, switches))