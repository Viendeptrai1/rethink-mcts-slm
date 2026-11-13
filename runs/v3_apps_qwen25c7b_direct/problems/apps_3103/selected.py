from collections import deque

def count_paths(Y, X, x_init, map_data):
    MOD = 1000003
    directions = [(-1, 0), (0, 1), (0, -1)]
    
    def is_valid(x, y):
        return 0 <= x < Y and 0 <= y < X
    
    def can_move_right(x, y):
        return map_data[x][y] == '>' and is_valid(x + 1, y) and map_data[x + 1][y] != '<' and map_data[x + 1][y] != '#'
    
    def can_move_left(x, y):
        return map_data[x][y] == '<' and is_valid(x - 1, y) and map_data[x - 1][y] != '>' and map_data[x - 1][y] != '#'
    
    queue = deque([(Y - 1, x_init, 0)])
    visited = set()
    visited.add((Y - 1, x_init))
    
    while queue:
        x, y, steps = queue.popleft()
        
        if map_data[x][y] == '@':
            return steps % MOD
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if is_valid(nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))
                
                if can_move_right(x, y):
                    queue.append((x, y + 1, steps + 1))
                    
                if can_move_left(x, y):
                    queue.append((x, y - 1, steps + 1))
    
    return "begin repairs"

# Example usage:
# result = count_paths(2, 2, 0, ['>@', '>~'])
# print(result)  # Output: 2