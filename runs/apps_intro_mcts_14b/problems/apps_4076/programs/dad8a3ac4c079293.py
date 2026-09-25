import sys
import math

def calculate_distance(A, B, H, M):
    # Calculate the angle of the hour hand
    hour_angle = (H % 12) * 30 + (M / 60) * 30
    
    # Calculate the angle of the minute hand
    minute_angle = M * 6
    
    # Convert angles to radians
    hour_angle_rad = math.radians(hour_angle)
    minute_angle_rad = math.radians(minute_angle)
    
    # Calculate the Cartesian coordinates of the endpoints
    x_hour = A * math.cos(hour_angle_rad)
    y_hour = A * math.sin(hour_angle_rad)
    
    x_minute = B * math.cos(minute_angle_rad)
    y_minute = B * math.sin(minute_angle_rad)
    
    # Calculate the distance between the two points
    distance = math.sqrt((x_hour - x_minute) ** 2 + (y_hour - y_minute) ** 2)
    
    return distance

# Read input
input_data = sys.stdin.read().strip()
A, B, H, M = map(int, input_data.split())

# Calculate and print the distance
distance = calculate_distance(A, B, H, M)
print(f"{distance:.20f}")