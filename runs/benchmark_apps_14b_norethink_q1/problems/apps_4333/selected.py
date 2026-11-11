import sys

def main():
    import sys
    x1, y1, x2, y2 = map(int, sys.stdin.read().split())
    
    # Calculate the vector from (x1, y1) to (x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    
    # Calculate the perpendicular vector (dx, dy) -> (-dy, dx)
    dx_perp = -dy
    dy_perp = dx
    
    # Calculate (x3, y3) and (x4, y4)
    x3 = x2 + dx_perp
    y3 = y2 + dy_perp
    x4 = x1 + dx_perp
    y4 = y1 + dy_perp
    
    # Ensure the vertices are in counter-clockwise order
    if (x3 - x1) * (y4 - y1) - (y3 - y1) * (x4 - x1) < 0:
        x3, y3, x4, y4 = x4, y4, x3, y3
    
    print(x3, y3, x4, y4)

if __name__ == "__main__":
    main()