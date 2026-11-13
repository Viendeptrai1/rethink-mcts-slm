import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)

    try:
        h = int(next(iterator))
        w = int(next(iterator))
        n = int(next(iterator))
    except StopIteration:
        return

    grid = []
    for _ in range(h):
        grid.append(next(iterator))

    commands = []
    for _ in range(n):
        direction = next(iterator)
        distance = int(next(iterator))
        commands.append((direction, distance))

    # Simulate the full path to get the sequence of visited cells and their timesteps
    # Timestep 0 is start. Timestep t corresponds to the cell visited at step t.
    # The marker draws at timestep t if it hasn't dried out before t.
    # If it dries out at timestep T, it draws cells at t=0, 1, ..., T.
    # It does NOT draw at t = T+1.
    
    # Let's simulate the full path first to know the coordinates at each timestep.
    # We'll store a list of (timestep, r, c)
    
    path = []
    r, c = h - 1, 0  # Start at bottom-left (row h-1, col 0)
    
    # Timestep 0
    path.append((0, r, c))
    
    for i, (direction, dist) in enumerate(commands):
        # The movement happens from current position.
        # The cells visited during this move are at timesteps: current_t + 1, current_t + 2, ..., current_t + dist
        # We need to record these.
        
        dr, dc = 0, 0
        if direction == 'up':
            dr = -1
        elif direction == 'down':
            dr = 1
        elif direction == 'left':
            dc = -1
        elif direction == 'right':
            dc = 1
        
        current_t = len(path)
        for d in range(1, dist + 1):
            nr, nc = r + dr * d, c + dc * d
            path.append((current_t + d, nr, nc))
            r, c = nr, nc
            
    total_steps = len(path) - 1 # Last timestep is total_steps
    
    # Now we need to find the range of T (dry out time) such that the resulting drawing matches the grid.
    # If marker dries out at T, it draws cells at timesteps 0, 1, ..., T.
    # Condition 1: For every cell (r, c) where grid[r][c] == '#', there must be at least one timestep t <= T such that path[t] == (r, c).
    # Condition 2: For every cell (r, c) where grid[r][c] == '.', there must be NO timestep t <= T such that path[t] == (r, c).
    
    # Let's precompute for each cell (r, c):
    # first_visit[r][c] = the smallest timestep t where the marker visits (r, c)
    # last_visit[r][c] = the largest timestep t where the marker visits (r, c)
    # Actually, for condition 2, we just need to know if it's visited at all.
    # But wait, if a cell is visited multiple times, say at t1 and t2 (t1 < t2), and we choose T such that t1 <= T < t2, then the cell is drawn (because t1 <= T).
    # If the cell is '.', it must NOT be drawn. So if it is visited at ANY t <= T, it's bad.
    # This implies that for a '.' cell, T must be strictly less than the FIRST visit time to that cell.
    # For a '#' cell, T must be greater than or equal to the FIRST visit time to that cell.
    
    # Let's verify this logic.
    # If grid[r][c] == '#': We need the cell to be drawn. It is drawn if min_visit_time <= T.
    # If grid[r][c] == '.': We need the cell NOT to be drawn. It is NOT drawn if min_visit_time > T.
    # So:
    # For '#': T >= min_visit_time
    # For '.': T < min_visit_time  => T <= min_visit_time - 1
    
    # We can compute min_visit_time for all cells visited.
    # Initialize min_visit with infinity.
    
    min_visit = {}
    
    for t, r, c in path:
        if (r, c) not in min_visit:
            min_visit[(r, c)] = t
        # We don't need max_visit because the condition depends only on the first time it's visited.
        # If a cell is visited at t1 and t2, and t1 <= T, it gets drawn. Whether t2 <= T or not doesn't change the fact it's drawn.
        # The only way a cell is NOT drawn is if ALL visit times are > T. Which means the first visit time > T.
    
    # Now determine constraints on T.
    # T must be an integer.
    # T >= 0 (given in problem: valid to dry out at 0)
    # T <= total_steps (problem says: "Neither number should be larger than the last timestep that the marker is on the board")
    
    min_T = 0
    max_T = total_steps
    
    # Check constraints from '#' cells
    for r in range(h):
        row_str = grid[r]
        for c in range(w):
            if row_str[c] == '#':
                if (r, c) not in min_visit:
                    # This '#' cell was never visited. Impossible.
                    print("-1 -1")
                    return
                t_first = min_visit[(r, c)]
                if t_first > max_T:
                    # Even if we go to the very end, we can't reach this '#' cell.
                    print("-1 -1")
                    return
                # Constraint: T >= t_first
                if t_first > min_T:
                    min_T = t_first
    
    # Check constraints from '.' cells
    for r in range(h):
        row_str = grid[r]
        for c in range(w):
            if row_str[c] == '.':
                if (r, c) in min_visit:
                    t_first = min_visit[(r, c)]
                    # Constraint: T < t_first  => T <= t_first - 1
                    if t_first - 1 < min_T:
                        # The lower bound from '#' cells forces T to be too high for this '.' cell.
                        print("-1 -1")
                        return
                    if t_first - 1 < max_T:
                        max_T = t_first - 1
    
    # Final check: if min_T > max_T, then no solution.
    if min_T > max_T:
        print("-1 -1")
    else:
        print(f"{min_T} {max_T}")

if __name__ == "__main__":
    solve()