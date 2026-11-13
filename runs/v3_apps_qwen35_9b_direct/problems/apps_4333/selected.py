import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    x1 = int(input_data[0])
    y1 = int(input_data[1])
    x2 = int(input_data[2])
    y2 = int(input_data[3])
    
    # Vector from P1 to P2
    dx = x2 - x1
    dy = y2 - y1
    
    # To get P3 in counter-clockwise order, rotate vector (dx, dy) by 90 degrees counter-clockwise
    # Rotation: (x, y) -> (-y, x)
    dx3 = -dy
    dy3 = dx
    
    x3 = x2 + dx3
    y3 = y2 + dy3
    
    # Vector from P2 to P3 is (dx3, dy3)
    # To get P4, we can go from P3 by rotating the vector (dx3, dy3) by 90 degrees counter-clockwise again? 
    # Actually, simpler: P4 = P1 + (dx3, dy3) because P1->P2 is (dx,dy) and P1->P4 should be the rotated version of P1->P2?
    # Let's re-verify with geometry.
    # P1 -> P2 is vector V.
    # P2 -> P3 is vector V rotated 90 deg CCW.
    # P3 -> P4 is vector V rotated 180 deg (which is -V).
    # P4 -> P1 is vector V rotated 270 deg (which is -V rotated 90).
    
    # So P3 = P2 + (-dy, dx)
    # P4 = P3 + (-dx, -dy) = P2 + (-dy, dx) + (-dx, -dy)
    # Alternatively, P4 = P1 + (-dy, dx)
    
    x4 = x1 + dx3
    y4 = y1 + dy3
    
    print(f"{x3} {y3} {x4} {y4}")

if __name__ == "__main__":
    solve()