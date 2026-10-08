import sys
import math

def find_aiming_point(y1, y2, yw, xb, yb, r):
    # Reflect the goal across the wall
    y1_reflected = 2 * yw - y1
    y2_reflected = 2 * yw - y2
    
    # Check if the ball can reach the reflected goal without hitting other walls or goalposts
    if yb + r >= y1_reflected or yb - r <= y2_reflected:
        return -1
    
    # Calculate the slope of the line from the ball to the reflected goal
    slope = (y2_reflected - yb) / (0 - xb)
    
    # Calculate the intersection of this line with the aiming wall
    xw = (yw - yb) / slope + xb
    
    # Check if the intersection point is within the valid range
    if xw <= xb or xw > 10**6:
        return -1
    
    return xw

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    y1 = int(data[0])
    y2 = int(data[1])
    yw = int(data[2])
    xb = int(data[3])
    yb = int(data[4])
    r = int(data[5])
    
    result = find_aiming_point(y1, y2, yw, xb, yb, r)
    if result == -1:
        print("-1")
    else:
        print(f"{result:.10f}")

if __name__ == "__main__":
    main()