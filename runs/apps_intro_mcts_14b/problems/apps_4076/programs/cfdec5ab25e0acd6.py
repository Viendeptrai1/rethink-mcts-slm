import sys
import math

def calculate_distance(A, B, H, M):
    # Convert hours and minutes to total minutes
    total_minutes = H * 60 + M
    
    # Calculate the angle of the hour hand in radians
    hour_angle = (total_minutes / 720) * 2 * math.pi
    
    # Calculate the angle of the minute hand in radians
    minute_angle = (M / 60) * 2 * math.pi
    
    # Calculate the difference in angles
    angle_difference = abs(hour_angle - minute_angle)
    
    # Use the Law of Cosines to find the distance between the endpoints
    distance = math.sqrt(A**2 + B**2 - 2 * A * B * math.cos(angle_difference))
    
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