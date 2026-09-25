import sys
import math

def calculate_distance(A, B, H, M):
    # Convert hours and minutes to total minutes
    total_minutes = H * 60 + M
    
    # Calculate the angle of the hour hand
    hour_angle = (total_minutes / 720) * 360
    
    # Calculate the angle of the minute hand
    minute_angle = (M / 60) * 360
    
    # Calculate the difference in angles
    angle_difference = abs(hour_angle - minute_angle)
    
    # Ensure the angle difference is the smaller angle
    if angle_difference > 180:
        angle_difference = 360 - angle_difference
    
    # Calculate the distance using the law of cosines
    distance = math.sqrt(A**2 + B**2 - 2 * A * B * math.cos(math.radians(angle_difference)))
    
    return distance

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    H = int(data[2])
    M = int(data[3])
    
    distance = calculate_distance(A, B, H, M)
    print(f"{distance:.20f}")

if __name__ == "__main__":
    main()