import sys

def max_path_length(v1, v2, t, d):
    # Initialize the maximum distance
    max_distance = 0
    
    # Try all possible sequences of speeds
    for i in range(t):
        # Calculate the speed at each second
        speeds = [v1]
        for j in range(1, t):
            if j <= i:
                new_speed = min(speeds[-1] + d, v2)
            else:
                new_speed = max(speeds[-1] - d, v1)
            speeds.append(new_speed)
        
        # Check if the last speed is v2
        if speeds[-1] == v2:
            # Calculate the distance for this sequence
            distance = sum(speeds)
            # Update the maximum distance
            max_distance = max(max_distance, distance)
    
    return max_distance

# Read input
input = sys.stdin.read
data = input().split()

v1 = int(data[0])
v2 = int(data[1])
t = int(data[2])
d = int(data[3])

# Calculate and print the maximum possible length of the path section
print(max_path_length(v1, v2, t, d))