import sys

def find_missing_vertices(x1, y1, x2, y2):
    # Calculate the vector from (x1, y1) to (x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    
    # Rotate the vector 90 degrees counterclockwise to get the vector to the next vertex
    dx_rotated = -dy
    dy_rotated = dx
    
    # Calculate (x3, y3) by adding the rotated vector to (x2, y2)
    x3 = x2 + dx_rotated
    y3 = y2 + dy_rotated
    
    # Calculate (x4, y4) by adding the rotated vector to (x1, y1)
    x4 = x1 + dx_rotated
    y4 = y1 + dy_rotated
    
    return x3, y3, x4, y4

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    x1 = int(data[0])
    y1 = int(data[1])
    x2 = int(data[2])
    y2 = int(data[3])
    
    x3, y3, x4, y4 = find_missing_vertices(x1, y1, x2, y2)
    
    print(x3, y3, x4, y4)

if __name__ == "__main__":
    main()