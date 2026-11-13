import sys

# Increase recursion depth just in case, though we will use an iterative approach with explicit stack management if needed.
# However, given the grid size (300x50000), a simple DFS with recursion might hit limits if the path is very long or branching is huge.
# We will use an iterative DFS to be safe and efficient.
sys.setrecursionlimit(500000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        Y = int(next(iterator))
        X = int(next(iterator))
        x_init = int(next(iterator))
    except StopIteration:
        return

    grid = []
    # Read Y rows, each row is a string of length X
    # Note: The problem says "Then follow Y rows, each with X characters each".
    # Sometimes split() might break if there are spaces, but the grid characters are '~', '#', '@', '>', '<'. No spaces.
    # So we can safely read Y strings.
    for _ in range(Y):
        grid.append(next(iterator))

    # Directions:
    # North: (-1, 0) -> This is moving UP the grid (row index decreases)
    # South: (1, 0) -> Not explicitly mentioned as a primary move, but "Move north by lowering the sails" implies we can go North.
    # Wait, the problem says:
    # "Move north by lowering the sails" -> This is a deliberate action Lysias takes.
    # "Retract the sails and move in the direction of the current... (east/west)"
    # So from any cell, we can:
    # 1. Move North (row - 1) if within bounds.
    # 2. Move East or West based on the current symbol if present.
    #
    # Currents:
    # '>' at (x, y) moves to (x+1, y)
    # '<' at (x, y) moves to (x-1, y)
    # '~' means no current, so retracting sails does nothing? Or does it mean we can't move East/West?
    # The problem says: "Retract the sails and move in the direction of the current they're on top of".
    # If there is no current (~), retracting sails does not move the ship East/West.
    # So effectively:
    # - If cell is '~': Can only move North (if valid). Cannot move East/West.
    # - If cell is '#': Impassable.
    # - If cell is '@': Destination.
    # - If cell is '>': Moves East (x+1). Can we also move North? Yes, "Move north by lowering the sails" seems to be a universal action regardless of current, 
    #   because lowering sails stops the wind (south wind pushing south) but allows current to act or lets the ship drift north?
    #   Let's re-read carefully: "the engines capable of turning the sails failed... south wind... blowing them in the right direction... at least approximately."
    #   "Lysias believes he can use the ocean's currents to move the ship either east or west temporarily by retracting and lowering the ship's sails."
    #   "In that way, the ship can move in two potential directions:
    #    - Move north by lowering the sails
    #    - Retract the sails and move in the direction of the current..."
    #
    # Interpretation:
    # Action 1: Lower sails -> Move North (against the south wind). This is always an option if the cell is not '#'.
    # Action 2: Retract sails (stop wind) -> Move with current (East or West). This is only possible if there is a current ('>' or '<').
    #
    # So from a cell (r, c):
    # - If grid[r][c] == '#': Invalid cell.
    # - Option A: Move to (r-1, c) if r-1 >= 0 and grid[r-1][c] != '#'.
    # - Option B: If grid[r][c] == '>': Move to (r, c+1). Check bounds and if target is not '#'.
    # - Option B: If grid[r][c] == '<': Move to (r, c-1). Check bounds and if target is not '#'.
    #
    # We need to count distinct paths from (Y-1, x_init) to the position of '@'.
    # Since we need the number of paths modulo 1000003, and the graph is a DAG (we only move North, East, West? Wait, West moves back? Or East moves back?)
    #
    # Wait, if we have '>' at (x, y), we move to (x+1, y). If that cell has '<', we move to (x, y). That would be a cycle.
    # BUT the constraints say:
    # "If C[x,y] = '>', then x+1 < X and C[x+1,y] not in {'<', '#'}"
    # "If C[x,y] = '<', then 0 <= x-1 and C[x-1,y] not in {'>', '#'}"
    # This constraint ensures that if you are pushed East, the next cell is not a West current (so you don't bounce back immediately).
    # However, could there be a cycle like A -> B -> C -> A?
    # Moves are: North (r-1), East (c+1), West (c-1).
    # If we keep moving North, we eventually hit row 0.
    # If we move East/West, we stay in the same row.
    # Can we have a cycle in the same row?
    # If we are at (r, c) and move East to (r, c+1), then from (r, c+1) can we move West back to (r, c)?
    # Only if (r, c+1) has '<'. But the constraint says if (r, c) is '>', then (r, c+1) is NOT '<'. So we cannot bounce back immediately.
    # What about (r, c) -> (r, c+1) -> (r, c+2) -> ... -> (r, c+k) -> ... -> (r, c)?
    # Since currents only push in one direction per cell, and you can't reverse immediately, it's hard to form a cycle in a single row unless there's a sequence like > > < < which is forbidden by the constraints (adjacent opposites forbidden).
    # Actually, the constraint is only for immediate neighbors. What about (r, c)='>', (r, c+1)='>', (r, c+2)='<', (r, c+3)='<'?
    # Path: c -> c+1 (via >) -> c+2 (via >) -> c+1 (via < at c+2? No, constraint says if c+2 is '<', then c+1 cannot be '>').
    # So the constraint "If C[x,y] = '<', then ... C[x-1,y] not in {'>', '#'}" prevents a '<' from being immediately followed by a '>'.
    # Similarly, '>' prevents '<' immediately after.
    # This means in any row, the currents must be monotonic segments? Like > > > > then < < < <? No, because > can't be followed by <, and < can't be followed by >.
    # So a row can look like: ~ ~ > > > ~ < < < ~ ~
    # But wait, if we have > > >, then at the third >, we go to the next cell. If the next cell is <, that's forbidden.
    # So once you enter a sequence of >, you cannot exit to a < immediately. You must exit to ~ or @ or #.
    # Once you exit to ~, you can't go back East/West unless you find another current later.
    # Can you go East, then West later?
    # Example: Row: > > ~ < <
    # Start at index 0 ('>'). Move to 1 ('>'). Move to 2 ('~').
    # From 2 ('~'), can we move West? No, '~' has no current.
    # Can we move North from 2? Yes.
    # So to move West, we must be on a cell with '<'.
    # If we are at index 3 ('<'), we move to 2. But we came from 2 via North then East? No, we were at 2 (from 1 via >).
    # Can we go 2 -> 3? No, 2 is '~', no current.
    # So we can never reach the '<' at index 3 from the left if we came from the left via '>'s?
    # Unless we came from the right? But we start somewhere.
    # Basically, in a single row, you can only traverse a contiguous block of currents in one direction.
    # And since '>' cannot be followed by '<', and '<' cannot be followed by '>', the currents in a row are separated by '~' or boundaries.
    # Within a block of '>'s, you move East. Within a block of '<'s, you move West.
    # You can never go East then West in the same row because to go West you need a '<', but you can only reach a '<' from a '~' (by moving North then South? No, can't move South) or from the right?
    # Wait, can we move South? The problem doesn't say we can move South.
    # "Move north by lowering the sails" -> Only North is explicit as a voluntary move.
    # Currents move East/West.
    # There is NO South move.
    # Therefore, we can never increase the row index. We only decrease row index (North) or stay same (East/West via currents).
    # This confirms it is a DAG (Directed Acyclic Graph) because row index never increases, and within the same row, cycles are impossible due to the constraints on adjacent currents.
    # So simple DFS/BFS counting paths works.

    # Find target
    target_r, target_c = -1, -1
    for r in range(Y):
        if '@' in grid[r]:
            target_r, target_c = r, grid[r].index('@')
            break

    if target_r == -1:
        # Should not happen based on problem statement
        print("begin repairs")
        return

    start_r, start_c = Y - 1, x_init

    # If start is target?
    if start_r == target_r and start_c == target_c:
        # One path: start is end.
        # But usually "get back to" implies movement? 
        # However, mathematically, a path of length 0 exists.
        # Let's assume 1 path.
        print(1 % 1000003)
        return

    # Memoization or DP?
    # Since it's a DAG and we want number of paths, we can use DP or DFS with memoization.
    # State: (r, c)
    # Since we can only go North, East, West, and row decreases monotonically, we can process row by row?
    # No, because from (r, c) we can go to (r, c+1) which is same row.
    # But we can't go back to (r, c) from (r, c+1) due to constraints.
    # So within a row, the dependency is linear?
    # Actually, from (r, c) we can go to (r, c+1) (if '>') or (r, c-1) (if '<').
    # This looks like we might have chains within a row.
    # Example: > > > (indices 0,1,2). 0->1->2.
    # Also from 2 we can go North to (1,2). From (1,2) we can go West to (1,1) etc.
    # So dependencies flow: (r, c) -> (r, c+1) -> ... -> (r, c+k) -> (r-1, c+k) -> ...
    # Since row index never increases, we can compute DP row by row from 0 to Y-1?
    # No, the path starts at Y-1 and goes to some row.
    # The target is at some row.
    # We want paths from Start to Target.
    # Since edges go North (r-1) or Horizontal (same r), we can think of it as:
    # To compute ways(r, c), we need ways(r-1, c) [if we came from South? No, we move North, so we arrive at (r,c) from (r+1,c)]
    # Wait, let's define DP[i][j] = number of paths from Start (Y-1, x_init) to (i, j).
    # But the graph is directed: Start -> ... -> Target.
    # We want to sum up paths.
    # Since we can only move to lower row indices or same row (but strictly forward/backward in a way that prevents cycles),
    # We can use memoized DFS.
    # Visited set to prevent cycles? Cycles shouldn't exist, but visited is good for safety.
    # But we need to count paths, not just reachability. So we need memoization of the count.

    MOD = 1000003
    memo = {}
    
    # Check if start is valid
    if grid[start_r][start_c] == '#':
        # Problem says "The boat will not start on a '#' tile"
        pass

    def get_paths(r, c):
        if (r, c) in memo:
            return memo[(r, c)]
        
        # If current cell is obstacle
        if grid[r][c] == '#':
            memo[(r, c)] = 0
            return 0
        
        # If current cell is target, we reached it. 
        # But we count the path ending here. So 1 path ends here.
        # However, this function returns number of paths FROM (r,c) TO Target?
        # Or TO (r,c) FROM Start?
        # Let's do: count paths FROM (r,c) TO Target.
        # Then answer is get_paths(start_r, start_c).
        
        if r == target_r and c == target_c:
            memo[(r, c)] = 1
            return 1

        total = 0
        
        # Option 1: Move North
        nr, nc = r - 1, c
        if nr >= 0:
            if grid[nr][nc] != '#':
                total = (total + get_paths(nr, nc)) % MOD
        
        # Option 2: Move with Current
        # Check current at (r, c)
        cell = grid[r][c]
        if cell == '>':
            # Move East
            nc = c + 1
            if nc < X:
                if grid[r][nc] != '#':
                    total = (total + get_paths(r, nc)) % MOD
        elif cell == '<':
            # Move West
            nc = c - 1
            if nc >= 0:
                if grid[r][nc] != '#':
                    total = (total + get_paths(r, nc)) % MOD
        # If '~', no horizontal move.

        memo[(r, c)] = total
        return total

    result = get_paths(start_r, start_c)
    
    if result == 0:
        print("begin repairs")
    else:
        print(result)

if __name__ == '__main__':
    solve()