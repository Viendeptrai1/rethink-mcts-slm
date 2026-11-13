def max_path_length(v1, v2, t, d):
    # Initialize the total distance to zero
    total_distance = 0
    
    # Calculate the initial speed
    current_speed = v1
    
    for i in range(t):
        # Calculate the distance covered in this second
        total_distance += current_speed
        
        # Determine the next speed
        if i < t - 1:
            # Calculate the potential next speed
            if current_speed < v2:
                next_speed = min(current_speed + d, v2)
            else:
                next_speed = max(current_speed - d, v2)
            
            # Update the current speed for the next iteration
            current_speed = next_speed
    
    return total_distance

# Read input
v1, v2 = map(int, input().split())
t, d = map(int, input().split())

# Calculate and print the result
print(max_path_length(v1, v2, t, d))