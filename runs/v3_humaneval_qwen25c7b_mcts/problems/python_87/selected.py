def get_row(lst, x):
    indices = []
    for i, row in enumerate(lst):
        for j, value in enumerate(row):
            if value == x:
                indices.append((i, j))
    indices.sort(key=lambda item: (item[0], -item[1]))
    return indices