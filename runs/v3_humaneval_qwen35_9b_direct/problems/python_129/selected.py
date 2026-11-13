from collections import deque

def minPath(grid, k):
    n = len(grid)
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Find the position of the minimum value (1)
    start_pos = None
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                start_pos = (r, c)
                break
        if start_pos:
            break
    
    # BFS to find the lexicographically smallest path of length k
    # State: (current_value, path)
    # We use BFS level by level to ensure we get paths of exact length k
    # Since we need lexicographically smallest, we process paths in order
    
    # Initial state: start from any cell, but we want the lexicographically smallest path
    # So we should consider all possible starting cells, but prioritize those with smaller values
    # However, the problem says we can start from any cell, and we want the minimum path
    
    # Let's use BFS where each level represents one step
    # We'll keep track of all possible paths of current length
    # But this could be exponential, so we need to be smart
    
    # Actually, since we need the lexicographically smallest path, we can use BFS
    # and at each step, only keep the paths that are lexicographically smallest so far
    # But we need to be careful because a path that is not smallest at step i might become smallest at step i+1
    
    # Better approach: BFS with pruning
    # At each step, we keep all possible paths, but we can prune dominated paths
    # A path A dominates path B if A is lexicographically smaller than B and len(A) == len(B)
    # But we need exactly k steps, so we can't prune too aggressively
    
    # Let's try a different approach: BFS level by level
    # At each level, we keep all possible paths, but we sort them and only keep the ones that could lead to the optimal solution
    # Since we need the lexicographically smallest path, we should prioritize paths with smaller values at each position
    
    # Actually, the key insight is that we want the lexicographically smallest sequence of k values
    # So we can use BFS and at each step, we generate all possible next paths
    # Then we sort them and keep only the necessary ones
    
    # But the state space could be large, so we need to be efficient
    # Let's use BFS with memoization or pruning
    
    # Alternative approach: Since k is likely small (otherwise the problem would be intractable),
    # we can use BFS and keep all paths of current length, but we prune dominated paths
    # A path P1 dominates P2 if P1 is lexicographically smaller than P2 and they have the same length
    # But we need to be careful because we might need to explore multiple paths
    
    # Let's implement BFS with pruning
    # We'll keep a list of all paths of current length, but we'll prune dominated paths
    # A path A dominates path B if A is lexicographically smaller than B
    # But we need to keep paths that could lead to the optimal solution
    
    # Actually, the correct approach is to use BFS and at each step, keep all possible paths
    # But we can prune paths that are lexicographically larger than the current best path of the same length
    # However, we don't know the final answer yet
    
    # Let's try a different approach: BFS level by level, keeping all paths
    # At each level, we sort the paths and only keep the top ones
    # But how many to keep? We don't know
    
    # Insight: Since we want the lexicographically smallest path, at each step we should
    # only keep paths that are lexicographically smallest among all paths of the same length
    # But we need to consider that a path that is not smallest at step i might become smallest at step i+1
    # Actually, no: if path A is lexicographically smaller than path B at step i, then for any extension,
    # A + extension will be lexicographically smaller than B + extension (because the first difference is at step i)
    # So we can safely prune dominated paths
    
    # Therefore, at each step, we only need to keep the lexicographically smallest path(s)
    # But wait, there might be multiple paths that are equally small at step i, but lead to different values at step i+1
    # So we need to keep all paths that are not dominated by any other path of the same length
    
    # Let's implement this:
    # At each step, we have a list of paths (each path is a list of values)
    # We generate all possible next paths by extending each current path with a neighbor
    # Then we sort the new paths and remove dominated ones
    # A path A dominates path B if A is lexicographically smaller than B
    # We keep only the non-dominated paths
    
    # But this could still be exponential in the worst case
    # However, given the constraints and the nature of the problem, this should work
    
    # Let's start with all possible starting cells
    # But we can optimize: we only need to start from cells that could lead to the optimal path
    # The optimal path must start with the smallest possible value, so we should start from the cell with value 1
    # But wait, the problem says we can start from any cell, and the path of length k means visiting exactly k cells
    # So the first cell of the path can be any cell
    
    # Actually, let's reconsider: the lexicographically smallest path of length k
    # The first element of the path should be as small as possible
    # So we should start from the cell with the smallest value, which is 1
    # But what if k=1? Then the answer is [1]
    # What if k>1? Then we start from 1, and then move to the smallest neighbor, etc.
    
    # But wait, the example shows: grid = [[1,2,3], [4,5,6], [7,8,9]], k = 3, output = [1, 2, 1]
    # This path starts at 1, then goes to 2, then back to 1
    # So the path can revisit cells
    
    # So the algorithm is:
    # 1. Start from the cell with value 1 (since we want the lexicographically smallest path)
    # 2. At each step, move to the neighbor with the smallest value
    # 3. If there are multiple neighbors with the same smallest value, we need to consider all of them
    #    But actually, since we want the lexicographically smallest path, we should choose the one that leads to the smallest next value
    #    But the next value is determined by the neighbor we choose, so we should choose the neighbor with the smallest value
    
    # However, the example shows that after 1, 2, we go back to 1, not to 3
    # So the path is [1, 2, 1], which is lexicographically smaller than [1, 2, 3]
    
    # So the greedy approach of always choosing the smallest neighbor might not work
    # We need to explore all possibilities and find the lexicographically smallest path
    
    # Let's use BFS with pruning
    # We'll keep all paths of current length, but we'll prune dominated paths
    # A path A dominates path B if A is lexicographically smaller than B
    # We keep only the non-dominated paths
    
    # Start with all possible starting cells
    # But we can optimize: we only need to start from cells that could lead to the optimal path
    # The optimal path must start with the smallest possible value, so we should start from the cell with value 1
    # But what if the optimal path doesn't start with 1? 
    # Actually, the lexicographically smallest path must start with the smallest possible value, which is 1
    # So we only need to start from the cell with value 1
    
    # Wait, but the problem says "You can start from any cell"
    # And the lexicographically smallest path of length k
    # The first element of the path should be as small as possible
    # So the optimal path must start with the smallest value in the grid, which is 1
    
    # So we only need to start from the cell with value 1
    
    # Let's implement BFS starting from the cell with value 1
    # At each step, we generate all possible next paths by moving to neighbors
    # Then we sort the paths and remove dominated ones
    # A path A dominates path B if A is lexicographically smaller than B
    # We keep only the non-dominated paths
    
    # But we need to be careful: the state space could be large
    # However, given the constraints and the nature of the problem, this should work
    
    # Let's start
    # Initial state: all paths of length 1 starting from the cell with value 1
    # But wait, we can start from any cell, but the optimal path must start with the smallest value
    # So we only need to consider starting from the cell with value 1
    
    # Actually, let's reconsider: what if k=1? Then the answer is [1]
    # What if k>1? Then we start from 1, and then move to the smallest neighbor, etc.
    # But the example shows that after 1, 2, we go back to 1, not to 3
    # So the path is [1, 2, 1], which is lexicographically smaller than [1, 2, 3]
    
    # So the algorithm is:
    # 1. Start from the cell with value 1
    # 2. At each step, generate all possible next paths by moving to neighbors
    # 3. Sort the paths and remove dominated ones
    # 4. Repeat until we have k steps
    
    # But we need to handle the case where k=1 separately
    if k == 1:
        # Find the minimum value in the grid
        min_val = min(val for row in grid for val in row)
        return [min_val]
    
    # Start from the cell with value 1
    start_val = 1
    start_pos = None
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                start_pos = (r, c)
                break
        if start_pos:
            break
    
    # BFS: each element is a path (list of values)
    # We start with paths of length 1
    paths = [[start_val]]
    
    for step in range(1, k):
        new_paths = []
        for path in paths:
            r, c = start_pos
            # We need to track the current position, but the path only contains values
            # So we need to recompute the position or store it in the path
            # Let's change the path to include positions as well
            pass
        
        # Actually, we need to track positions, so let's change the path format
        # Path will be a list of (value, position) tuples
        # But we only need to return the values, so we can convert at the end
        
        # Let's restart with the correct format
        # paths will be a list of lists, where each inner list contains (value, position) tuples
        # But we only need to return the values, so we can convert at the end
        
        # Actually, let's keep it simple: paths will be a list of lists of values
        # And we'll track the current position separately
        # But we need to know the current position to move to neighbors
        
        # Let's change the approach: each state is (path, current_position)
        # But this could be memory-intensive
        
        # Alternative: at each step, we have a list of (path, current_position)
        # We generate all possible next states by moving to neighbors
        # Then we sort and prune
        
        # Let's implement this
        new_states = []
        for path, (r, c) in zip(paths, [start_pos] * len(paths)):
            # This is wrong because paths is a list of paths, not (path, position)
            pass
        
        # Let's restart with the correct approach
        # We'll use a list of (path, current_position) where path is a list of values
        # And current_position is (r, c)
        
        # Initial state: all paths of length 1 starting from the cell with value 1
        # But we only have one starting cell (the one with value 1)
        # So we start with one state: ([1], start_pos)
        
        # Wait, but the problem says we can start from any cell
        # But the optimal path must start with the smallest value, which is 1
        # So we only need to start from the cell with value 1
        
        # Let's implement BFS with states (path, current_position)
        # Each state is a tuple: (path, (r, c))
        # path is a list of values
        
        # Initial state
        states = [([start_val], start_pos)]
        
        for step in range(1, k):
            new_states = []
            for path, (r, c) in states:
                # Try all neighbors
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        new_val = grid[nr][nc]
                        new_path = path + [new_val]
                        new_states.append((new_path, (nr, nc)))
            
            # Now prune dominated states
            # A state (path1, pos1) dominates (path2, pos2) if path1 is lexicographically smaller than path2
            # We keep only the non-dominated paths
            
            # Sort the states by path
            new_states.sort(key=lambda x: x[0])
            
            # Remove dominated states
            # We keep only the first occurrence of each unique path prefix
            # But actually, we need to keep all paths that are not dominated by any other path
            # Since we sorted by path, the first path is the smallest, and we keep it
            # Then we check if the second path is dominated by the first, etc.
            
            # Actually, since we sorted by path, if path[i] < path[j] for i < j, then path[i] dominates path[j]
            # So we only need to keep the first occurrence of each unique path
            # But wait, two different paths could be equal up to some point and then differ
            # In that case, the one that is smaller at the first difference dominates the other
            
            # Since we sorted by path, the first path is the smallest, and we keep it
            # Then we check if the second path is equal to the first, if so, we skip it (dominated)
            # Otherwise, we keep it
            
            # But actually, we need to keep all paths that are not dominated by any other path
            # Since we sorted by path, if path[i] < path[j] for i < j, then path[i] dominates path[j]
            # So we only need to keep the first occurrence of each unique path
            
            # Let's implement this
            unique_paths = []
            if new_states:
                unique_paths.append(new_states[0][0])
                for i in range(1, len(new_states)):
                    if new_states[i][0] != unique_paths[-1]:
                        unique_paths.append(new_states[i][0])
            
            # Now we have the unique paths, but we need to keep the corresponding states
            # Actually, we need to keep all states that have these unique paths
            # But since we sorted by path, all states with the same path are consecutive
            # So we can group by path and keep one state per unique path
            
            # But which state to keep? Any state with that path is fine, because the path is the same
            # So we can keep the first state for each unique path
            
            # Let's rebuild the states list
            filtered_states = []
            if new_states:
                filtered_states.append(new_states[0])
                for i in range(1, len(new_states)):
                    if new_states[i][0] != new_states[i-1][0]:
                        filtered_states.append(new_states[i])
            
            states = filtered_states
        
        # After k-1 steps, we have paths of length k
        # We need to find the lexicographically smallest path
        # Since we've been pruning dominated paths, the first path in states should be the smallest
        if states:
            best_path = states[0][0]
            return best_path
    
    # If k=1, we already handled it above
    return [start_val]