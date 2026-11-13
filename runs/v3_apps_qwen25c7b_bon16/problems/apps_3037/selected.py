import sys

def min_max_time(h, w, n, pattern, commands):
    def move(x, y, dx, dy, steps):
        return x + dx * steps, y + dy * steps

    def get_steps_to_target(x, y, target):
        if target[x][y] == '#':
            return 1
        return 0

    def is_valid_move(x, y, dx, dy, steps):
        nx, ny = move(x, y, dx, dy, steps)
        return 0 <= nx < h and 0 <= ny < w

    def simulate(commands, pattern):
        x, y = h - 1, 0
        current_pattern = [['.' for _ in range(w)] for _ in range(h)]
        current_pattern[x][y] = '#'
        steps_taken = 0

        for command in commands:
            direction, distance = command.split()
            dx, dy = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}[direction]
            steps_taken += 1
            while is_valid_move(x, y, dx, dy, 1):
                x, y = move(x, y, dx, dy, 1)
                if current_pattern[x][y] != '#' and pattern[x][y] == '#':
                    current_pattern[x][y] = '#'
                elif current_pattern[x][y] == '#' and pattern[x][y] == '.':
                    return -1
                steps_taken += 1
                if steps_taken >= n:
                    break

        return steps_taken if current_pattern == pattern else -1

    min_steps = float('inf')
    max_steps = 0
    for i in range(1, n + 1):
        temp_pattern = [row[:] for row in pattern]
        result = simulate(commands[:i], temp_pattern)
        if result != -1:
            min_steps = min(min_steps, result)
            max_steps = max(max_steps, result)

    return min_steps if min_steps != float('inf') else -1, max_steps if max_steps > 0 else -1

if __name__ == "__main__":
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

    min_time, max_time = min_max_time(h, w, n, pattern, commands)
    print(min_time, max_time)