import sys

def main():
    # Read the input values from a single line
    input_values = sys.stdin.readline().split()
    
    # Convert the input values to integers
    w1 = int(input_values[0])
    h1 = int(input_values[1])
    w2 = int(input_values[2])
    h2 = int(input_values[3])
    
    # Calculate the number of cells to be marked
    # The ship is composed of two rectangles stacked vertically
    # The number of cells to be marked is calculated by considering the perimeter
    # of the ship and adding the cells around the ship.
    
    # The perimeter of the ship is the sum of the perimeters of both rectangles
    # minus the overlapping edges (which are counted twice).
    perimeter = 2 * (w1 + h1 + w2 + h2 - w2)
    
    # The number of cells to be marked is the perimeter plus the cells around the ship.
    # We need to add the cells around the ship carefully to avoid double-counting.
    
    # The number of cells to be marked is the perimeter plus the cells around the ship.
    # We need to add the cells around the ship carefully to avoid double-counting.
    marked_cells = perimeter + 2 * (w1 + h1 + w2 + h2 - 2 * w2)
    
    print(marked_cells)

if __name__ == "__main__":
    main()