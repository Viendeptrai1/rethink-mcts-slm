def simulate_bacteria_game(N, M, K, trap_row, trap_col, bacteria_info):
    from collections import deque

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
    def turn_right(direction):
        if direction == 'U':
            return 'R'
        elif direction == 'R':
            return 'D'
        elif direction == 'D':
            return 'L'
        elif direction == 'L':
            return 'U'

    # Initialize bacteria states
    bacteria_states = []
    for i in range(K):
        x, y, direction = bacteria_info[i][:3]
        matrix = bacteria_info[i][3]
        bacteria_states.append({
            'position': (x - 1, y - 1),
            'direction': direction,
            'matrix': matrix
        })

    # Simulate the game
    time = 0
    visited = set()

    while True:
        time += 1
        new_positions = []

        for i, state in enumerate(bacteria_states):
            x, y = state['position']
            direction = state['direction']
            matrix = state['matrix']

            # Read the number in the current cell
            steps = int(matrix[x][y])

            # Turn the required number of times
            for _ in range(steps):
                direction = turn_right(direction)

            # Calculate new position
            dx, dy = directions[direction]
            new_x, new_y = x + dx, y + dy

            # Check if new position is out of bounds
            if not (0 <= new_x < N and 0 <= new_y < M):
                direction = reverse_direction[direction]
                dx, dy = directions[direction]
                new_x, new_y = x + dx, y + dy

            new_positions.append((new_x, new_y, direction, i))

        # Check for collisions
        collision = False
        position_count = {}
        for new_x, new_y, direction, index in new_positions:
            if (new_x, new_y) == (trap_row - 1, trap_col - 1):
                return time
            if (new_x, new_y) in position_count:
                position_count[(new_x, new_y)].append(index)
            else:
                position_count[(new_x, new_y)] = [index]

        for pos, indices in position_count.items():
            if len(indices) > 1:
                collision = True
                break

        if collision:
            return time

        # Update positions
        for (new_x, new_y, direction, index) in new_positions:
            bacteria_states[index]['position'] = (new_x, new_y)
            bacteria_states[index]['direction'] = direction

        # Check for infinite loop
        state_key = tuple((state['position'], state['direction']) for state in bacteria_states)
        if state_key in visited:
            return -1
        visited.add(state_key)

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
        matrix.append(data[index + 3 + j])
    bacteria_info.append((x, y, direction, matrix))
    index += 3 + N

result = simulate_bacteria_game(N, M, K, trap_row, trap_col, bacteria_info)
print(result)