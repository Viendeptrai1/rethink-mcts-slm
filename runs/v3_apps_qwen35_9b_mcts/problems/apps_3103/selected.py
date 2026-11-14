import sys

# Increase recursion depth just in case, though we will use iterative BFS/DFS
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin
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
    for _ in range(Y):
        grid.append(next(iterator))

    # Find the castle position '@'
    castle_pos = None
    for r in range(Y):
        if '@' in grid[r]:
            c = grid[r].index('@')
            castle_pos = (r, c)
            break

    if castle_pos is None:
        # Should not happen based on problem statement
        print("begin repairs")
        return

    start_r, start_c = Y - 1, x_init

    # If start is the castle
    if (start_r, start_c) == castle_pos:
        print(1)
        return

    # BFS to count paths
    # We need to count distinct paths. Since the graph can have cycles (e.g., > < loops),
    # we cannot use standard BFS for counting paths if cycles exist.
    # However, the problem asks for the number of distinct paths.
    # If there are cycles, the number of paths can be infinite.
    # Let's re-read carefully: "how many different routes they can take".
    # Usually in such grid problems with cycles, either:
    # 1. Cycles are not reachable or don't lead to the target in a way that creates infinite paths.
    # 2. We are looking for simple paths (no repeated nodes).
    # 3. The problem implies a DAG structure or specific constraints that prevent infinite loops.
    #
    # Let's analyze the movement rules again:
    # - Move North (r-1, c) is always an option if not '#'.
    # - Move East/West ONLY if there is a current ('>' or '<').
    # - '~' allows only North.
    # - '@' is the target.
    #
    # Can we have a cycle?
    # A cycle would require moving East/West back and forth.
    # Example: Row r has ">>". From (r, 0) -> (r, 1) -> (r, 2). No way back unless there is '<'.
    # If we have "><", from (r, 0) with '>' go to (r, 1). At (r, 1) with '<' go to (r, 0). Cycle!
    # If we can cycle, the number of paths is infinite.
    # But the problem asks for a number modulo 1000003. This implies the answer is finite.
    # Therefore, either:
    # a) The test cases do not contain cycles that can be part of a path to the castle.
    # b) We are only counting simple paths (no repeated vertices).
    #
    # Given the constraints and typical competitive programming patterns, if cycles exist,
    # counting all paths is impossible (infinity). So it must be simple paths.
    # However, counting simple paths is #P-complete in general graphs.
    # But on a grid with specific movement rules, maybe it's manageable?
    # Or perhaps the "cycles" are not reachable from the start or cannot reach the target?
    #
    # Let's reconsider the "Move North" rule.
    # From any cell (r, c) where grid[r][c] != '#', we can go to (r-1, c).
    # This means we can always decrease the row index.
    # To increase the row index, we would need a rule allowing South movement. There isn't one.
    # So, any path must strictly decrease the row index eventually?
    # Not necessarily. We can move East/West on the same row, then move North.
    # But we can NEVER move South.
    # Therefore, a path cannot visit the same row twice?
    # Wait. If I am at row r, move East to (r, c+1), then move North to (r-1, c+1).
    # Can I ever come back to row r? No, because there is no South movement.
    # So, a path can visit each row at most once?
    # Yes! Because the only vertical movement is North (r -> r-1).
    # Once you leave row r to go to r-1, you can never return to row r.
    # This means there are NO cycles in the graph of reachable states!
    # The graph is a DAG (Directed Acyclic Graph) based on row indices.
    # We can use dynamic programming or memoized recursion.
    #
    # State: (r, c)
    # Transitions:
    # 1. If grid[r][c] == '#': No moves.
    # 2. If grid[r][c] == '@': Target reached.
    # 3. If grid[r][c] == '~': Can only move North to (r-1, c).
    # 4. If grid[r][c] == '>': Can move East to (r, c+1) AND North to (r-1, c).
    #    Note: The problem says "Retract the sails and move in the direction of the current".
    #    It doesn't explicitly say you MUST move with the current. It says you CAN use currents.
    #    And "Move north by lowering the sails".
    #    So from '>', you have two choices: follow current (East) OR lower sails (North).
    # 5. If grid[r][c] == '<': Can move West to (r, c-1) AND North to (r-1, c).
    #
    # Since we can never go South, we can process rows from Y-1 down to 0.
    # Or use memoization.
    #
    # Let's verify the "no cycle" logic again.
    # Is it possible to move South? No.
    # Is it possible to move North? Yes.
    # Is it possible to move East/West? Yes, but only on current cells.
    # So in any path, the row index is non-increasing.
    # If the row index stays the same, we move East/West.
    # If we move East/West, we are still on the same row.
    # Can we have a cycle on the same row?
    # Example: "><". (r, 0) -> '>' -> (r, 1) -> '<' -> (r, 0).
    # This is a cycle.
    # But wait, if we have a cycle, we can loop infinitely.
    # Does the problem imply simple paths?
    # "how many different routes they can take".
    # If I can loop 100 times then go North, is that a different route?
    # Usually, "route" implies a sequence of cells. If the sequence repeats, it's the same route?
    # No, a route is a sequence of moves.
    # If I can loop, there are infinite routes.
    # Since the output is a number modulo 1000003, the answer must be finite.
    # This implies that either:
    # 1. Such cycles do not exist in the input (guaranteed by constraints or test data).
    # 2. We are counting simple paths (no repeated vertices).
    #
    # Let's look at the constraints again.
    # "If C[x,y] = '>', then x+1 < X and C[x+1,y] not in {'<', '#'}"
    # "If C[x,y] = '<', then 0 <= x-1 and C[x-1,y] not in {'>', '#'}"
    # These constraints prevent immediate back-and-forth like "><" or "<>"?
    # If I have ">", the next cell cannot be "<". So I can't immediately reverse.
    # But what about ">>><<<"?
    # (r, 0) '>' -> (r, 1) '>' -> (r, 2) '>' -> (r, 3) '<' -> (r, 2) ...
    # At (r, 2), if it is '>', I can go to (r, 3) or (r-1, 2).
    # If I go to (r, 3) ('<'), I go to (r, 2).
    # So I can go (r, 2) -> (r, 3) -> (r, 2). Cycle!
    # The constraint says: if current is '>', next cannot be '<'.
    # So (r, 2) is '>', (r, 3) is '<'. This is allowed?
    # Constraint: "If C[x,y] = '>', then ... C[x+1,y] not in {'<', '#'}"
    # So if (r, 2) is '>', then (r, 3) CANNOT be '<'.
    # So the pattern "><" is forbidden.
    # What about ">>><<<"?
    # (r, 2) is '>', (r, 3) is '<'. Forbidden.
    # So we cannot have a '>' immediately followed by a '<'.
    # Similarly, we cannot have a '<' immediately followed by a '>'.
    # This prevents immediate cycles of length 2.
    # What about longer cycles?
    # ">>><" -> (r, 0)>'->(r,1)>'->(r,2)>'->(r,3)'<'.
    # At (r, 2) ('>'), next is (r, 3) ('<'). Forbidden.
    # So we cannot have a '>' followed by a '<' anywhere.
    # This means all '>' must be followed by '>' or '~' or '@' or end of row.
    # All '<' must be followed by '<' or '~' or '@' or start of row.
    # This implies that on any row, the currents form a sequence like:
    # [some '<'s] ... [some '~'s] ... [some '>'s] ...
    # Because you can't switch from '>' to '<' or vice versa.
    # So the flow on a row is unidirectional!
    # You can move East on a block of '>'s. You can move West on a block of '<'s.
    # But you cannot go back.
    # Example: "<><" is forbidden because '<' followed by '>' is forbidden.
    # Example: "><" is forbidden.
    # Example: ">>" is allowed. "<<" is allowed.
    # So on any row, the movement is strictly monotonic in one direction (or no movement if '~').
    # Therefore, there are NO cycles on any row.
    # And since we can only move North, there are NO cycles in the entire graph.
    # The graph is a DAG.
    # We can use DP.
    #
    # DP State: dp[r][c] = number of ways to reach the castle from (r, c).
    # Base case: dp[castle_r][castle_c] = 1.
    # Transitions:
    # To calculate dp[r][c], we sum up dp[next_r][next_c] for all valid next moves.
    # But wait, we are counting paths FROM start TO castle.
    # It's easier to think forward: dp[r][c] = number of paths from (r, c) to castle.
    # Or backward: dp[r][c] = number of paths from start to (r, c).
    # Let's do forward DP (from start to castle) or backward (from castle to start).
    # Since it's a DAG, we can process in topological order.
    # Topological order: Row Y-1 down to 0. Within a row, order depends on current direction.
    # Actually, since we can move North (r -> r-1) and East/West (c -> c+/-1),
    # and we established no cycles, we can just use memoized recursion.
    #
    # Let's define f(r, c) = number of distinct paths from (r, c) to castle.
    # If (r, c) is '#', f(r, c) = 0.
    # If (r, c) is '@', f(r, c) = 1.
    # Else:
    #   ways = 0
    #   # Move North
    #   if r > 0 and grid[r-1][c] != '#':
    #       ways = (ways + f(r-1, c)) % MOD
    #   # Move East/West based on current
    #   if grid[r][c] == '>':
    #       if c + 1 < X and grid[r][c+1] != '#':
    #           ways = (ways + f(r, c+1)) % MOD
    #   elif grid[r][c] == '<':
    #       if c - 1 >= 0 and grid[r][c-1] != '#':
    #           ways = (ways + f(r, c-1)) % MOD
    #   # Note: '~' and '@' handled. '@' is base case. '~' only moves North.
    #   return ways
    #
    # Wait, what if the castle is not reachable? Then f(start) = 0.
    # Output "begin repairs".
    #
    # One detail: "The boat will not start on a '#' tile".
    # "There is exactly one '@' tile".
    #
    # Let's double check the constraints logic again.
    # "If C[x,y] = '>', then x+1 < X and C[x+1,y] not in {'<', '#'}"
    # This ensures that if you are on a '>', you cannot immediately jump to a '<' or '#'.
    # This prevents the pattern "><" and ">>#".
    # Similarly for '<'.
    # This guarantees that on any row, the sequence of current cells is monotonic.
    # e.g. "<<<~~>>>" or "~~~".
    # So you can traverse a block of '>'s to the right, but you can't turn back.
    # So no cycles.
    #
    # Implementation details:
    # Use a 2D array for memoization. Initialize with -1.
    # MOD = 1000003.

    MOD = 1000003
    memo = [[-1] * X for _ in range(Y)]

    def count_paths(r, c):
        if r < 0 or c < 0 or c >= X:
            return 0
        if grid[r][c] == '#':
            return 0
        if grid[r][c] == '@':
            return 1
        if memo[r][c] != -1:
            return memo[r][c]

        total = 0
        
        # Option 1: Move North
        if r > 0:
            # Check if the cell above is not blocked
            if grid[r-1][c] != '#':
                total = (total + count_paths(r-1, c)) % MOD
        
        # Option 2: Move with current
        cell = grid[r][c]
        if cell == '>':
            if c + 1 < X and grid[r][c+1] != '#':
                total = (total + count_paths(r, c+1)) % MOD
        elif cell == '<':
            if c - 1 >= 0 and grid[r][c-1] != '#':
                total = (total + count_paths(r, c-1)) % MOD
        # If cell is '~', only North is allowed (handled above)
        # If cell is '@', handled at start
        
        memo[r][c] = total
        return total

    result = count_paths(start_r, start_c)
    
    if result == 0:
        print("begin repairs")
    else:
        print(result)

if __name__ == '__main__':
    solve()