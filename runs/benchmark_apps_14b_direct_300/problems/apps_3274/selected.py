import sys

def main():
    import sys
    import heapq
    
    def can_dodge(n, m, ships):
        # Sort ships by y-coordinate
        ships.sort(key=lambda x: x[2])
        
        # Priority queue to keep track of the positions the torpedo can be at
        pq = []
        heapq.heappush(pq, (0, 0, 0))  # (time, x, y)
        
        # Set to keep track of visited states
        visited = set()
        visited.add((0, 0))
        
        # Directions: left, straight, right
        directions = [(-1, 1), (0, 1), (1, 1)]
        
        while pq:
            time, x, y = heapq.heappop(pq)
            
            # If we reached the end without hitting any ship
            if time == n:
                return True
            
            # Try all possible directions
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                # Check if the new position is within bounds and not on a ship
                if 0 <= ny < n and -n <= nx <= n and (nx, ny) not in visited:
                    if not any(x1 <= nx <= x2 and ny == y for x1, x2, y in ships):
                        visited.add((nx, ny))
                        heapq.heappush(pq, (time + 1, nx, ny))
        
        return False
    
    def find_path(n, m, ships):
        # Sort ships by y-coordinate
        ships.sort(key=lambda x: x[2])
        
        # Priority queue to keep track of the positions the torpedo can be at
        pq = []
        heapq.heappush(pq, (0, 0, 0, ""))  # (time, x, y, path)
        
        # Set to keep track of visited states
        visited = set()
        visited.add((0, 0))
        
        # Directions: left, straight, right
        directions = [(-1, 1, '-'), (0, 1, '0'), (1, 1, '+')]
        
        while pq:
            time, x, y, path = heapq.heappop(pq)
            
            # If we reached the end without hitting any ship
            if time == n:
                return path
            
            # Try all possible directions
            for dx, dy, move in directions:
                nx, ny = x + dx, y + dy
                
                # Check if the new position is within bounds and not on a ship
                if 0 <= ny < n and -n <= nx <= n and (nx, ny) not in visited:
                    if not any(x1 <= nx <= x2 and ny == y for x1, x2, y in ships):
                        visited.add((nx, ny))
                        heapq.heappush(pq, (time + 1, nx, ny, path + move))
        
        return "impossible"
    
    # Read input
    n, m = map(int, sys.stdin.readline().split())
    ships = [tuple(map(int, sys.stdin.readline().split())) for _ in range(m)]
    
    # Check if dodging is possible
    if can_dodge(n, m, ships):
        # Find and print the path
        path = find_path(n, m, ships)
        print(path)
    else:
        print("impossible")

if __name__ == "__main__":
    main()