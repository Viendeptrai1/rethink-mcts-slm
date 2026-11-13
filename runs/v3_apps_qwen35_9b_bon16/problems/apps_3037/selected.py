import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        h = int(next(iterator))
        w = int(next(iterator))
        n = int(next(iterator))
        
        # Read the grid pattern
        target_grid = []
        for _ in range(h):
            row_str = next(iterator)
            target_grid.append(row_str)
            
        # Parse commands
        commands = []
        for _ in range(n):
            direction = next(iterator)
            distance = int(next(iterator))
            commands.append((direction, distance))
            
    except StopIteration:
        return

    # Determine the path taken by the marker
    # Start at bottom-left: (h-1, 0)
    # Coordinates: row 0 is top, row h-1 is bottom. col 0 is left, col w-1 is right.
    
    curr_r, curr_c = h - 1, 0
    path = []  # List of (step, r, c) where step is 0-indexed timestep when marker lands on cell
    
    for t in range(n):
        dir_name, dist = commands[t]
        dr, dc = 0, 0
        
        if dir_name == 'up':
            dr = -1
        elif dir_name == 'down':
            dr = 1
        elif dir_name == 'left':
            dc = -1
        elif dir_name == 'right':
            dc = 1
            
        for k in range(1, dist + 1):
            new_r = curr_r + dr * k
            new_c = curr_c + dc * k
            step = t + k
            path.append((step, new_r, new_c))
            curr_r, curr_c = new_r, new_c

    if not path:
        # No moves made, only start position.
        # Timestep 0 is start.
        # Check if start matches target.
        if target_grid[h-1][0] == '#':
            print("0 0")
        else:
            print("-1 -1")
        return

    last_step = path[-1][0]
    
    # We need to find the range of dry-out times [min_t, max_t] such that the resulting drawing matches target_grid.
    # The marker draws on cells visited from step 0 (start) up to step T inclusive.
    # If it dries out at time T, it draws on steps 0, 1, ..., T.
    # It does NOT draw on step T+1.
    
    # Let's create an array to store for each cell, the set of timesteps it was visited.
    # Since h*w <= 1,000,000, we can map (r,c) to an index 0..h*w-1.
    # We want to know for each cell, what are the possible "last drawn time" values that result in '#' or '.'.
    
    # Actually, the condition is simpler:
    # For each cell (r, c):
    #   If target_grid[r][c] == '#':
    #       The cell must be marked at least once in the range [0, T].
    #       So, the first time the marker visits (r,c), let's call it first_visit[r][c].
    #       We must have first_visit[r][c] <= T.
    #   If target_grid[r][c] == '.':
    #       The cell must NOT be marked in the range [0, T].
    #       So, if the marker ever visits (r,c), the last time it visits it must be > T.
    #       Wait, no. If it dries out at T, then any visit at time t <= T results in a mark.
    #       So if target is '.', then for ALL visits at time t to (r,c), we must have t > T.
    #       This means if the marker visits (r,c) at any time t <= T, it's invalid.
    #       Therefore, if target is '.', and the marker visits (r,c) at time t, then we must have T < t.
    #       This implies T must be strictly less than the MINIMUM visit time to that cell?
    #       No, if the marker visits a cell multiple times, say at times t1, t2, t3...
    #       If target is '.', then we cannot have ANY of these times <= T.
    #       So all visit times must be > T.
    #       Thus, T < min(visit_times).
    
    # Let's re-verify the logic.
    # Scenario: Target has '.' at (r,c). Path visits (r,c) at times 5, 10, 15.
    # If T = 4: Visits <= 4 are none. Cell remains '.'. OK.
    # If T = 5: Visits <= 5 include 5. Cell becomes '#'. FAIL.
    # So if target is '.', T must be < first_visit_time.
    
    # Scenario: Target has '#' at (r,c). Path visits (r,c) at times 5, 10, 15.
    # If T = 4: Visits <= 4 are none. Cell remains '.' (initial state). FAIL.
    # If T = 5: Visits <= 5 include 5. Cell becomes '#'. OK.
    # So if target is '#', T must be >= first_visit_time.
    
    # Summary:
    # For each cell (r,c):
    #   Let visits be the sorted list of timesteps the marker visits (r,c).
    #   If target[r][c] == '#':
    #       We need at least one visit <= T.
    #       Since visits are sorted, we just need the FIRST visit time <= T.
    #       Constraint: T >= first_visit_time[r][c].
    #   If target[r][c] == '.':
    #       We need NO visits <= T.
    #       This means the FIRST visit time (if exists) must be > T.
    #       Constraint: T < first_visit_time[r][c]. (If never visited, constraint is T < infinity, i.e., no upper bound from this cell).
    
    # If a cell in target is '#' but the marker never visits it, then it's impossible -> -1 -1.
    # If a cell in target is '.' and the marker visits it at time t, then T must be < t.
    
    # So we can compute:
    # min_T = 0 (since T>=0 is always true, and start is step 0)
    # max_T = last_step (potentially)
    #
    # For each cell (r,c):
    #   Find first_visit_time[r][c].
    #   If target[r][c] == '#':
    #       If first_visit_time is None: return -1 -1
    #       min_T = max(min_T, first_visit_time[r][c])
    #   If target[r][c] == '.':
    #       If first_visit_time is not None:
    #           max_T = min(max_T, first_visit_time[r][c] - 1)
    
    # Initial state:
    # The board is initially all '.'.
    # Start position (h-1, 0) is step 0.
    
    # We need to track first_visit_time for each cell.
    # Initialize first_visit with infinity.
    
    # Map (r, c) to index: r * w + c
    # Size h * w <= 1,000,000.
    
    first_visit = {} # Dictionary mapping (r,c) -> first timestep
    # Or use a flat array if we want speed, but dict is fine for 1e6.
    # Actually, let's use a list for O(1) access.
    
    # Initialize first_visit array with a value larger than any possible step (e.g., last_step + 1)
    # Or just -1 and check. Let's use -1 to indicate not visited.
    
    first_visit_arr = [-1] * (h * w)
    
    # Process path
    # path contains (step, r, c)
    # We only care about the first time we visit a cell.
    
    for step, r, c in path:
        idx = r * w + c
        if first_visit_arr[idx] == -1:
            first_visit_arr[idx] = step
            
    # Now calculate min_T and max_T
    min_T = 0
    max_T = last_step
    
    possible = True
    
    for r in range(h):
        row_str = target_grid[r]
        for c in range(w):
            is_target_hash = (row_str[c] == '#')
            idx = r * w + c
            tv = first_visit_arr[idx]
            
            if is_target_hash:
                if tv == -1:
                    # Target needs a mark, but marker never visited.
                    possible = False
                    break
                else:
                    if tv > min_T:
                        min_T = tv
            else:
                # Target needs blank.
                if tv != -1:
                    # Marker visited, so T must be < tv.
                    # Current max_T is candidate.
                    # If tv - 1 < min_T, then we might have a conflict later?
                    # We just update max_T.
                    if tv - 1 < max_T:
                        max_T = tv - 1
        
        if not possible:
            break
            
    if not possible:
        print("-1 -1")
    elif min_T > max_T:
        print("-1 -1")
    else:
        print(f"{min_T} {max_T}")

if __name__ == '__main__':
    solve()