import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    w1 = int(data[0])
    h1 = int(data[1])
    w2 = int(data[2])
    h2 = int(data[3])
    
    # Calculate the perimeter of the first rectangle
    perimeter1 = 2 * (w1 + h1)
    
    # Calculate the perimeter of the second rectangle
    perimeter2 = 2 * (w2 + h2)
    
    # Subtract the shared side between the two rectangles
    shared_side = min(w1, w2)
    
    # Calculate the total perimeter of the ship
    total_perimeter = perimeter1 + perimeter2 - 2 * shared_side
    
    # Calculate the number of corner cells
    corner_cells = 4
    
    # Calculate the number of cells to be marked
    marked_cells = total_perimeter + corner_cells
    
    print(marked_cells)

if __name__ == "__main__":
    main()