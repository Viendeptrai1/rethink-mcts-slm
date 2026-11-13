def count_marked_cells(w1, h1, w2, h2):
    # Calculate the total area of the ship
    total_ship_area = w1 * h1 + w2 * h2
    
    # Calculate the number of cells that are part of the ship
    ship_cells = total_ship_area
    
    # Calculate the number of cells that are adjacent to the ship
    # Top and bottom borders of the first rectangle
    top_bottom_cells = w1 * 2
    
    # Left and right borders of the first rectangle
    left_right_cells_first = (h1 - 1) * 2
    
    # Left and right borders of the second rectangle
    left_right_cells_second = (h2 - 1) * 2
    
    # Total border cells of the first rectangle
    border_cells_first = top_bottom_cells + left_right_cells_first
    
    # Total border cells of the second rectangle
    border_cells_second = top_bottom_cells + left_right_cells_second
    
    # Total border cells of the ship
    border_cells_ship = border_cells_first + border_cells_second
    
    # Total cells to be marked
    marked_cells = border_cells_ship - ship_cells
    
    return marked_cells

# Read input
w1, h1, w2, h2 = map(int, input().split())

# Calculate and print the result
print(count_marked_cells(w1, h1, w2, h2))