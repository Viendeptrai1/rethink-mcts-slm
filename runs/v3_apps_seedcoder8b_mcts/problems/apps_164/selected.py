import sys
import math

def find_robowallace_aiming_point(y1, y2, yw, xb, yb, r):
    # Calculate the time it takes for the ball to reach the wall
    if yw <= yb:
        return -1  # Invalid input as yw should be greater than yb

    # Calculate the time to reach the wall yw
    time_to_wall = (yw - yb) / math.sqrt(1)  # Since the ball moves in a straight line

    # Calculate the x-coordinate of the wall yw
    xw = xb + time_to_wall

    # Calculate the y-coordinate of the ball when it hits the wall
    y_wall = yw

    # Calculate the time it takes for the ball to bounce back
    time_to_bounce = (yw - yb) / math.sqrt(1)

    # Calculate the x-coordinate of the bounce point
    x_bounce = xb + 2 * time_to_bounce

    # Check if the bounce point is within the goal boundaries
    if y1 <= y_wall <= y2:
        return xw
    else:
        return -1

def main():
    input_data = sys.stdin.read().strip()
    y1, y2, yw, xb, yb, r = map(int, input_data.split())
    result = find_robowallace_aiming_point(y1, y2, yw, xb, yb, r)
    if result == -1:
        print(result)
    else:
        print(f"{result:.12f}")

if __name__ == "__main__":
    main()