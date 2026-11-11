def min_time_to_deliver_candies(n, m, candies):
    # Initialize the result list
    result = []
    
    # Simulate starting from each station
    for start_station in range(1, n + 1):
        total_time = 0
        current_station = start_station
        
        # Process each candy
        for a_i, b_i in candies:
            # Calculate the distance from current station to the candy's station
            distance_to_candy = abs(a_i - current_station)
            if distance_to_candy > n // 2:
                distance_to_candy = n - distance_to_candy
            
            # Move to the candy's station
            total_time += distance_to_candy
            
            # Calculate the distance from the candy's station to the destination
            distance_to_destination = abs(b_i - a_i)
            if distance_to_destination > n // 2:
                distance_to_destination = n - distance_to_destination
            
            # Move to the destination station
            total_time += distance_to_destination
            
            # Update the current station to the destination station
            current_station = b_i
        
        # Append the total time for this starting station
        result.append(total_time)
    
    return result

# Read input
n, m = map(int, input().split())
candies = [tuple(map(int, input().split())) for _ in range(m)]

# Get the result
result = min_time_to_deliver_candies(n, m, candies)

# Print the result
print(" ".join(map(str, result)))