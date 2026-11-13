from collections import deque

def get_next_times(current_time):
    next_times = []
    hours, minutes = map(int, current_time.split(':'))
    
    # Increment hour
    new_hours = (hours + 1) % 24
    next_times.append(f"{new_hours:02}:{minutes:02}")
    
    # Decrement hour
    new_hours = (hours - 1) % 24
    next_times.append(f"{new_hours:02}:{minutes:02}")
    
    # Increment minute
    new_minutes = (minutes + 1) % 60
    next_times.append(f"{hours:02}:{new_minutes:02}")
    
    # Decrement minute
    new_minutes = (minutes - 1) % 60
    next_times.append(f"{hours:02}:{new_minutes:02}")
    
    return next_times

def bfs(start_time, end_time):
    queue = deque([start_time])
    visited = set([start_time])
    parent = {start_time: None}
    
    while queue:
        current_time = queue.popleft()
        
        if current_time == end_time:
            break
        
        for next_time in get_next_times(current_time):
            if next_time not in visited:
                visited.add(next_time)
                parent[next_time] = current_time
                queue.append(next_time)
    
    path = []
    while end_time is not None:
        path.append(end_time)
        end_time = parent[end_time]
    
    return path[::-1]

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    start_time = data[0]
    end_time = data[1]
    
    path = bfs(start_time, end_time)
    
    print(len(path))
    for time in path:
        print(time)

if __name__ == "__main__":
    main()