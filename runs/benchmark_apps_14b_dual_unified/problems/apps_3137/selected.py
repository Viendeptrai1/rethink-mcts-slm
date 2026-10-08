import sys

def simulate_bacteria(N, M, K, trap_row, trap_col, bacteria):
    directions = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
    opposite_directions = {'U': 'D', 'R': 'L', 'D': 'U', 'L': 'R'}
    
    def move_bacterium(bacterium):
        x, y, direction, grid = bacterium
        X = int(grid[x-1][y-1])
        direction_index = list(directions.keys()).index(direction)
        new_direction_index = (direction_index + X) % 4
        new_direction = list(directions.keys())[new_direction_index]
        
        dx, dy = directions[new_direction]
        nx, ny = x + dx, y + dy
        
        if not (1 <= nx <= N and 1 <= ny <= M):
            new_direction = opposite_directions[new_direction]
            dx, dy = directions[new_direction]
            nx, ny = x + dx, y + dy
        
        return (nx, ny, new_direction, grid)
    
    time = 0
    while True:
        time += 1
        new_positions = [move_bacterium(b) for b in bacteria]
        
        if any((x, y) == (trap_row, trap_col) for x, y, _, _ in new_positions):
            return time
        
        positions = set((x, y) for x, y, _, _ in new_positions)
        if len(positions) != len(new_positions):
            return -1
        
        bacteria = new_positions

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    M = int(data[index + 1])
    K = int(data[index + 2])
    index += 3
    
    trap_row = int(data[index])
    trap_col = int(data[index + 1])
    index += 2
    
    bacteria = []
    for _ in range(K):
        x = int(data[index])
        y = int(data[index + 1])
        direction = data[index + 2]
        index += 3
        
        grid = []
        for _ in range(N):
            grid.append(data[index])
            index += 1
        
        bacteria.append((x, y, direction, grid))
    
    result = simulate_bacteria(N, M, K, trap_row, trap_col, bacteria)
    print(result)

if __name__ == "__main__":
    main()