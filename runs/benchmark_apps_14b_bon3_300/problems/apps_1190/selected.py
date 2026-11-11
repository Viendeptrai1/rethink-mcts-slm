import sys

def main():
    import sys
    w1 = int(sys.stdin.readline())
    h1 = int(sys.stdin.readline())
    w2 = int(sys.stdin.readline())
    h2 = int(sys.stdin.readline())
    
    # Calculate the total area covered by the ship
    total_area = w1 * h1 + w2 * h2
    
    # Calculate the perimeter of the ship
    # The ship is composed of two rectangles stacked vertically
    # The perimeter is calculated as follows:
    # - Top and bottom edges: w1 + w2
    # - Left and right edges: h1 + h2
    # However, we need to subtract the overlapping edges (w2)
    perimeter = 2 * (w1 + h1 + h2) - w2
    
    # The number of cells to be marked is the perimeter minus the width of the overlapping edge
    marked_cells = perimeter - w2
    
    print(marked_cells)

if __name__ == "__main__":
    main()