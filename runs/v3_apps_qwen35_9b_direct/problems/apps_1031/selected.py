import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = []
    idx = 1
    for _ in range(n):
        a.append(int(input_data[idx]))
        idx += 1

    # Calculate points
    # Point k (0-indexed) corresponds to sum of a[0]...a[k] for x
    # and alternating sum for y
    points = []
    x = 0
    y = 0
    points.append((x, y))
    
    current_y = 0
    for i in range(n):
        x += a[i]
        if i % 2 == 0:
            current_y += a[i]
        else:
            current_y -= a[i]
        points.append((x, current_y))

    # Determine height (max |y|)
    max_y = 0
    min_y = 0
    for _, y_val in points:
        if y_val > max_y:
            max_y = y_val
        if y_val < min_y:
            min_y = y_val
    
    height = max_y - min_y
    if height == 0:
        height = 1  # At least one line if points exist

    # Determine width
    width = points[-1][0]

    # Create grid: rows from top (min_y) to bottom (max_y)
    # We will map y coordinate to row index
    # Row 0 corresponds to y = min_y
    # Row height-1 corresponds to y = max_y
    
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Fill the polyline
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        
        # Determine direction
        if y2 > y1:
            # Upward: /
            for k in range(1, x2 - x1 + 1):
                # Map y1 to row index
                row1 = y1 - min_y
                row2 = y2 - min_y
                # The segment goes from (x1, y1) to (x2, y2)
                # At step k, x = x1 + k, y = y1 + k (since slope is 1)
                y_curr = y1 + k
                row_curr = y_curr - min_y
                if 0 <= row_curr < height:
                    grid[row_curr][x1 + k] = '/'
        else:
            # Downward: \
            for k in range(1, x2 - x1 + 1):
                row1 = y1 - min_y
                row2 = y2 - min_y
                # The segment goes from (x1, y1) to (x2, y2)
                # At step k, x = x1 + k, y = y1 - k (since slope is -1)
                y_curr = y1 - k
                row_curr = y_curr - min_y
                if 0 <= row_curr < height:
                    grid[row_curr][x1 + k] = '\\'

    # Print the grid
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    solve()