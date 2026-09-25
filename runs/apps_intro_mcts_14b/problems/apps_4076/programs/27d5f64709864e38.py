import sys
import math

def calculate_distance(A, B, H, M):
    # Calculate the angle of the hour hand
    hour_angle = (30 * H) + (0.5 * M)
    
    # Calculate the angle of the minute hand
    minute_angle = 6 * M
    
    # Convert angles to radians
    hour_angle_rad = math.radians(hour_angle)
    minute_angle_rad = math.radians(minute_angle)
    
    # Calculate the distance using the law of cosines
    distance = math.sqrt(A**2 + B**2 - 2 * A * B * math.cos(minute_angle_rad - hour_angle_rad))
    
    return distance

# Read input from standard input
input_data = sys.stdin.read().strip().split()
A = int(input_data[0])
B = int(input_data[1])
H = int(input_data[2])
M = int(input_data[3])

# Calculate the distance
distance = calculate_distance(A, B, H, M)

# Print the result with high precision
print(f"{distance:.20f}")