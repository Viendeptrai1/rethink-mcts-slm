def count_marked_cells(w1, h1, w2, h2):
    # Calculate the area of each rectangle
    area1 = w1 * h1
    area2 = w2 * h2

    # Total area of the ship
    total_ship_area = area1 + area2

    # Calculate the perimeter of the ship
    perimeter_ship = 2 * (w1 + h1 + w2 + h2)

    # Subtract the ship area from the perimeter to get the number of marked cells
    marked_cells = perimeter_ship - total_ship_area

    return marked_cells

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    w1, h1, w2, h2 = map(int, data)
    print(count_marked_cells(w1, h1, w2, h2))