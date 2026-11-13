def max_path_length(v1, v2, t, d):
    # Calculate the total speed change needed
    total_speed_change = v2 - v1
    
    # Calculate the maximum speed change possible within t seconds
    max_possible_change = d * (t - 1)
    
    # If the total speed change needed is within the max possible change,
    # we can achieve it by distributing the change evenly
    if abs(total_speed_change) <= max_possible_change:
        # Calculate the average speed
        avg_speed = (v1 + v2) / 2
        # The total distance is the average speed multiplied by time
        return avg_speed * t
    else:
        # If the total speed change needed exceeds the max possible change,
        # we need to distribute the change as evenly as possible
        # Calculate the number of seconds where we can change speed by d
        full_changes = max_possible_change // d
        # Calculate the remaining change
        remaining_change = max_possible_change % d
        
        # Calculate the average speed for the full changeable periods
        avg_speed_full = (v1 + v2) / 2
        
        # Calculate the speed at the start of the remaining period
        if total_speed_change > 0:
            speed_remaining = avg_speed_full + (remaining_change / 2)
        else:
            speed_remaining = avg_speed_full - (remaining_change / 2)
        
        # Calculate the total distance
        distance_full = avg_speed_full * full_changes
        distance_remaining = speed_remaining * (t - full_changes)
        
        return distance_full + distance_remaining

# Read input
v1, v2 = map(int, input().split())
t, d = map(int, input().split())

# Calculate and print the result
result = max_path_length(v1, v2, t, d)
print(int(result))