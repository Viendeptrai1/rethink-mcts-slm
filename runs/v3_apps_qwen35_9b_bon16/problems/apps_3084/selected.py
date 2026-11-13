import sys

def get_next_valid(current):
    h, m = map(int, current.split(':'))
    
    # Try increasing minutes
    candidates = []
    for _ in range(2):
        m = (m + 1) % 60
        if h <= 23 and m <= 59:
            candidates.append(f"{h:02d}:{m:02d}")
        else:
            # Minutes are invalid, try to increment hour
            h = (h + 1) % 24
            if h <= 23:
                candidates.append(f"{h:02d}:{m:02d}")
            else:
                break
    
    # If we couldn't find a valid time by just incrementing minutes, try the next hour
    if not candidates:
        h = (h + 1) % 24
        m = 0
        if h <= 23:
            candidates = [f"{h:02d}:{m:02d}"]
    
    # Try decreasing minutes
    for _ in range(2):
        m = (m - 1) % 60
        if h <= 23 and m <= 59:
            candidates.append(f"{h:02d}:{m:02d}")
        else:
            # Minutes are invalid, try to decrement hour
            h = (h - 1) % 24
            if h <= 23:
                candidates.append(f"{h:02d}:{m:02d}")
            else:
                break
    
    # If we couldn't find a valid time by just decrementing minutes, try the previous hour
    if not candidates:
        h = (h - 1) % 24
        m = 59
        if h <= 23:
            candidates = [f"{h:02d}:{m:02d}"]
    
    # Try increasing hours
    for _ in range(2):
        h = (h + 1) % 24
        m = 0
        if h <= 23 and m <= 59:
            candidates.append(f"{h:02d}:{m:02d}")
        else:
            break
    
    # Try decreasing hours
    for _ in range(2):
        h = (h - 1) % 24
        m = 59
        if h <= 23 and m <= 59:
            candidates.append(f"{h:02d}:{m:02d}")
        else:
            break
    
    return candidates

def solve():
    lines = sys.stdin.read().strip().split('\n')
    if len(lines) < 2:
        return
    start_time = lines[0].strip()
    target_time = lines[1].strip()
    
    # If start equals target, output 1 and the time
    if start_time == target_time:
        print(1)
        print(start_time)
        return
    
    # BFS to find the shortest path
    from collections import deque
    queue = deque([(start_time, 1)])  # (time, count)
    visited = {start_time}
    result_times = [start_time]
    
    while queue:
        current, count = queue.popleft()
        
        if current == target_time:
            result_times.append(target_time)
            break
        
        # Get next possible times
        next_times = get_next_valid(current)
        
        for t in next_times:
            if t not in visited:
                visited.add(t)
                result_times.append(t)
                queue.append((t, count + 1))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_times = []
    for t in result_times:
        if t not in seen:
            seen.add(t)
            unique_times.append(t)
    
    # The problem asks for the number of different times seen when setting it correctly.
    # This implies the shortest path. Our BFS guarantees the shortest path.
    # However, the example output shows the sequence of times.
    # We need to output the count and then each time in the sequence.
    
    # Re-run BFS to get the exact sequence without duplicates in the list but with the path
    queue = deque([(start_time, [start_time])])
    visited = {start_time}
    result_path = None
    
    while queue:
        current, path = queue.popleft()
        
        if current == target_time:
            result_path = path
            break
        
        next_times = get_next_valid(current)
        
        for t in next_times:
            if t not in visited:
                visited.add(t)
                queue.append((t, path + [t]))
    
    if result_path:
        print(len(result_path))
        for t in result_path:
            print(t)
    else:
        # Fallback, though BFS should always find a path
        print(len(result_times))
        for t in result_times:
            print(t)

if __name__ == "__main__":
    solve()