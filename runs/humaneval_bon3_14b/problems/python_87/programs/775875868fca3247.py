def get_row(lst, x):
    coordinates = []
    for i, row in enumerate(lst):
        for j, value in enumerate(row):
            if value == x:
                coordinates.append((i, j))
    
    # Sort by row in ascending order, then by column in descending order
    coordinates.sort(key=lambda coord: (coord[0], -coord[1]))
    
    return coordinates

# Test cases
print(get_row([
  [1,2,3,4,5,6],
  [1,2,3,4,1,6],
  [1,2,3,4,5,1]
], 1))  # [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]

print(get_row([], 1))  # []

print(get_row([[], [1], [1, 2, 3]], 3))  # [(2, 2)]