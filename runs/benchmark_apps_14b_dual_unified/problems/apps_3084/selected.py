from collections import deque, defaultdict

def get_neighbors(time):
    neighbors = []
    h = int(time[:2])
    m = int(time[3:])
    
    # Change hours
    for dh in [-1, 1]:
        nh = (h + dh) % 24
        neighbors.append(f"{nh:02}:{m:02}")
    
    # Change minutes
    for dm in [-1, 1]:
        nm = (m + dm) % 60
        neighbors.append(f"{h:02}:{nm:02}")
    
    return neighbors

def bfs(start_time, end_time):
    queue = deque([start_time])
    visited = set([start_time])
    path = {start_time: None}
    
    while queue:
        current = queue.popleft()
        
        if current == end_time:
            break
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                path[neighbor] = current
                queue.append(neighbor)
    
    # Reconstruct the path
    result = []
    while current:
        result.append(current)
        current = path[current]
    
    return result[::-1]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    start_time = data[0]
    end_time = data[1]
    
    path = bfs(start_time, end_time)
    
    print(len(path))
    for time in path:
        print(time)

if __name__ == "__main__":
    main()