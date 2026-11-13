def get_row(lst, x):
    result = []
    for row_idx, row in enumerate(lst):
        for col_idx, value in enumerate(row):
            if value == x:
                result.append((row_idx, col_idx))
    
    # Sort by row ascending, then by column descending
    result.sort(key=lambda coord: (coord[0], -coord[1]))
    
    return result