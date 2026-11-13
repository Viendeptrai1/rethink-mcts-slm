def calculate_marked_cells(w1, h1, w2, h2):
    # Calculate the total area of the ship
    total_area = w1 * h1 + w2 * h2
    
    # Calculate the overlap area
    overlap_width = w1 - w2
    overlap_height = h2
    overlap_area = overlap_width * overlap_height
    
    # Calculate the total perimeter of the ship
    total_perimeter = 2 * (w1 + h1) + 2 * (w2 + h2)
    
    # Calculate the number of cells to be marked
    marked_cells = total_perimeter - 2 * overlap_area
    
    return marked_cells

# Read input
w1, h1, w2, h2 = map(int, input().split())

# Calculate and print the result
result = calculate_marked_cells(w1, h1, w2, h2)
print(result)