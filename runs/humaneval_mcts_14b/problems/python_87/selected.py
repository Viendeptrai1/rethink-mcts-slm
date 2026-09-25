def get_row(lst, x):
    coordinates = []
    for row_index, row in enumerate(lst):
        for col_index, value in enumerate(row):
            if value == x:
                coordinates.append((row_index, col_index))
    
    # Sort by row in ascending order, then by column in descending order within each row
    coordinates.sort(key=lambda coord: (coord[0], -coord[1]))
    
    return coordinates

# Example usage:
# print(get_row([
#   [1,2,3,4,5,6],
#   [1,2,3,4,1,6],
#   [1,2,3,4,5,1]
# ], 1))  # Output: [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]