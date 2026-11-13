def min_max_drying_time(h, w, n, pattern, commands):
    directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
    x, y = h - 1, 0
    min_time = float('inf')
    max_time = 0
    
    def is_valid(x, y):
        return 0 <= x < h and 0 <= y < w
    
    def get_next_position(x, y, dx, dy):
        while is_valid(x + dx, y + dy):
            x += dx
            y += dy
        return x, y
    
    for i in range(n):
        direction, distance = commands[i].split()
        dx, dy = directions[direction]
        nx, ny = get_next_position(x, y, dx, dy)
        
        if pattern[nx][ny] == '#':
            min_time = min(min_time, i * distance + (nx - x) * abs(dx) + (ny - y) * abs(dy))
        
        x, y = nx, ny
    
    if min_time == float('inf'):
        return -1, -1
    
    return min_time, max_time

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
        pattern.append(list(data[index]))
        index += 1
    
    commands = []
    for _ in range(n):
        commands.append(data[index])
        index += 1
    
    result = min_max_drying_time(h, w, n, pattern, commands)
    print(result[0], result[1])