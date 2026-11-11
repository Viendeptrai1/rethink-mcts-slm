def operate_bridge(N, arrival_times):
    bridge_unavailable_time = 0
    current_time = 0
    boats_waiting = []
    
    for arrival_time in arrival_times:
        # Check if the bridge can be lowered for the next boat
        if boats_waiting:
            next_arrival = boats_waiting[0]
            if current_time >= next_arrival + 30 * 60:
                # Lower the bridge
                bridge_unavailable_time += 60
                current_time += 60
                # All waiting boats pass through
                bridge_unavailable_time += len(boats_waiting) * 20
                current_time += len(boats_waiting) * 20
                boats_waiting = []
        
        # Raise the bridge if it's not already raised
        if current_time < arrival_time:
            bridge_unavailable_time += 60
            current_time = arrival_time + 60
        
        # Add the current boat to the waiting list
        boats_waiting.append(arrival_time)
    
    # Process any remaining boats
    if boats_waiting:
        next_arrival = boats_waiting[0]
        if current_time >= next_arrival + 30 * 60:
            # Lower the bridge
            bridge_unavailable_time += 60
            current_time += 60
            # All waiting boats pass through
            bridge_unavailable_time += len(boats_waiting) * 20
            current_time += len(boats_waiting) * 20
        else:
            # Keep the bridge raised for the last batch of boats
            bridge_unavailable_time += 60
            current_time += 60
            bridge_unavailable_time += len(boats_waiting) * 20
            current_time += len(boats_waiting) * 20
    
    return bridge_unavailable_time

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
arrival_times = list(map(int, data[1:]))

# Output the result
print(operate_bridge(N, arrival_times))