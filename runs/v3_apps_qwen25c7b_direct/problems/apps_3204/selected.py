import sys

def min_unavailable_time(N, arrival_times):
    total_unavailable = 0
    current_time = 0
    bridge_up = False
    
    for T in arrival_times:
        if not bridge_up:
            # Raise the bridge
            current_time += 60
            bridge_up = True
        
        if current_time > T:
            # Boat arrived before bridge was ready, wait
            wait_time = T - current_time
            if wait_time > 30 * 60:
                return -1  # Not possible to meet the requirement
            current_time += wait_time
        
        # Boat passes through the bridge
        current_time += 20
        
        # Lower the bridge after the boat has passed
        if current_time >= T + 20:
            bridge_up = False
        else:
            current_time += 60
            bridge_up = True
        
        total_unavailable += 60
    
    return total_unavailable

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
arrival_times = list(map(int, data[1:]))

# Calculate and print the result
result = min_unavailable_time(N, arrival_times)
print(result)