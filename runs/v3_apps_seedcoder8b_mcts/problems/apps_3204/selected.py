def calculate_bridge_unavailability():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    T = list(map(int, data[1:N+1]))
    
    bridge_up_time = 0
    bridge_down_time = 0
    current_time = 0
    bridge_raised = False
    boats_waiting = 0
    
    for i in range(N):
        arrival_time = T[i]
        
        # Move time forward to the next boat's arrival if needed
        if current_time < arrival_time:
            current_time = arrival_time
        
        # If the bridge is not raised, raise it
        if not bridge_raised:
            bridge_up_time += 60
            bridge_raised = True
            current_time += 60
        
        # If the bridge is raised, check if the next boat can pass immediately
        if bridge_raised:
            if current_time + 20 <= arrival_time:
                # The boat can pass immediately
                current_time += 20
            else:
                # The boat must wait
                boats_waiting += 1
                # Calculate the time until the bridge is available
                bridge_available_time = current_time + 20
                # Wait until the bridge is available
                current_time = bridge_available_time
        
        # If there are boats waiting, let them pass
        if boats_waiting > 0:
            # Time to pass all waiting boats
            current_time += 20 * boats_waiting
            # Lower the bridge after all boats have passed
            bridge_down_time += 60
            bridge_raised = False
            boats_waiting = 0
    
    # Calculate total unavailable time
    total_unavailable_time = bridge_up_time + bridge_down_time
    print(total_unavailable_time)