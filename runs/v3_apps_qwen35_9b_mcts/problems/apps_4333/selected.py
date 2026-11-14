import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    x1 = int(input_data[0])
    y1 = int(input_data[1])
    x2 = int(input_data[2])
    y2 = int(input_data[3])
    
    # Vector from (x1, y1) to (x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    
    # To go from (x2, y2) to (x3, y3) in counter-clockwise order,
    # we rotate the vector (dx, dy) by 90 degrees counter-clockwise.
    # Rotation of (a, b) by 90 degrees CCW is (-b, a).
    # So the vector from (x2, y2) to (x3, y3) is (-dy, dx).
    x3 = x2 - dy
    y3 = y2 + dx
    
    # To go from (x3, y3) to (x4, y4), we rotate the vector (-dy, dx) by 90 degrees CCW again.
    # Vector is now (-dy, dx). Rotated 90 CCW: (-dx, -dy).
    # Alternatively, (x4, y4) is (x1, y1) + rotated vector from (x1,y1) to (x2,y2) by 180 degrees? 
    # Simpler: (x4, y4) = (x3, y3) + (-dx, -dy)
    x4 = x3 - dx
    y4 = y3 - dy
    
    print(f"{x3} {y3} {x4} {y4}")

if __name__ == "__main__":
    solve()