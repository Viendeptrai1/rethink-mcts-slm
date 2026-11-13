def solve():
    import sys
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    # Read the initial dimensions and number of commands
    h, w, n = map(int, data[0].split())
    
    # Read the target drawing pattern
    target = [list(data[i + 1]) for i in range(h)]
    
    # Read the commands
    commands = [tuple(data[h + 1 + i].split()) for i in range(n)]
    for i in range(n):
        commands[i] = (commands[i][0], int(commands[i][1]))
    
    # Initialize the position of the marker
    x, y = 0, 0  # Start at the bottom left corner
    
    # Initialize the timestep
    timestep = 0
    
    # Function to check if the current board matches the target
    def matches_target():
        board = [['.' for _ in range(w)] for _ in range(h)]
        for i in range(h):
            for j in range(w):
                if target[i][j] == '#' and timestep >= visited[i][j]:
                    board[i][j] = '#'
        return board == target
    
    # Initialize visited matrix with -1
    visited = [[-1 for _ in range(w)] for _ in range(h)]
    
    # Process each command
    for direction, distance in commands:
        dx, dy = 0, 0
        if direction == 'up':
            dx = -1
        elif direction == 'down':
            dx = 1
        elif direction == 'left':
            dy = -1
        elif direction == 'right':
            dy = 1
        
        for _ in range(distance):
            x += dx
            y += dy
            timestep += 1
            visited[x][y] = timestep
    
    # Find the earliest and latest timestep
    min_timestep = float('inf')
    max_timestep = -1
    
    for i in range(h):
        for j in range(w):
            if visited[i][j] != -1:
                min_timestep = min(min_timestep, visited[i][j])
                max_timestep = max(max_timestep, visited[i][j])
    
    # Check if the drawing is possible
    if matches_target():
        print(min_timestep, max_timestep)
    else:
        print(-1, -1)