def simulate_bacteria(N, M, K, trap_row, trap_col, bacteria):
    directions = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
    opposite_directions = {'U': 'D', 'R': 'L', 'D': 'U', 'L': 'R'}
    
    def move_bacterium(bac):
        x, y, dir_index = bac['pos']
        X = bac['grid'][x-1][y-1]
        
        # Turn 90 degrees clockwise X times
        dir_index = (dir_index + X) % 4
        dx, dy = directions[list(directions.keys())[dir_index]]
        
        # Check if the new position is out of bounds
        if not (1 <= x + dx <= N and 1 <= y + dy <= M):
            # Turn 180 degrees
            dir_index = (dir_index + 2) % 4
            dx, dy = directions[list(directions.keys())[dir_index]]
        
        # Move to the new position
        bac['pos'] = (x + dx, y + dy, dir_index)
    
    # Initialize bacteria positions and directions
    bacs = []
    for i in range(K):
        x, y, C = bacteria[i]['start']
        grid = bacteria[i]['grid']
        bacs.append({'pos': (x, y, list(directions.keys()).index(C)), 'grid': grid})
    
    # Simulate the movement
    time = 0
    while True:
        time += 1
        for bac in bacs:
            move_bacterium(bac)
        
        # Check if all bacteria are in the trap cell
        if all(bac['pos'][:2] == (trap_row, trap_col) for bac in bacs):
            return time
    
    return -1

# Read input
N, M, K = map(int, input().split())
trap_row, trap_col = map(int, input().split())

bacteria = []
for _ in range(K):
    x, y, C = input().split()
    x, y = int(x), int(y)
    grid = [list(map(int, input().strip())) for _ in range(N)]
    bacteria.append({'start': (x, y, C), 'grid': grid})

# Output the result
print(simulate_bacteria(N, M, K, trap_row, trap_col, bacteria))