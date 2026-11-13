def count_marked_cells(w1, h1, w2, h2):
    # Calculate the total area of the ship
    ship_area = w1 * h1 + w2 * h2
    
    # Calculate the area of the surrounding cells
    # Top and bottom rows
    top_bottom_area = (w1 - w2) * 2 + 4
    # Left and right columns
    left_right_area = (h1 - h2) * 2 + 4
    
    # Total marked cells
    marked_cells = ship_area + top_bottom_area + left_right_area
    
    return marked_cells

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    w1 = int(data[0])
    h1 = int(data[1])
    w2 = int(data[2])
    h2 = int(data[3])
    
    result = count_marked_cells(w1, h1, w2, h2)
    print(result)