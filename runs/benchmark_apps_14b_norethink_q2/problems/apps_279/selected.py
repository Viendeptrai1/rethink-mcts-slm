import sys

def max_path_length(v1, v2, t, d):
    # Initialize the current speed and the total distance
    current_speed = v1
    total_distance = 0
    
    # Iterate over each second except the last one
    for i in range(t - 1):
        # Calculate the next speed, ensuring it stays within the bounds
        if v2 > current_speed:
            next_speed = min(current_speed + d, v2)
        else:
            next_speed = max(current_speed - d, v2)
        
        # Add the distance covered in this second to the total distance
        total_distance += current_speed
        
        # Update the current speed for the next iteration
        current_speed = next_speed
    
    # Add the distance covered in the last second
    total_distance += current_speed
    
    return total_distance

# Read input from standard input
input = sys.stdin.read
data = input().split()

v1 = int(data[0])
v2 = int(data[1])
t = int(data[2])
d = int(data[3])

# Calculate and print the maximum possible length of the path section
print(max_path_length(v1, v2, t, d))