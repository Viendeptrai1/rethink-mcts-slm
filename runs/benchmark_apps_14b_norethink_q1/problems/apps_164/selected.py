import math

def calculate_xw(y1, y2, yw, xb, yb, r):
    # Calculate the height of the goal
    goal_height = y2 - y1
    
    # Calculate the vertical distance from the ball to the wall
    vertical_distance = yw - yb
    
    # Calculate the horizontal distance from the ball to the wall
    horizontal_distance = xb
    
    # Calculate the angle of incidence using trigonometry
    angle_of_incidence = math.atan(vertical_distance / horizontal_distance)
    
    # Calculate the angle of reflection (same as angle of incidence)
    angle_of_reflection = angle_of_incidence
    
    # Calculate the horizontal distance from the wall to the goal
    horizontal_distance_to_goal = yw
    
    # Calculate the vertical distance from the wall to the goal
    vertical_distance_to_goal = (y1 + y2) / 2 - yw
    
    # Calculate the angle of the trajectory after reflection
    angle_after_reflection = math.atan(vertical_distance_to_goal / horizontal_distance_to_goal)
    
    # Check if the angle after reflection is within the goal range
    if angle_after_reflection < angle_of_reflection or angle_after_reflection > math.pi - angle_of_reflection:
        return -1
    
    # Calculate the x-coordinate of the point on the wall where the ball should hit
    xw = (yw - yb) * (horizontal_distance_to_goal / vertical_distance_to_goal)
    
    return xw

# Read input
input_data = input().split()
y1 = int(input_data[0])
y2 = int(input_data[1])
yw = int(input_data[2])
xb = int(input_data[3])
yb = int(input_data[4])
r = int(input_data[5])

# Calculate the result
result = calculate_xw(y1, y2, yw, xb, yb, r)

# Print the result
print(result)