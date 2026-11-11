import sys

def main():
    import sys
    import heapq
    
    def simulate_boats(arrival_times):
        bridge_unavailable = 0
        current_time = 0
        boat_queue = []
        bridge_status = 'lowered'  # 'lowered' or 'raised'
        raise_time = 0
        lower_time = 0
        
        for arrival_time in arrival_times:
            # Move forward in time to the next event
            if boat_queue:
                next_event_time = min(boat_queue[0][0], arrival_time)
            else:
                next_event_time = arrival_time
            
            # Process all boats that have arrived up to the next event time
            while boat_queue and boat_queue[0][0] <= next_event_time:
                _, boat_id = heapq.heappop(boat_queue)
                if bridge_status == 'lowered':
                    # Raise the bridge
                    bridge_status = 'raising'
                    raise_time = next_event_time + 60
                    bridge_unavailable += 60
                # Boat passes through the bridge
                current_time = max(current_time, next_event_time)
                current_time += 20
                bridge_unavailable += 20
            
            # If the bridge is raising and we've reached the raise time
            if bridge_status == 'raising' and current_time >= raise_time:
                bridge_status = 'raised'
            
            # If the bridge is raised and there are no boats waiting, lower it
            if bridge_status == 'raised' and not boat_queue:
                bridge_status = 'lowering'
                lower_time = current_time + 60
                bridge_unavailable += 60
            
            # If the bridge is lowering and we've reached the lower time
            if bridge_status == 'lowering' and current_time >= lower_time:
                bridge_status = 'lowered'
            
            # Add the current boat to the queue
            heapq.heappush(boat_queue, (arrival_time, len(boat_queue)))
        
        # Process remaining boats in the queue
        while boat_queue:
            next_event_time = boat_queue[0][0]
            if bridge_status == 'lowered':
                # Raise the bridge
                bridge_status = 'raising'
                raise_time = next_event_time + 60
                bridge_unavailable += 60
            
            # Process all boats that have arrived up to the next event time
            while boat_queue and boat_queue[0][0] <= next_event_time:
                _, boat_id = heapq.heappop(boat_queue)
                # Boat passes through the bridge
                current_time = max(current_time, next_event_time)
                current_time += 20
                bridge_unavailable += 20
            
            # If the bridge is raising and we've reached the raise time
            if bridge_status == 'raising' and current_time >= raise_time:
                bridge_status = 'raised'
            
            # If the bridge is raised and there are no boats waiting, lower it
            if bridge_status == 'raised' and not boat_queue:
                bridge_status = 'lowering'
                lower_time = current_time + 60
                bridge_unavailable += 60
            
            # If the bridge is lowering and we've reached the lower time
            if bridge_status == 'lowering' and current_time >= lower_time:
                bridge_status = 'lowered'
        
        return bridge_unavailable
    
    # Read input
    N = int(sys.stdin.readline().strip())
    arrival_times = [int(sys.stdin.readline().strip()) for _ in range(N)]
    
    # Simulate the bridge operations
    result = simulate_boats(arrival_times)
    
    # Print the result
    print(result)

if __name__ == "__main__":
    main()