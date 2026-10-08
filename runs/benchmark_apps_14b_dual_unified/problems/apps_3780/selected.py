import math

def calculate_time(x1, y1, x2, y2, vmax, t, vx1, vy1, vx2, vy2):
    # Calculate the distance to travel
    total_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # Calculate the effective velocity for the first t seconds
    effective_vx1 = min(vmax, math.sqrt((vx1 + vmax)**2 + vy1**2))
    effective_vy1 = min(vmax, math.sqrt(vx1**2 + (vy1 + vmax)**2))
    
    # Calculate the effective velocity for the remaining time
    effective_vx2 = min(vmax, math.sqrt((vx2 + vmax)**2 + vy2**2))
    effective_vy2 = min(vmax, math.sqrt(vx2**2 + (vy2 + vmax)**2))
    
    # Calculate the distance covered in the first t seconds
    distance_covered1 = effective_vx1 * t
    
    # Calculate the remaining distance to cover
    remaining_distance = total_distance - distance_covered1
    
    # Calculate the time to cover the remaining distance
    time_remaining = remaining_distance / effective_vx2
    
    # Total time is the sum of time for the first t seconds and the remaining time
    total_time = t + time_remaining
    
    return total_time

# Read input
import sys
input = sys.stdin.read
data = input().split()

x1 = int(data[0])
y1 = int(data[1])
x2 = int(data[2])
y2 = int(data[3])
vmax = int(data[4])
t = int(data[5])
vx1 = int(data[6])
vy1 = int(data[7])
vx2 = int(data[8])
vy2 = int(data[9])

# Calculate and print the result
result = calculate_time(x1, y1, x2, y2, vmax, t, vx1, vy1, vx2, vy2)
print(result)