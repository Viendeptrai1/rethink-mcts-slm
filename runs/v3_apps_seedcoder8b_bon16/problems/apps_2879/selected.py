import sys
from collections import defaultdict, deque

def find_polyomino_power(h, w, grid):
    # Find all 'X' positions
    positions = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == 'X']
    
    def bfs(start):
        queue = deque([start])
        visited = set([start])
        while queue:
            x, y = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] == 'X' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return visited
    
    # Find all connected components
    components = []
    visited = set()
    for pos in positions:
        if pos not in visited:
            component = bfs(pos)
            components.append(component)
            visited.update(component)
    
    # Check if components are uniform
    component_sizes = [len(comp) for comp in components]
    if len(set(component_sizes)) != 1:
        return "No solution"
    
    # Check if it's a power
    for k in range(2, 6):
        if component_sizes[0] == k * k:
            return [[1 for _ in range(w)] for _ in range(h)]
    
    return "No solution"

def main():
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    h, w = map(int, data[0].split())
    grid = [list(data[i + 1]) for i in range(h)]
    
    result = find_polyomino_power(h, w, grid)
    
    if isinstance(result, str):
        print(result)
    else:
        for row in result:
            print(''.join(map(str, row)))

if __name__ == "__main__":
    main()