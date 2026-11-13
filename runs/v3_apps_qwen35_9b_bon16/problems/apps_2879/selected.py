import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    h = int(input_data[0])
    w = int(input_data[1])
    
    grid = []
    idx = 2
    for i in range(h):
        row_str = input_data[idx]
        idx += 1
        grid.append(row_str)
    
    # Collect coordinates of all 'X's
    cells = []
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 'X':
                cells.append((r, c))
    
    if not cells:
        # No cells, technically no solution as k>=2 requires at least 2 cells
        print("No solution")
        return

    # Try all possible values of k from 2 to 5
    for k in range(2, 6):
        # Check if total number of cells is divisible by k
        if len(cells) % k != 0:
            continue
        
        base_size = len(cells) // k
        
        # We need to find a base polyomino of size `base_size` that can tile the given shape `k` times
        # using only translations (no rotation, no mirroring).
        
        # Generate all possible base polyominoes that fit within the bounding box and have size `base_size`
        # Since h, w <= 10 and base_size is small, we can brute force sub-shapes.
        
        # However, a more efficient approach for small constraints:
        # Iterate over all possible subsets of `cells` of size `base_size` as candidate base pieces.
        # But there might be many combinations. Let's optimize by fixing the first cell of the base piece to be the first cell of the global list to avoid duplicates due to translation.
        
        # Actually, since we are tiling the EXACT shape given, the base piece must be a subset of `cells`.
        # So we iterate over all combinations of `cells` of size `base_size`.
        # To reduce redundancy (translation equivalence), we can fix the top-left-most cell of the base piece to match the top-left-most cell of the global `cells`.
        
        # Sort cells for consistent ordering
        sorted_cells = sorted(cells)
        
        from itertools import combinations
        
        # Find the index of the first cell (top-left-most)
        first_cell = sorted_cells[0]
        
        # Generate candidates: subsets of size base_size that include first_cell
        # This ensures we only consider shapes that can be translated to cover the whole set starting from first_cell
        candidates = combinations(sorted_cells, base_size)
        
        for candidate in candidates:
            # Check if first_cell is in candidate
            if first_cell not in candidate:
                continue
            
            # Convert candidate tuple to a set for easy lookup
            base_set = set(candidate)
            
            # Verify connectivity of the base_set
            if not is_connected(base_set):
                continue
            
            # Now try to tile the full set with k translations of base_set
            # We need to find k vectors (dr, dc) such that:
            # 1. Each translation T_i = {(r+dr, c+dc) | (r,c) in base_set} is a subset of cells
            # 2. The union of all T_i is exactly cells
            # 3. All T_i are disjoint
            
            # Since k is small (up to 5) and the grid is small, we can try to find the translation vectors.
            # The translation vector for a piece must be such that when added to the base_set, it lands in `cells`.
            # Specifically, for a piece to be a translation of base_set, there exists a vector v such that
            # base_set + v == subset_of_cells.
            # The vector v is determined by matching the first cell.
            # Let the first cell of base_set be b0. Then the translation vector v = t - b0 for some t in cells.
            
            # Get the first cell of the base piece (which is fixed as first_cell relative to base coordinates, but in global coords it's first_cell)
            # Wait, base_set is a set of global coordinates. The "first" cell in base_set (by sorted order) is first_cell.
            # So any translation of this base_set must map first_cell to some target t in cells.
            # The translation vector would be v = (t_r - first_cell_r, t_c - first_cell_c).
            
            # Collect all possible translation vectors that map first_cell to some cell in `cells`
            possible_vectors = []
            for t in cells:
                dr = t[0] - first_cell[0]
                dc = t[1] - first_cell[1]
                possible_vectors.append((dr, dc))
            
            # We need to choose k vectors from possible_vectors (with replacement? No, pieces are identical but placed at different locations, so vectors can be same? 
            # If vectors are same, pieces overlap. Since pieces must be disjoint, vectors must be distinct relative to the base shape structure? 
            # Actually, if we use the same vector twice, the two resulting sets of coordinates are identical, so they overlap completely. 
            # Thus, all k translation vectors must be distinct.
            
            # We need to select k distinct vectors from possible_vectors such that the union of translated base_sets covers `cells` exactly.
            
            from itertools import combinations as itertools_combinations
            
            # Optimization: If number of possible vectors is less than k, skip
            if len(possible_vectors) < k:
                continue
            
            # Try all combinations of k vectors
            for vecs in itertools_combinations(possible_vectors, k):
                # Check if these k vectors tile the `cells` exactly
                current_union = set()
                valid = True
                mapping = {} # Map each cell to its piece ID (1..k)
                
                for i, vec in enumerate(vecs):
                    # Generate the piece at this vector
                    piece_coords = set()
                    for (r, c) in base_set:
                        nr, nc = r + vec[0], c + vec[1]
                        if (nr, nc) not in cells:
                            valid = False
                            break
                        piece_coords.add((nr, nc))
                    if not valid:
                        break
                    
                    # Check overlap with already placed pieces
                    for coord in piece_coords:
                        if coord in current_union:
                            valid = False
                            break
                    if not valid:
                        break
                    current_union.update(piece_coords)
                
                if not valid:
                    continue
                
                if current_union == cells:
                    # Found a solution!
                    # Construct the output grid
                    output_grid = [['.' for _ in range(w)] for _ in range(h)]
                    
                    # Assign IDs to cells
                    # We need to map each cell in `cells` to an ID 1..k
                    # Since we have `vecs` and `base_set`, we can determine which piece covers which cell.
                    # However, multiple vectors might produce the same piece? No, we selected distinct vectors.
                    # But different vectors could theoretically produce overlapping pieces if not checked. We checked disjointness.
                    
                    # To assign IDs correctly:
                    # For each vector in vecs, assign a unique ID (1 to k)
                    # Then for each cell in the translated base_set, assign that ID.
                    
                    # But wait: what if the base_set itself has symmetries? 
                    # The problem says "identifying the factor pieces". As long as the pieces are distinguished by the numbers, it's fine.
                    # We just need to ensure that each connected component in the output (formed by same numbers) corresponds to one base piece.
                    
                    # Let's create a mapping from coordinate to piece index
                    coord_to_piece = {}
                    piece_id = 0
                    for idx_vec, vec in enumerate(vecs):
                        piece_id += 1
                        for (r, c) in base_set:
                            nr, nc = r + vec[0], c + vec[1]
                            coord_to_piece[(nr, nc)] = piece_id
                    
                    # Fill the grid
                    for (r, c) in cells:
                        pid = coord_to_piece[(r, c)]
                        output_grid[r][c] = str(pid)
                    
                    # Print the result
                    for row in output_grid:
                        print("".join(row))
                    return

    print("No solution")

def is_connected(shape_set):
    if not shape_set:
        return False
    start = next(iter(shape_set))
    stack = [start]
    visited = set([start])
    while stack:
        curr = stack.pop()
        r, c = curr
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in shape_set and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append((nr, nc))
    return len(visited) == len(shape_set)

if __name__ == "__main__":
    solve()