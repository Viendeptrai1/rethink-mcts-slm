def count_marked_cells(w1, h1, w2, h2):
    # Calculate the total area covered by the ship
    total_area = w1 * h1 + w2 * h2
    
    # Calculate the area of overlap between the two rectangles
    overlap_area = min(w1, w2) * min(h1, h2)
    
    # Calculate the effective area that needs to be marked
    marked_area = 4 * (w1 + w2 - min(w1, w2)) + 4 * (h1 + h2 - min(h1, h2))
    
    return marked_area

# Read input values
w1, h1, w2, h2 = map(int, input().split())

# Output the result
print(count_marked_cells(w1, h1, w2, h2))