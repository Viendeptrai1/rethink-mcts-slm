import sys

def main():
    import sys
    import heapq
    
    def operate_bridge(N, times):
        # Initialize variables
        current_time = 0
        bridge_up = False
        bridge_up_time = 0
        total_downtime = 0
        boat_queue = []
        
        # Process each boat arrival
        for arrival_time in times:
            # Check if the bridge needs to be lowered
            if bridge_up and arrival_time > bridge_up_time + 30 * 60:
                total_downtime += current_time - bridge_up_time
                bridge_up = False
            
            # If the bridge is not up and the next boat arrives within 30 minutes
            if not bridge_up and arrival_time <= current_time + 30 * 60:
                bridge_up = True
                bridge_up_time = current_time
                current_time += 60  # Time to raise the bridge
            
            # Add the boat to the queue
            heapq.heappush(boat_queue, arrival_time)
            
            # Process all boats that can pass through the bridge
            while boat_queue and boat_queue[0] <= current_time:
                current_time += 20  # Time for one boat to pass through
        
        # Lower the bridge if it was up
        if bridge_up:
            total_downtime += current_time - bridge_up_time
        
        return total_downtime
    
    # Read input
    N = int(sys.stdin.readline().strip())
    times = [int(sys.stdin.readline().strip()) for _ in range(N)]
    
    # Output the result
    print(operate_bridge(N, times))

if __name__ == "__main__":
    main()