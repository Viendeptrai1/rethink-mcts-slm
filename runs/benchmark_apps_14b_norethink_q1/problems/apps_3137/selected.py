from collections import deque

def get_next_direction(current_dir, turns):
    directions = ['U', 'R', 'D', 'L']
    index = directions.index(current_dir)
    new_index = (index + turns) % 4
    return directions[new_index]

def move_bacteria(N, M, X, Y, bacteria):
    queue = deque([(bacteria, 0)])
    visited = set()
    visited.add(tuple(bacteria))
    
    while queue:
        current_state, time = queue.popleft()
        
        if all(x == X and y == Y for x, y, _ in current_state):
            return time
        
        next_state = []
        for x, y, dir in current_state:
            num = board[x-1][y-1]
            new_dir = get_next_direction(dir, num)
            
            if new_dir == 'U' and x > 1:
                new_x, new_y = x-1, y
            elif new_dir == 'D' and x < N:
                new_x, new_y = x+1, y
            elif new_dir == 'L' and y > 1:
                new_x, new_y = x, y-1
            elif new_dir == 'R' and y < M:
                new_x, new_y = x, y+1
            else:
                new_dir = get_next_direction(new_dir, 2)
                if new_dir == 'U':
                    new_x, new_y = x-1, y
                elif new_dir == 'D':
                    new_x, new_y = x+1, y
                elif new_dir == 'L':
                    new_x, new_y = x, y-1
                elif new_dir == 'R':
                    new_x, new_y = x, y+1
            
            next_state.append((new_x, new_y, new_dir))
        
        next_state_tuple = tuple(next_state)
        if next_state_tuple not in visited:
            visited.add(next_state_tuple)
            queue.append((next_state_tuple, time + 1))
    
    return -1

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])
K = int(data[2])

trap_X = int(data[3])
trap_Y = int(data[4])

bacteria = []
index = 5
for i in range(K):
    start_X = int(data[index])
    start_Y = int(data[index + 1])
    start_dir = data[index + 2]
    bacteria.append((start_X, start_Y, start_dir))
    index += 3
    
board = []
for i in range(N):
    row = [int(c) for c in data[index]]
    board.append(row)
    index += 1

# Run the simulation
result = move_bacteria(N, M, trap_X, trap_Y, bacteria)
print(result)