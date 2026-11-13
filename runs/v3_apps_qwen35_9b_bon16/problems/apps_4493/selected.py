import sys

def solve():
    grid = []
    try:
        lines = sys.stdin.read().strip().split('\n')
        if not lines:
            return
        for line in lines:
            if line.strip():
                grid.append(list(map(int, line.split())))
    except Exception:
        return

    if len(grid) != 3 or any(len(row) != 3 for row in grid):
        print("No")
        return

    c = grid

    # Condition 1: c[i][j] - c[i][k] must equal c[l][j] - c[l][k] for all i, l, j, k
    # This is equivalent to: c[i][j] + c[l][k] == c[i][k] + c[l][j]
    # We can check this for all combinations of rows i, l and columns j, k
    for i in range(3):
        for l in range(3):
            for j in range(3):
                for k in range(3):
                    if c[i][j] + c[l][k] != c[i][k] + c[l][j]:
                        print("No")
                        return

    # If the condition holds, we can construct a valid set of a and b
    # Let a_1 = 0, then b_j = c[0][j]
    # Then a_i = c[i][0] - b_0 = c[i][0] - c[0][0]
    # Check if this reconstruction matches the entire grid
    a = [0] * 3
    b = [0] * 3
    a[0] = 0
    for j in range(3):
        b[j] = c[0][j]
    
    for i in range(3):
        a[i] = c[i][0] - b[0]
    
    valid = True
    for i in range(3):
        for j in range(3):
            if a[i] + b[j] != c[i][j]:
                valid = False
                break
        if not valid:
            break

    if valid:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()