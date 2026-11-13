def bacteria_game(N, M, K, trap_row, trap_col, bacteria_info):
    from collections import defaultdict, deque

    # Directions: U, R, D, L
    directions = {
        'U': (-1, 0),
        'R': (0, 1),
        'D': (1, 0),
        'L': (0, -1)
    }

    # Reverse directions for turning 180 degrees
    reverse_direction = {
        'U': 'D',
        'R': 'L',
        'D': 'U',
        'L': 'R'
    }

    # Turn 90 degrees clockwise
    def turn_clockwise(direction):
        if direction == 'U':
            return 'R'
        elif direction == 'R':
            return 'D'
        elif direction == 'D':
            return 'L'
        elif direction == 'L':
            return 'U'

    # Initialize the state of each bacterium
    bacteria_states = []
    for i in range(K):
        x, y, direction = bacteria_info[i][:3]
        matrix = bacteria_info[i][3]
        bacteria_states.append((x - 1, y - 1, direction, matrix))

    # Track the positions of bacteria
    positions = defaultdict(list)
    for idx, (x, y, _, _) in enumerate(bacteria_states):
        positions[(x, y)].append(idx)

    # BFS to simulate the game
    queue = deque([(0, bacteria_states)])
    visited = set()
    visited.add((0, tuple((x, y, d) for x, y, d, _ in bacteria_states)))

    while queue:
        time, current_states = queue.popleft()

        # Check if all bacteria are in the trap
        if all(x == trap_row - 1 and y == trap_col - 1 for x, y, _, _ in current_states):
            return time

        # Move each bacterium
        new_states = []
        for idx, (x, y, direction, matrix) in enumerate(current_states):
            steps = matrix[x][y]
            for _ in range(steps):
                direction = turn_clockwise(direction)

            # Calculate new position
            dx, dy = directions[direction]
            new_x, new_y = x + dx, y + dy

            # Check if out of bounds
            if not (0 <= new_x < N and 0 <= new_y < M):
                direction = reverse_direction[direction]
                dx, dy = directions[direction]
                new_x, new_y = x + dx, y + dy

            new_states.append((new_x, new_y, direction, matrix))

        # Check for collision with trap
        if (new_x, new_y) == (trap_row - 1, trap_col - 1):
            return time + 1

        # Check for collision with other bacteria
        new_positions = defaultdict(list)
        for idx, (x, y, _, _) in enumerate(new_states):
            new_positions[(x, y)].append(idx)

        # If there's a collision, the game ends
        if any(len(v) > 1 for v in new_positions.values()):
            return time + 1

        # Serialize the state to check for repeated states
        state_tuple = tuple((x, y, d) for x, y, d, _ in new_states)
        if (time + 1, state_tuple) not in visited:
            visited.add((time + 1, state_tuple))
            queue.append((time + 1, new_states))

    return -1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])
K = int(data[2])
trap_row = int(data[3])
trap_col = int(data[4])

bacteria_info = []
index = 5
for i in range(K):
    x = int(data[index])
    y = int(data[index + 1])
    direction = data[index + 2]
    matrix = []
    for j in range(N):
        matrix.append([int(data[index + 3 + j * M + col]) for col in range(M)])
    bacteria_info.append((x, y, direction, matrix))
    index += 3 + N * M

print(bacteria_game(N, M, K, trap_row, trap_col, bacteria_info))