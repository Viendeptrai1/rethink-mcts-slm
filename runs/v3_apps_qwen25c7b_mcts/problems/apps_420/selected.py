def min_rows_for_mirror(a):
    seen = set()
    for row in a:
        row_tuple = tuple(row)
        reversed_row_tuple = tuple(reversed(row))
        if reversed_row_tuple not in seen:
            seen.add(row_tuple)
    return len(seen)

# Example usage:
n, m = map(int, input().split())
matrix_a = [tuple(map(int, input().split())) for _ in range(n)]
print(min_rows_for_mirror(matrix_a))