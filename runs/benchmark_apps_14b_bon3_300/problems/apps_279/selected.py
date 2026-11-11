import sys

def max_path_length(v1, v2, t, d):
    # Initialize the maximum length
    max_length = 0
    
    # Iterate over all possible speeds for each second
    for i in range(t):
        # Calculate the speed at the i-th second
        if i == 0:
            current_speed = v1
        elif i == t - 1:
            current_speed = v2
        else:
            current_speed = max(min(v1 + i * d, v2), v1)
        
        # Add the current speed to the total length
        max_length += current_speed
    
    return max_length

# Read input
input = sys.stdin.read
data = input().split()

v1 = int(data[0])
v2 = int(data[1])
t = int(data[2])
d = int(data[3])

# Calculate and print the maximum possible length of the path section
print(max_path_length(v1, v2, t, d))