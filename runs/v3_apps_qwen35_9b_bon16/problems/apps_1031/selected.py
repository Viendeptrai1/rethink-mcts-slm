import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(x) for x in input_data[1:n+1]]

    # Calculate coordinates
    points_x = [0]
    points_y = [0]
    curr_y = 0
    for i in range(n):
        curr_y += a[i] if i % 2 == 0 else -a[i]
        points_x.append(points_x[-1] + a[i])
        points_y.append(curr_y)

    max_y = max(points_y)
    min_y = min(points_y)
    height = max_y - min_y

    # Determine grid dimensions
    width = points_x[-1]
    # We need to print height + 1 lines to cover from min_y to max_y
    lines_count = height + 1

    # Initialize grid with spaces
    grid = [[' ' for _ in range(width + 1)] for _ in range(lines_count)]

    # Map coordinates to grid
    # y in points goes from 0 to height, but actual values range from min_y to max_y
    # We want row 0 to correspond to y = max_y
    # So row r corresponds to y = max_y - r
    def get_row(y):
        return max_y - y

    # Draw the polyline
    for i in range(n):
        x1, y1 = points_x[i], points_y[i]
        x2, y2 = points_x[i+1], points_y[i+1]
        
        # Determine the segment type
        if y2 > y1:
            # Upward segment: /
            # x increases, y increases
            step_x = 1
            step_y = a[i] // step_x
            # We draw from x1 to x2-1
            for x in range(x1, x2):
                r = get_row(y1 + (x - x1))
                c = x
                grid[r][c] = '/'
        else:
            # Downward segment: \
            # x increases, y decreases
            step_x = 1
            step_y = a[i] // step_x
            for x in range(x1, x2):
                r = get_row(y1 + (x - x1))
                c = x
                grid[r][c] = '\\'

    # Print the grid
    for r in range(lines_count):
        print("".join(grid[r]))

if __name__ == "__main__":
    solve()