def get_next_time(current_time):
    hours, minutes = map(int, current_time.split(':'))
    minutes += 1
    if minutes == 60:
        minutes = 0
        hours += 1
        if hours == 24:
            hours = 0
    return f"{hours:02}:{minutes:02}"

def get_previous_time(current_time):
    hours, minutes = map(int, current_time.split(':'))
    minutes -= 1
    if minutes == -1:
        minutes = 59
        hours -= 1
        if hours == -1:
            hours = 23
    return f"{hours:02}:{minutes:02}"

def find_path(original_time, target_time):
    visited = set()
    queue = [original_time]
    paths = {original_time: [original_time]}
    
    while queue:
        current_time = queue.pop(0)
        
        if current_time == target_time:
            return paths[current_time]
        
        next_time = get_next_time(current_time)
        if next_time not in visited:
            visited.add(next_time)
            queue.append(next_time)
            paths[next_time] = paths[current_time] + [next_time]
        
        prev_time = get_previous_time(current_time)
        if prev_time not in visited:
            visited.add(prev_time)
            queue.append(prev_time)
            paths[prev_time] = paths[current_time] + [prev_time]
    
    return []

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    original_time = data[0]
    target_time = data[1]
    
    path = find_path(original_time, target_time)
    print(len(path))
    for time in path:
        print(time)

if __name__ == "__main__":
    main()