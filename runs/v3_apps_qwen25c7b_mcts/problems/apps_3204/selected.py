import sys

def min_bridge_unavailability(N, arrival_times):
    total_unavailability = 0
    current_time = 0
    bridge_up = False
    
    for arrival_time in arrival_times:
        if not bridge_up:
            # Raise the bridge
            current_time += 60
            bridge_up = True
        
        if current_time > arrival_time:
            # Boat arrived before bridge was ready, calculate wait time
            wait_time = current_time - arrival_time
            if wait_time > 1800:
                return -1  # More than 30 minutes wait time, impossible to satisfy requirement
            current_time += 20
        else:
            # Boat arrived after bridge was ready, just let it pass
            current_time += 20
        
        # Check if we need to lower the bridge immediately
        if N == 1 or arrival_times[N-1] - arrival_time <= 20:
            bridge_up = False
            current_time += 60
    
    return total_unavailability

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
arrival_times = list(map(int, data[1:]))

# Calculate and print result
result = min_bridge_unavailability(N, arrival_times)
print(result)