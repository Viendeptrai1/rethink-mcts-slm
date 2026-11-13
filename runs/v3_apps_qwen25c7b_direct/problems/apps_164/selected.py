import sys

def find_wall_position(y1, y2, yw, xb, yb, r):
    # Calculate the slope of the line from the ball to the goal
    if xb == 0:
        return -1  # Ball is directly below the wall, cannot bounce off
    
    slope = (y2 - y1) / (xb * 2)
    
    # Calculate the intersection points of the line with the vertical lines
    x1 = (yb - y1) / slope
    x2 = (y2 - yb) / slope
    
    # Check if the intersection points are within the valid range
    if x1 > 0 and x1 < xb:
        return x1
    elif x2 > 0 and x2 < xb:
        return x2
    
    return -1

# Read input
input_data = sys.stdin.read().strip()
y1, y2, yw, xb, yb, r = map(int, input_data.split())

# Find the wall position
result = find_wall_position(y1, y2, yw, xb, yb, r)

# Print the result
print(result)