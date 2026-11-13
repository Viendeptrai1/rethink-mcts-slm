def turtle_drawing(h, w, n, board, commands):
    # Initialize the starting position and time
    x, y, time = 0, 0, 0
    
    # Directions mapping
    directions = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    
    # Function to check if the current position matches the target drawing
    def matches_drawing(x, y, time):
        if 0 <= x < h and 0 <= y < w:
            return board[x][y] == '#'
        return False
    
    # Simulate the commands
    for command in commands:
        direction, distance = command.split()
        dx, dy = directions[direction]
        distance = int(distance)
        
        for _ in range(distance):
            x += dx
            y += dy
            time += 1
            if matches_drawing(x, y, time):
                return time, time
    
    # If we finish all commands, check if the final position matches the drawing
    if matches_drawing(x, y, time):
        return time, time
    
    # If no match is found, return -1 -1
    return -1, -1

import sys
input = sys.stdin.read
data = input().splitlines()

# Read the dimensions and number of commands
h, w, n = map(int, data[0].split())

# Read the board
board = [data[i + 1] for i in range(h)]

# Read the commands
commands = [data[i + h + 1] for i in range(n)]

# Get the result
min_time, max_time = turtle_drawing(h, w, n, board, commands)

# Print the result
print(min_time, max_time)