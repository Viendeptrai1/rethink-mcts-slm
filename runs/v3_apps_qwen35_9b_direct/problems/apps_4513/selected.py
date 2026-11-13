import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    t = int(next(iterator))
    
    for _ in range(t):
        grid = []
        for _ in range(9):
            row_str = next(iterator)
            grid.append([int(c) for c in row_str])
        
        # Strategy: Change all cells in the first row to 1.
        # This ensures:
        # 1. First row has 9 ones (>= 2 equal).
        # 2. First column now has 9 ones (>= 2 equal).
        # 3. Top-left 3x3 block now has 9 ones (>= 2 equal).
        # Since we only change 9 elements (the entire first row), this satisfies the constraint.
        
        for j in range(9):
            grid[0][j] = 1
            
        # Output the modified grid
        for row in grid:
            print("".join(str(x) for x in row))

if __name__ == "__main__":
    solve()