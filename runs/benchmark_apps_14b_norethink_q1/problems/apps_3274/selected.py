import sys

def main():
    import sys
    import collections
    
    def is_valid_move(x, y, ships):
        return y > 0 and (x, y) not in ships
    
    def find_path(n, m, ships):
        start = (0, 0)
        end = (0, n)
        queue = collections.deque([(start, '')])
        visited = set([start])
        
        while queue:
            (x, y), path = queue.popleft()
            
            if (x, y) == end:
                return path
            
            for dx in [-1, 0, 1]:
                nx, ny = x + dx, y + 1
                if is_valid_move(nx, ny, ships) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + ('-' if dx == -1 else '+' if dx == 1 else '0')))
        
        return "impossible"
    
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    ships = set()
    for _ in range(m):
        x1 = int(data[index])
        x2 = int(data[index + 1])
        y = int(data[index + 2])
        index += 3
        for x in range(x1, x2 + 1):
            ships.add((x, y))
    
    result = find_path(n, m, ships)
    print(result)

if __name__ == "__main__":
    main()