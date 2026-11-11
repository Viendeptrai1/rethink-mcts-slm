def operate_bridge(N, arrival_times):
    total_unavailable_time = 0
    current_time = 0
    queue = []
    
    for arrival in arrival_times:
        # Lower the bridge if it's up and there are no boats waiting
        if not queue:
            total_unavailable_time += 60
            current_time += 60
        
        # Add the boat to the queue
        queue.append(arrival)
        
        # Process the queue
        while queue:
            boat_arrival = queue[0]
            if current_time >= boat_arrival + 1800:  # 30 minutes wait time
                break
            
            # Raise the bridge if it's down
            if current_time < boat_arrival:
                total_unavailable_time += 60
                current_time = boat_arrival + 60
            
            # Boat passes through
            current_time += 20
            queue.pop(0)
        
        # Lower the bridge after the last boat passes
        if queue:
            total_unavailable_time += 60
            current_time += 60
    
    return total_unavailable_time

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
arrival_times = list(map(int, data[1:]))

# Output the result
print(operate_bridge(N, arrival_times))