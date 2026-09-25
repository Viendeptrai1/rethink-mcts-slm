import sys
import math

def calculate_distance(A, B, H, M):
    # Calculate the angle of the hour hand from the 12 o'clock position
    hour_angle = (H % 12) * 30 + (M / 60) * 30
    
    # Calculate the angle of the minute hand from the 12 o'clock position
    minute_angle = M * 6
    
    # Calculate the difference in angles
    angle_difference = abs(hour_angle - minute_angle)
    
    # Ensure the angle difference is the smaller angle between the two possible angles
    if angle_difference > 180:
        angle_difference = 360 - angle_difference
    
    # Convert the angle difference to radians
    angle_radians = math.radians(angle_difference)
    
    # Calculate the distance using the law of cosines
    distance = math.sqrt(A**2 + B**2 - 2 * A * B * math.cos(angle_radians))
    
    return distance

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    A = int(data[0])
    B = int(data[1])
    H = int(data[2])
    M = int(data[3])
    
    result = calculate_distance(A, B, H, M)
    print(f"{result:.20f}")

if __name__ == "__main__":
    main()