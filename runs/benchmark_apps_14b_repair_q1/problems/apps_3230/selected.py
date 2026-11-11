import sys
from collections import deque

def calculate_distance(r, c, x, y):
    return ((r - x) ** 2 + (c - y) ** 2) ** 0.5

def bfs_to_find_closest_seats(rows, cols, tram_layout):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque()
    visited = [[False] * cols for _ in range(rows)]
    explosions = 0
    
    # Enqueue all passengers
    for r in range(rows):
        for c in range(cols):
            if tram_layout[r][c] == 'X':
                queue.append((r, c))
                visited[r][c] = True
    
    while queue:
        size = len(queue)
        seats_taken = set()
        
        for _ in range(size):
            r, c = queue.popleft()
            
            min_distance = float('inf')
            closest_seat = None
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                while 0 <= nr < rows and 0 <= nc < cols and tram_layout[nr][nc] != '.':
                    distance = calculate_distance(r, c, nr, nc)
                    
                    if tram_layout[nr][nc] == 'L' and distance < min_distance:
                        min_distance = distance
                        closest_seat = (nr, nc)
                    
                    nr += dr
                    nc += dc
            
            if closest_seat:
                if closest_seat in seats_taken:
                    explosions += 1
                else:
                    seats_taken.add(closest_seat)
        
        for seat in seats_taken:
            tram_layout[seat[0]][seat[1]] = 'X'
    
    return explosions

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    C = int(data[1])
    
    tram_layout = []
    index = 2
    for _ in range(R):
        row = list(data[index])
        tram_layout.append(row)
        index += 1
    
    result = bfs_to_find_closest_seats(R, C, tram_layout)
    print(result)

if __name__ == "__main__":
    main()