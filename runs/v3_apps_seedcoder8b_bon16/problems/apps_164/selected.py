import math

def find_robowallace_aim(y1, y2, yw, xb, yb, r):
    # Calculate the length of the hypotenuse formed by the ball's initial position and the wall
    dx = yw - xb
    dy = yb - (yw - yb)
    d = math.sqrt(dx * dx + dy * dy)

    # Calculate the initial angle of the ball's trajectory
    theta = math.atan2(dy, dx)

    # Calculate the time for the ball to hit the wall
    if d < 2 * r:
        return -1  # The ball touches the wall before reaching the goal
    time_to_wall = (d - 2 * r) / (2 * math.sqrt(dx * dx + (yb - yw) * (yb - yw)))

    # Calculate the ball's position when it hits the wall
    xw = xb + time_to_wall * math.cos(theta)
    yw_wall = yw - time_to_wall * math.sin(theta)

    # Calculate the reflection of the ball's trajectory
    dx_reflect = -dx
    dy_reflect = dy
    d_reflect = math.sqrt(dx_reflect * dx_reflect + dy_reflect * dy_reflect)

    # Calculate the angle of the reflected trajectory
    theta_reflect = math.atan2(dy_reflect, dx_reflect)

    # Calculate the time for the ball to hit the goal after reflection
    if (yw_wall < y1 or yw_wall > y2) or d_reflect < 2 * r:
        return -1  # The ball does not hit the goal after reflection
    time_to_goal = d_reflect / (2 * math.sqrt(dx_reflect * dx_reflect + (yw - yw_wall) * (yw - yw_wall)))

    # Calculate the ball's position when it hits the goal
    xw_goal = xw + time_to_goal * math.cos(theta_reflect)
    yw_goal = yw_wall + time_to_goal * math.sin(theta_reflect)

    # Check if the ball crosses the goal line between (0, y1) and (0, y2)
    if 0 <= xw_goal <= xb and y1 <= yw_goal <= y2:
        return xw
    else:
        return -1

# Read input values
y1, y2, yw, xb, yb, r = map(int, input().split())

# Get the result and print it
result = find_robowallace_aim(y1, y2, yw, xb, yb, r)
print(f"{result:.12f}" if result != -1 else "-1")