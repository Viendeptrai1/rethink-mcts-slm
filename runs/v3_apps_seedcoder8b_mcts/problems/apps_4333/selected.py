def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    x1, y1 = int(data[0]), int(data[1])
    x2, y2 = int(data[2]), int(data[3])
    
    # Calculate the vector from (x1, y1) to (x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    
    # The square's vertices are in counter-clockwise order
    # To find (x3, y3), move (-dy, dx) from (x2, y2)
    x3 = x2 - dy
    y3 = y2 + dx
    
    # To find (x4, y4), move (dy, -dx) from (x1, y1)
    x4 = x1 - dy
    y4 = y1 + dx
    
    # Print the result
    print(x3, y3, x4, y4)

if __name__ == "__main__":
    main()