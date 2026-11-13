def calculate_bridge_unavailability():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    T = list(map(int, data[1:]))
    
    bridge_up_time = 0
    bridge_down_time = 0
    current_time = 0
    
    for i in range(N):
        arrival_time = T[i]
        
        # If the current time is less than the arrival time, move the current time to the arrival time
        if current_time < arrival_time:
            current_time = arrival_time
        
        # Calculate the time when the bridge can be raised
        bridge_up_time = max(bridge_up_time, current_time)
        
        # Calculate the time when the boat will leave the bridge
        boat_exit_time = current_time + 20
        
        # Update the current time to the boat exit time
        current_time = boat_exit_time
    
    # Calculate the total bridge unavailability time
    total_unavailability = current_time - T[0]
    
    print(total_unavailability)