def calculate_unavailable_time(N, arrival_times):
    # Initialize the bridge state and unavailable time
    bridge_open_time = 0
    bridge_unavailable_time = 0
    
    # Iterate over each boat's arrival time
    for i in range(N):
        if i == 0:
            # First boat opens the bridge
            bridge_open_time = arrival_times[i] + 60
        else:
            # If the bridge is already open and enough time has passed to open it again
            if arrival_times[i] > bridge_open_time + 20:
                bridge_open_time = arrival_times[i] + 60
            else:
                bridge_open_time += 20

        # Calculate the time the bridge is unavailable during this boat's passage
        boat_start_time = max(arrival_times[i], bridge_open_time - 60)
        boat_end_time = boat_start_time + 20
        bridge_unavailable_time += boat_end_time - bridge_open_time + 60
        bridge_open_time += 20  # Increase the bridge open time by the boat's transit time

    return bridge_unavailable_time

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    # Read the number of boats
    N = int(data[0])
    
    # Read the arrival times
    arrival_times = list(map(int, data[1:N+1]))
    
    # Calculate the total unavailable time
    result = calculate_unavailable_time(N, arrival_times)
    
    # Print the result
    print(result)

if __name__ == "__main__":
    main()