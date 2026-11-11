import sys
import math

def main():
    y1, y2, yw, xb, yb, r = map(int, sys.stdin.readline().split())
    
    # Reflect the goal across the wall
    y1_reflected = 2 * yw - y2
    y2_reflected = 2 * yw - y1
    
    # Calculate the slope of the line from the ball to the reflected goal
    if xb == 0:
        print(-1)
        return
    
    slope = (y1_reflected - yb) / (0 - xb)
    
    # Calculate the y-intercept of the line
    intercept = yb - slope * xb
    
    # Calculate the x-coordinate where the line intersects the wall
    xw = (yw - intercept) / slope
    
    # Check if the intersection point is within the valid range
    if xw > xb and y1 <= yw - r and yw + r <= y2:
        print(xw)
    else:
        print(-1)

if __name__ == "__main__":
    main()