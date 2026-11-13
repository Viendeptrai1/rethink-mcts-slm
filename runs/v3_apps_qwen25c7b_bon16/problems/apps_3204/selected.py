import sys

def main():
    # Read input from stdin
    input = sys.stdin.read
    data = input().split()
    
    # Number of boats
    N = int(data[0])
    
    # Arrival times of boats
    arrival_times = [int(data[i]) for i in range(1, N+1)]
    
    # Initialize variables
    current_time = 0
    bridge_up_to = 0
    total_unavailable_time = 0
    
    # Process each boat
    for i in range(N):
        boat_arrival = arrival_times[i]
        
        # If the bridge is down, raise it
        if bridge_up_to <= current_time:
            bridge_up_to = current_time + 60
        
        # Calculate the time until the boat can enter the bridge
        wait_time = max(0, boat_arrival - current_time)
        current_time += wait_time
        
        # If the bridge is up but not yet occupied, let the boat enter
        if current_time < bridge_up_to:
            current_time += 20
        else:
            bridge_up_to += 60
            current_time += 20
        
        # Update the total unavailable time
        total_unavailable_time += (bridge_up_to - current_time) if bridge_up_to > current_time else 0
    
    # Print the result
    print(total_unavailable_time)

if __name__ == "__main__":
    main()