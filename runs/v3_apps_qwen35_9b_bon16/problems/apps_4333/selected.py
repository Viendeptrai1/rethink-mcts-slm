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
    
    # To get the next vertex (x3, y3) in counter-clockwise order,
    # we rotate the vector (dx, dy) by 90 degrees counter-clockwise.
    # Rotation formula for 90 degrees CCW: (a, b) -> (-b, a)
    dx3 = -dy
    dy3 = dx
    
    x3 = x2 + dx3
    y3 = y2 + dy3
    
    # Vector from (x2, y2) to (x3, y3) is (dx3, dy3)
    # Now rotate this vector by 90 degrees CCW to get vector from (x3, y3) to (x4, y4)
    dx4 = -dy3
    dy4 = dx3
    
    x4 = x3 + dx4
    y4 = y3 + dy4
    
    print(f"{x3} {y3} {x4} {y4}")

if __name__ == "__main__":
    solve()