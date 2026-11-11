from collections import deque

def get_neighbors(time):
    neighbors = []
    h1, h2, m1, m2 = int(time[0]), int(time[1]), int(time[3]), int(time[4])
    
    # Change hour first digit
    for dh1 in [-1, 1]:
        nh1 = (h1 + dh1) % 10
        if 0 <= int(f"{nh1}{h2}") <= 23:
            neighbors.append(f"{nh1}{h2}:{m1}{m2}")
    
    # Change hour second digit
    for dh2 in [-1, 1]:
        nh2 = (h2 + dh2) % 10
        if 0 <= int(f"{h1}{nh2}") <= 23:
            neighbors.append(f"{h1}{nh2}:{m1}{m2}")
    
    # Change minute first digit
    for dm1 in [-1, 1]:
        nm1 = (m1 + dm1) % 10
        if 0 <= int(f"{m1}{nm1}") <= 59:
            neighbors.append(f"{h1}{h2}:{nm1}{m2}")
    
    # Change minute second digit
    for dm2 in [-1, 1]:
        nm2 = (m2 + dm2) % 10
        if 0 <= int(f"{m1}{m2}") <= 59:
            neighbors.append(f"{h1}{h2}:{m1}{nm2}")
    
    return neighbors

def bfs(start, end):
    queue = deque([start])
    visited = set([start])
    path = {start: [start]}
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            return path[current]
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                path[neighbor] = path[current] + [neighbor]
    
    return []

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    current_time = data[0]
    target_time = data[1]
    
    result_path = bfs(current_time, target_time)
    
    print(len(result_path))
    for time in result_path:
        print(time)

if __name__ == "__main__":
    main()