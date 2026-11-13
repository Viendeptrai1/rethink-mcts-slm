import sys

def find_aim_point(y1, y2, yw, xb, yb, r):
    # Check if the target wall is vertical and within the valid range
    if yw <= y1 or yw >= y2:
        return -1
    
    # Calculate the slope of the line from the ball to the target wall
    if xb == 0:
        return -1  # Avoid division by zero if the ball is directly below the wall
    
    slope = (yw - yb) / (yw - xb)
    
    # Calculate the y-intercept of the line from the ball to the target wall
    intercept = yb - slope * xb
    
    # Calculate the x-coordinate where the ball would hit the wall
    x_hit_wall = yw
    
    # Calculate the y-coordinate where the ball would bounce back
    y_bounce_back = slope * x_hit_wall + intercept
    
    # Check if the bouncing point is within the goalposts
    if y1 <= y_bounce_back <= y2:
        return x_hit_wall
    
    return -1

# Read input from standard input
input_data = sys.stdin.read()
y1, y2, yw, xb, yb, r = map(int, input_data.split())

# Find the aiming point
result = find_aim_point(y1, y2, yw, xb, yb, r)

# Print the result
print(result)