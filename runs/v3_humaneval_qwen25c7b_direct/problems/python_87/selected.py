def get_row(lst, x):
    result = []
    for i, row in enumerate(lst):
        for j, value in enumerate(row[::-1]):
            if value == x:
                result.append((i, len(row) - 1 - j))
    return sorted(result)