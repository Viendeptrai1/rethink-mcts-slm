import math
import sys

def find_release_point(b, tx, ty):
    # Calculate the angle of the target relative to the origin
    theta_target = math.atan2(ty, tx)
    
    # Calculate the radius of the target on the spiral
    r_target = b * theta_target
    
    # Calculate the angle at which the avatar should release the spiral
    theta_release = theta_target + math.pi / 2
    
    # Calculate the radius at the release point
    r_release = b * theta_release
    
    # Convert the polar coordinates to Cartesian coordinates
    rx = r_release * math.cos(theta_release)
    ry = r_release * math.sin(theta_release)
    
    return rx, ry

# Read input from stdin
input_line = sys.stdin.readline().strip()
b, tx, ty = map(float, input_line.split())

# Find the release point
release_point = find_release_point(b, tx, ty)

# Print the result
print(f"{release_point[0]:.10f} {release_point[1]:.10f}")