import sys
from collections import deque

def get_neighbors(h, m):
    neighbors = []
    h_str = f"{h:02d}"
    m_str = f"{m:02d}"
    
    # Try modifying each of the 4 digits
    for i in range(4):
        if i == 0:
            digit = int(h_str[0])
            new_h_str = h_str[0]
            if i == 0:
                new_h_str = str((digit - 1) % 10)
            elif i == 1:
                new_h_str = str((digit - 1) % 10) + h_str[1]
            elif i == 2:
                new_h_str = h_str[0] + str((digit - 1) % 10)
            elif i == 3:
                new_h_str = h_str[0] + h_str[1]
            
            # Actually, let's do it more cleanly by index
            pass
        
    # Let's restart the logic cleanly
    digits = list(h_str) + list(m_str)
    
    for i in range(4):
        d = int(digits[i])
        
        # Decrease
        new_d = (d - 1) % 10
        new_digits = digits[:]
        new_digits[i] = str(new_d)
        new_h = int(new_digits[0] + new_digits[1])
        new_m = int(new_digits[2] + new_digits[3])
        if 0 <= new_h <= 23 and 0 <= new_m <= 59:
            neighbors.append((new_h, new_m))
        
        # Increase
        new_d = (d + 1) % 10
        new_digits = digits[:]
        new_digits[i] = str(new_d)
        new_h = int(new_digits[0] + new_digits[1])
        new_m = int(new_digits[2] + new_digits[3])
        if 0 <= new_h <= 23 and 0 <= new_m <= 59:
            neighbors.append((new_h, new_m))
            
    return neighbors

def solve():
    input_data = sys.stdin.read().splitlines()
    if len(input_data) < 2:
        return
    
    start_str = input_data[0].strip()
    target_str = input_data[1].strip()
    
    start_h, start_m = map(int, start_str.split(':'))
    target_h, target_m = map(int, target_str.split(':'))
    
    start = (start_h, start_m)
    target = (target_h, target_m)
    
    if start == target:
        print(1)
        print(f"{start_h:02d}:{start_m:02d}")
        return
    
    # BFS to find shortest path
    queue = deque([start])
    visited = {start: None}  # time -> parent time
    
    found = False
    while queue:
        curr = queue.popleft()
        if curr == target:
            found = True
            break
        
        for neighbor in get_neighbors(*curr):
            if neighbor not in visited:
                visited[neighbor] = curr
                queue.append(neighbor)
    
    if not found:
        # Should not happen given problem constraints but good to handle
        print(0)
        return
    
    # Reconstruct path
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = visited[curr]
    
    path.reverse()
    
    print(len(path))
    for h, m in path:
        print(f"{h:02d}:{m:02d}")

if __name__ == "__main__":
    solve()