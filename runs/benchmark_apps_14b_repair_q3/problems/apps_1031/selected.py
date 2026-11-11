import sys

def paint_cardiogram(n, a):
    total_length = sum(a)
    max_height = max(sum(a[:i+1]) for i in range(n))
    
    # Initialize the grid with spaces
    grid = [[' ' for _ in range(total_length)] for _ in range(max_height)]
    
    x, y = 0, 0
    for i in range(n):
        if i % 2 == 0:
            # Move up and right
            for j in range(a[i]):
                grid[y][x] = '/'
                x += 1
                y -= 1
        else:
            # Move down and right
            for j in range(a[i]):
                grid[y][x] = '\\'
                x += 1
                y += 1
    
    # Print the grid
    for row in grid:
        print(''.join(row))

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Paint the cardiogram
paint_cardiogram(n, a)