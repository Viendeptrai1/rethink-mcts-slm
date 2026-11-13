def count_marked_cells(w1, h1, w2, h2):
    # Calculate the area of the first rectangle
    area_first = w1 * h1
    
    # Calculate the area of the second rectangle
    area_second = w2 * h2
    
    # Calculate the total area covered by the ship
    total_area = area_first + area_second
    
    # Calculate the perimeter of the ship
    # Each side of the first rectangle contributes to the perimeter except the shared side with the second rectangle
    # Each side of the second rectangle contributes to the perimeter except the shared side with the first rectangle
    # The shared side is counted twice, so we subtract it once
    perimeter = 2 * (w1 + h1 + w2 - 1)
    
    # The number of marked cells is the perimeter minus the total area of the ship
    marked_cells = perimeter - total_area
    
    return marked_cells

# Read input values
w1, h1, w2, h2 = map(int, input().split())

# Print the result
print(count_marked_cells(w1, h1, w2, h2))