def find_marker_drying_times():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    h, w, n = map(int, data[0].split())
    target_board = [list(data[i + 1]) for i in range(h)]
    commands = [data[i + h + 1].split() for i in range(n)]
    
    # Directions mapping
    direction_map = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    
    # Initialize the current position and time
    x, y = 0, 0
    time = 0
    
    # Function to check if the current drawing matches the target
    def matches_target():
        for i in range(h):
            for j in range(w):
                if target_board[i][j] == '#' and drawing_board[i][j] == '.':
                    return False
                if target_board[i][j] == '.' and drawing_board[i][j] == '#':
                    return False
        return True
    
    # Initialize the drawing board
    drawing_board = [['.' for _ in range(w)] for _ in range(h)]
    
    # Track the earliest and latest drying times
    earliest_drying_time = float('inf')
    latest_drying_time = -1
    
    # Simulate the commands
    for direction, distance in commands:
        dx, dy = direction_map[direction]
        distance = int(distance)
        
        for _ in range(distance):
            x += dx
            y += dy
            time += 1
            
            # Mark the current position on the drawing board
            drawing_board[x][y] = '#'
            
            # Check if the current drawing matches the target
            if matches_target():
                earliest_drying_time = min(earliest_drying_time, time)
                latest_drying_time = max(latest_drying_time, time)
    
    # If no valid drying time was found, return -1 -1
    if earliest_drying_time == float('inf'):
        print(-1, -1)
    else:
        print(earliest_drying_time, latest_drying_time)