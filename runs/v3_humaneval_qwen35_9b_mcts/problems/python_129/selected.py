from collections import deque

def minPath(grid, k):
    n = len(grid)
    # Map value to (row, col)
    val_to_pos = {}
    for r in range(n):
        for c in range(n):
            val_to_pos[grid[r][c]] = (r, c)
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # We need the lexicographically smallest path of length k.
    # Since k can be up to N*N and N is at least 2, but the grid contains values 1..N*N,
    # and we want the lexicographically smallest sequence, the optimal strategy is:
    # At each step, try to move to a neighbor that has the smallest possible value.
    # However, we can also stay in the same cell? The problem says "move to any of the neighbor cells".
    # "Neighbor cells" usually implies distinct cells sharing an edge. But the example [1,2,3], [4,5,6], [7,8,9], k=3 -> [1,2,1]
    # Wait, the example output is [1, 2, 1]. 
    # Path: Start at 1 (0,0). Move to 2 (0,1). Then move to 1? 
    # If we can only move to neighbors, from (0,1) [value 2], neighbors are 1 (0,0), 3 (0,2), 5 (1,1).
    # So moving back to 1 is allowed.
    # The path is a sequence of k cells.
    # Lexicographical comparison: compare element by element.
    # To minimize the list, we want the first element to be as small as possible.
    # Then the second, etc.
    # Since we can start anywhere, the first element of our path should be the minimum value in the grid, which is 1.
    # Then from the current cell, we should choose the neighbor that leads to the smallest next value.
    # Actually, since we want the entire list to be lexicographically smallest, at each step i (from 0 to k-2),
    # given the current cell, we should pick the neighbor that has the minimum value.
    # Why? Because the value at index i+1 in the path list is determined solely by the choice of the next cell.
    # To make the list lexicographically smallest, we must minimize the value at index 1, then index 2, etc.
    # Greedy approach:
    # 1. Start at the cell with value 1 (since 1 is the smallest possible value and we can start anywhere).
    # 2. For the next k-1 steps, from the current cell, move to the adjacent neighbor with the smallest value.
    # 3. If there are multiple neighbors with the same smallest value, does it matter which one we pick?
    #    The value added to the list is the same. The future values might differ.
    #    However, the problem guarantees a unique answer. This implies that either:
    #      a) The greedy choice of value is sufficient and the tie-breaking doesn't affect the final list values, OR
    #      b) The structure of the grid and values ensures that the path of values is unique regardless of tie-breaking in position, OR
    #      c) We need to look ahead.
    #    Let's re-read: "It is guaranteed that the answer is unique."
    #    If we have a choice between two neighbors with value V, and one leads to a sequence [V, 10, 20] and the other [V, 5, 100],
    #    then [V, 5, 100] is lexicographically smaller. So simple greedy on immediate neighbor value might fail if ties exist.
    #    BUT, the values in the grid are a permutation of 1 to N*N.
    #    Is it possible to have two neighbors with the same value? No, all values are distinct.
    #    Therefore, at any cell, the neighbors have distinct values.
    #    So the greedy strategy is strictly deterministic: always move to the neighbor with the minimum value.
    
    # Step 1: Find the starting cell (value 1)
    start_r, start_c = val_to_pos[1]
    
    # Step 2: Build the path
    path = []
    curr_r, curr_c = start_r, start_c
    
    for _ in range(k):
        path.append(grid[curr_r][curr_c])
        
        # Find the best next move
        best_val = float('inf')
        best_next_r, best_next_c = -1, -1
        
        for dr, dc in directions:
            nr, nc = curr_r + dr, curr_c + dc
            if 0 <= nr < n and 0 <= nc < n:
                val = grid[nr][nc]
                if val < best_val:
                    best_val = val
                    best_next_r, best_next_c = nr, nc
        
        # Move to the best neighbor
        curr_r, curr_c = best_next_r, best_next_c
        
    return path

# Test with provided examples
# grid = [[1,2,3], [4,5,6], [7,8,9]], k = 3
# Start at 1. Neighbors of 1 are 2 and 4. Min is 2. Path: [1, 2].
# Current at 2. Neighbors of 2 are 1, 3, 5. Min is 1. Path: [1, 2, 1].
# Result: [1, 2, 1]. Matches example.

# grid = [[5,9,3], [4,1,6], [7,8,2]], k = 1
# Start at 1. Path: [1]. Matches example.