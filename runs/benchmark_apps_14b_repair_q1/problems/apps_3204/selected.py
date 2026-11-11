import sys

def main():
    import sys
    import heapq
    
    def operate_bridge(N, times):
        bridge_unavailable = 0
        current_time = 0
        boat_queue = []
        last_boat_time = 0
        
        for arrival_time in times:
            # Lower the bridge if it's been up for more than 30 minutes
            if current_time - last_boat_time > 1800:
                current_time += 60
                bridge_unavailable += 60
            
            # Add the current boat to the queue
            heapq.heappush(boat_queue, (arrival_time, arrival_time))
            
            # Process the boats in the queue
            while boat_queue:
                boat_arrival, boat_pass_time = heapq.heappop(boat_queue)
                
                # If the boat has to wait, skip to its arrival time
                if current_time < boat_arrival:
                    current_time = boat_arrival
                
                # Raise the bridge if it's not already raised
                if current_time == boat_arrival:
                    current_time += 60
                    bridge_unavailable += 60
                
                # Pass the boat through the bridge
                current_time += 20
                last_boat_time = current_time
                
                # Keep the bridge raised if the next boat is arriving soon
                if boat_queue and boat_queue[0][0] <= current_time + 20:
                    continue
                
                # Lower the bridge after the last boat passes
                current_time += 60
                bridge_unavailable += 60
                break
        
        return bridge_unavailable
    
    # Read input
    N = int(sys.stdin.readline().strip())
    times = [int(sys.stdin.readline().strip()) for _ in range(N)]
    
    # Calculate and print the result
    result = operate_bridge(N, times)
    print(result)

if __name__ == "__main__":
    main()