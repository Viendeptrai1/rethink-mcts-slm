import sys

def calculate_wall_position(y1, y2, yw, xb, yb, r):
    # Calculate the slope of the line from the ball to the goal
    slope = (yw - yb) / (yw - xb)
    
    # Calculate the y-intercept of the line
    intercept = yb - slope * xb
    
    # Calculate the x-coordinate where the line intersects the wall
    xw = (yw - y1) / slope
    
    # Check if the intersection point is within the bounds of the wall
    if y1 <= yw <= y2 and xw > xb:
        return xw
    else:
        return -1

# Read input from stdin
input_data = sys.stdin.read().strip()
y1, y2, yw, xb, yb, r = map(int, input_data.split())

# Calculate the wall position
result = calculate_wall_position(y1, y2, yw, xb, yb, r)

# Print the result
print(result)