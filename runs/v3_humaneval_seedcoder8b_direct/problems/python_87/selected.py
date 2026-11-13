def get_row(lst, x):
    result = []
    for i, row in enumerate(lst):
        for j, value in enumerate(row):
            if value == x:
                result.append((i, j))
    return sorted(result, key=lambda coord: (coord[0], -coord[1]))