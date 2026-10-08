import math

def find_detach_point(b, tx, ty):
    # Calculate the angle to the target
    phi_target = math.atan2(ty, tx)
    
    # Calculate the radius at the target angle
    r_target = math.sqrt(tx**2 + ty**2)
    
    # Calculate the angle phi where the spiral intersects the line to the target
    # We solve b * phi = r_target for phi
    phi = r_target / b
    
    # Calculate the coordinates of the point on the spiral
    x = b * phi * math.cos(phi)
    y = b * phi * math.sin(phi)
    
    return x, y

# Read input
import sys
input = sys.stdin.read
data = input().split()
b = float(data[0])
tx = float(data[1])
ty = float(data[2])

# Find the detach point
x, y = find_detach_point(b, tx, ty)

# Print the result
print(f"{x:.10f} {y:.10f}")