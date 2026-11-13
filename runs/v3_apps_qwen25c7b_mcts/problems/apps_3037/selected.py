def min_max_drying_time(h, w, n, pattern, commands):
    directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
    grid = [[False] * w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            if pattern[i][j] == '#':
                grid[i][j] = True
    
    def is_valid(x, y):
        return 0 <= x < h and 0 <= y < w
    
    def simulate(commands, start_x, start_y):
        x, y = start_x, start_y
        steps = 0
        for cmd in commands:
            dir, dist = cmd.split()
            dx, dy = directions[dir]
            for _ in range(int(dist)):
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny):
                    x, y = nx, ny
                    steps += 1
                    if grid[x][y]:
                        break
        return steps
    
    min_steps = float('inf')
    max_steps = 0
    for i in range(h):
        for j in range(w):
            if not grid[i][j]:
                steps = simulate(commands, i, j)
                if steps != float('inf'):
                    min_steps = min(min_steps, steps)
                    max_steps = max(max_steps, steps)
    
    if min_steps == float('inf'):
        return -1, -1
    else:
        return min_steps, max_steps

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    h = int(data[0])
    w = int(data[1])
    n = int(data[2])
    
    pattern = []
    index = 3
    for _ in range(h):
        pattern.append(data[index])
        index += 1
    
    commands = []
    for _ in range(n):
        commands.append(data[index])
        index += 1
    
    result = min_max_drying_time(h, w, n, pattern, commands)
    print(result[0], result[1])