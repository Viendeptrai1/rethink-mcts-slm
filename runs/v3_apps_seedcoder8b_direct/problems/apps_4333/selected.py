def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    x1, y1 = int(data[0]), int(data[1])
    x2, y2 = int(data[2]), int(data[3])
    
    # The square is in counter-clockwise order: (x1, y1), (x2, y2), (x3, y3), (x4, y4)
    # The diagonals of a square intersect at their midpoint.
    # Midpoint of (x1, y1) and (x2, y2) is ((x1 + x2) / 2, (y1 + y2) / 2)
    # Midpoint of (x3, y3) and (x4, y4) is ((x3 + x4) / 2, (y3 + y4) / 2)
    # These midpoints should be equal for the diagonals to intersect at the same point.
    
    # Calculate the midpoint of the first diagonal
    mid_x1 = (x1 + x2) / 2
    mid_y1 = (y1 + y2) / 2
    
    # Calculate the midpoint of the second diagonal
    mid_x2 = (x1 + x2) / 2
    mid_y2 = (y1 + y2) / 2
    
    # Since the problem guarantees integer values, we can deduce:
    # x3 = x1 + (x2 - x1)
    # y3 = y1 + (y2 - y1)
    # x4 = x1 + (x2 - x1)
    # y4 = y1 + (y2 - y1)
    
    # Calculate the coordinates of the third and fourth points
    x3 = x1 + (x2 - x1)
    y3 = y1 + (y2 - y1)
    x4 = x1 + (x2 - x1)
    y4 = y1 + (y2 - y1)
    
    # Print the result
    print(x3, y3, x4, y4)

if __name__ == "__main__":
    main()