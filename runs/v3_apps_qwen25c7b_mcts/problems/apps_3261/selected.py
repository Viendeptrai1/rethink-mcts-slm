def is_white(row, col):
    return any((row >> i) & 1 == (col >> i) & 1 for i in range(32)) and not (row == 0 and col == 0)

def count_grey_cells(R, C, K):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    current_direction = 0
    x, y = 0, 0
    grey_count = 0
    
    for _ in range(K):
        if is_white(x, y):
            grey_count += 1
        dx, dy = directions[current_direction]
        nx, ny = x + dx, y + dy
        
        if nx < 0 or nx >= R or ny < 0 or ny >= C:
            current_direction = (current_direction + 1) % 4
            dx, dy = directions[current_direction]
            nx, ny = x + dx, y + dy
        
        x, y = nx, ny
    
    return grey_count

# Read input
import sys
input = sys.stdin.read
data = input().split()

R = int(data[0])
C = int(data[1])
K = int(data[2])

# Calculate and print the result
print(count_grey_cells(R, C, K))