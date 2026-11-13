import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        K = int(next(iterator))
        
        trap_r = int(next(iterator))
        trap_c = int(next(iterator))
        
        # Directions: 0: Up, 1: Right, 2: Down, 3: Left
        # Mapping characters to indices
        dir_map = {'U': 0, 'R': 1, 'D': 2, 'L': 3}
        dir_chars = ['U', 'R', 'D', 'L']
        
        # Store grid for each bacterium
        # grids[b_idx][r][c] = digit
        grids = []
        
        for b_idx in range(K):
            start_r = int(next(iterator))
            start_c = int(next(iterator))
            start_dir_char = next(iterator)
            start_dir = dir_map[start_dir_char]
            
            grid = []
            for r in range(N):
                row_str = next(iterator)
                row_digits = [int(ch) for ch in row_str]
                grid.append(row_digits)
            
            grids.append({
                'r': start_r - 1,
                'c': start_c - 1,
                'dir': start_dir,
                'grid': grid
            })
            
    except StopIteration:
        return

    # Simulation
    # We need to detect if any bacterium enters the trap cell at the same time step.
    # Max steps? Since board is small (50x50) and K is small (5), cycles might occur.
    # If we simulate too long without hitting trap, it's likely infinite.
    # Let's set a reasonable limit. State space per bacterium: pos(2500) * dir(4) = 10000.
    # With K=5, total state is huge, but we only care about simultaneous arrival.
    # If no one hits trap within a certain number of steps, and patterns repeat, it won't happen.
    # Given constraints and problem type, 10000 steps should be enough to detect cycles or solution.
    # Actually, let's use a slightly larger safe bound or cycle detection per bacterium.
    # However, the condition is "all step on that cell in the same second".
    # If we run for a sufficiently large number of steps (e.g., 20000) and haven't seen it, output -1.
    # Why 20000? Period of movement is at most LCM of cycle lengths. Max cycle length per bacterium is 2500*4 = 10000.
    # LCM could be large, but practically for these constraints, if it doesn't happen quickly, it won't.
    # Let's use 50000 to be safe.
    
    MAX_STEPS = 50000
    
    for step in range(1, MAX_STEPS + 1):
        current_positions = []
        all_at_trap = True
        
        for b in grids:
            r, c, d = b['r'], b['c'], b['dir']
            grid = b['grid']
            
            # Read X
            x_val = grid[r][c]
            
            # Turn 90 degrees clockwise X times
            # Clockwise: U->R->D->L->U (0->1->2->3->0)
            d = (d + x_val) % 4
            
            # Check if facing outside
            # If facing outside, turn 180 degrees
            facing_out = False
            if d == 0 and r == 0: # Up from row 0
                facing_out = True
            elif d == 1 and c == M - 1: # Right from col M-1
                facing_out = True
            elif d == 2 and r == N - 1: # Down from row N-1
                facing_out = True
            elif d == 3 and c == 0: # Left from col 0
                facing_out = True
            
            if facing_out:
                d = (d + 2) % 4
            
            # Move
            if d == 0:
                nr, nc = r - 1, c
            elif d == 1:
                nr, nc = r, c + 1
            elif d == 2:
                nr, nc = r + 1, c
            elif d == 3:
                nr, nc = r, c - 1
            
            # Update position
            b['r'] = nr
            b['c'] = nc
            b['dir'] = d
            
            current_positions.append((nr, nc))
            
            if (nr, nc) != (trap_r - 1, trap_c - 1):
                all_at_trap = False
        
        if all_at_trap:
            print(step)
            return

    print("-1")

if __name__ == "__main__":
    solve()