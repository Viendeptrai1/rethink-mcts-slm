import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    matrix = []
    for _ in range(n):
        row = []
        for _ in range(m):
            row.append(int(next(iterator)))
        matrix.append(row)

    # We start with the full matrix and try to "unmirror" it as much as possible.
    # A matrix can be unmirrored if the bottom half is exactly the reverse of the top half.
    # If it can be unmirrored, we reduce the number of rows by half and repeat.
    # Otherwise, we stop and the current number of rows is the answer.

    current_rows = n
    while current_rows % 2 == 0:
        half = current_rows // 2
        # Check if the bottom half is the mirror of the top half
        is_mirror = True
        for i in range(half):
            # Row i from top should match row (current_rows - 1 - i) from bottom
            for j in range(m):
                if matrix[i][j] != matrix[current_rows - 1 - i][j]:
                    is_mirror = False
                    break
            if not is_mirror:
                break
        
        if is_mirror:
            # We can unmirror, so the original base matrix had 'half' rows
            current_rows = half
        else:
            # Cannot unmirror further
            break

    print(current_rows)

if __name__ == "__main__":
    solve()