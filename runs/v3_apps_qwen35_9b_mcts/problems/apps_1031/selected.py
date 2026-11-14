import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
    except StopIteration:
        return

    # Calculate coordinates
    # Points: (0, 0), (a1, a1), (a1+a2, a1-a2), ...
    # x_k = sum(a[0]...a[k-1])
    # y_k = sum((-1)^(i+1) * a[i]) for i from 0 to k-1
    
    points = []
    curr_x = 0
    curr_y = 0
    points.append((curr_x, curr_y))
    
    current_y_val = 0
    
    for i in range(n):
        val = a[i]
        # The problem says: (a1; a1), (a1+a2; a1-a2), ...
        # So the first segment goes UP by a1.
        # The sign alternates: +, -, +, -, ...
        # i=0: +a[0]
        # i=1: -a[1]
        # i=2: +a[2]
        sign = 1 if i % 2 == 0 else -1
        current_y_val += sign * val
        curr_x += val
        points.append((curr_x, current_y_val))

    # Determine grid bounds
    # We need to map y coordinates to rows.
    # Higher y -> Lower row index (standard screen coordinates)
    # But the problem asks to print max|y_i - y_j| lines.
    # Let's find min_y and max_y.
    
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    
    height = max_y - min_y + 1
    width = points[-1][0] + 1  # x goes from 0 to sum(a)
    
    # Initialize grid with spaces
    # grid[row][col]
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Map y to row: row = max_y - y
    # When y = max_y, row = 0
    # When y = min_y, row = height - 1
    
    # Draw lines
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        
        # Determine slope direction
        # If y2 > y1, we are going UP. In screen coords, row decreases.
        # If y2 < y1, we are going DOWN. In screen coords, row increases.
        
        # We need to draw a diagonal line.
        # Since x increases by a[i] and y changes by +/- a[i], it's always a 45 degree line.
        # Number of steps = a[i]
        step = a[i]
        
        # Direction in terms of row change
        # If y increases (y2 > y1), row decreases (row2 < row1)
        # If y decreases (y2 < y1), row increases (row2 > row1)
        
        dy = y2 - y1
        dr = -dy  # row change is opposite to y change
        
        # Start and end rows
        r1 = max_y - y1
        r2 = max_y - y2
        
        # We iterate from x1 to x2
        # For each x, we determine the row.
        # Since it's a straight diagonal, row changes by 1 for every 1 step in x.
        
        # Determine character
        # If y is increasing (dy > 0), we are going up-right -> '/'
        # If y is decreasing (dy < 0), we are going down-right -> '\'
        
        char = '/' if dy > 0 else '\\'
        
        # Fill the line
        # We can just iterate x from x1 to x2-1
        for k in range(step):
            x = x1 + k
            r = r1 + k * dr
            grid[r][x] = char

    # Print the grid
    for row in grid:
        print("".join(row))

if __name__ == '__main__':
    solve()