import sys

def solve():
    try:
        input_data = sys.stdin.read().split()
    except Exception:
        return

    if not input_data:
        return

    iterator = iter(input_data)
    try:
        h = int(next(iterator))
        w = int(next(iterator))
        grid = []
        for _ in range(h):
            grid.append(next(iterator))
    except StopIteration:
        return

    # Parse the grid into a set of (r, c) coordinates
    cells = set()
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 'X':
                cells.add((r, c))

    if len(cells) == 0:
        print("No solution")
        return

    # Try k from 2 to 5
    for k in range(2, 6):
        if len(cells) % k != 0:
            continue

        base_size = len(cells) // k
        if base_size < 1:
            continue

        # Generate all unique sub-polyominoes of size base_size from the grid
        # We will try every possible subset of 'base_size' cells that forms a connected component
        # However, generating all subsets is expensive. Instead, we can try to find a base shape
        # by fixing one cell as the "origin" of the base and trying to grow it.
        # But a simpler approach for small constraints (h,w <= 10, base_size <= 25) is:
        # Iterate over all possible base shapes that are subsets of 'cells' with size 'base_size'.
        # To avoid TLE, we can use a recursive backtracking to find connected components of size base_size.

        # Let's collect all connected components of size base_size within the 'cells' set.
        # We do this by iterating over each cell as a potential start of a base component.
        # To avoid duplicates, we enforce an ordering (e.g., the cell with the smallest index must be the first).

        base_components = []

        # Sort cells to have a deterministic order
        sorted_cells = sorted(cells)

        # Recursive function to find connected components of size base_size
        def find_components(start_idx, current_set, visited_global):
            if len(current_set) == base_size:
                # Check connectivity
                # BFS from the first element in current_set
                start_node = min(current_set)
                q = [start_node]
                visited_comp = {start_node}
                idx = 0
                while idx < len(q):
                    node = q[idx]
                    idx += 1
                    r, c = node
                    # Check neighbors in current_set
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nr, nc = r + dr, c + dc
                        if (nr, nc) in current_set and (nr, nc) not in visited_comp:
                            visited_comp.add((nr, nc))
                            q.append((nr, nc))
                if len(visited_comp) == base_size:
                    return [tuple(sorted(current_set))]
                return []
            
            if start_idx >= len(sorted_cells):
                return []

            # Optimization: if remaining cells are not enough
            remaining = len(sorted_cells) - start_idx
            if remaining < base_size - len(current_set):
                return []

            results = []
            # Option 1: Include sorted_cells[start_idx]
            next_cell = sorted_cells[start_idx]
            # Check if adding next_cell maintains connectivity with current_set
            # If current_set is empty, just add it.
            # If not empty, check if next_cell is adjacent to any node in current_set
            can_add = False
            if not current_set:
                can_add = True
            else:
                for node in current_set:
                    r, c = node
                    nr, nc = next_cell
                    if abs(r - nr) + abs(c - nc) == 1:
                        can_add = True
                        break
            
            if can_add:
                new_set = current_set | {next_cell}
                sub_results = find_components(start_idx + 1, new_set, visited_global)
                results.extend(sub_results)
            
            # Option 2: Skip sorted_cells[start_idx]
            # Only skip if we haven't reached the start of the component (to avoid duplicates)
            # Actually, standard subset generation with connectivity check is tricky.
            # Let's refine: We fix the "root" of the component to be the cell with the minimum index in the component.
            # So when we are at start_idx, if sorted_cells[start_idx] is not in current_set, we MUST include it if we want it to be the root?
            # No, the root is defined as the minimum index in the final set.
            # So if we are building a set and the current minimum candidate is sorted_cells[start_idx], 
            # and sorted_cells[start_idx] is NOT in current_set, then we MUST include it to make it the root?
            # Not necessarily, we could have skipped it and picked a smaller one earlier? 
            # But we iterate start_idx from 0. If we skipped sorted_cells[0], then the root must be >= sorted_cells[1].
            # So the logic is:
            # If current_set is empty, we MUST pick sorted_cells[start_idx] as the first element (the root).
            # If current_set is not empty, we can either pick sorted_cells[start_idx] (if connected) or skip it.
            
            if not current_set:
                # Must pick
                new_set = {next_cell}
                sub_results = find_components(start_idx + 1, new_set, visited_global)
                results.extend(sub_results)
            else:
                # Try including
                if can_add:
                    new_set = current_set | {next_cell}
                    sub_results = find_components(start_idx + 1, new_set, visited_global)
                    results.extend(sub_results)
                
                # Try skipping
                sub_results_skip = find_components(start_idx + 1, current_set, visited_global)
                results.extend(sub_results_skip)
            
            return results

        # Start finding components
        # We need to ensure we don't generate the same component multiple times.
        # The strategy above (forcing the first element to be the minimum index) handles uniqueness.
        all_base_shapes = []
        # We iterate start_idx from 0. The first cell we pick becomes the root.
        # But the recursive function above handles the "must pick first if empty" logic.
        # However, we need to call it once.
        # Let's restructure slightly to be cleaner.
        
        # We will generate all connected subsets of size base_size.
        # To avoid duplicates, we enforce that the cell with the smallest coordinate in the subset is the first one added.
        
        def generate_components(idx, current):
            if len(current) == base_size:
                # Verify connectivity
                start = min(current)
                q = [start]
                seen = {start}
                i = 0
                while i < len(q):
                    r, c = q[i]
                    i += 1
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nr, nc = r+dr, c+dc
                        if (nr, nc) in current and (nr, nc) not in seen:
                            seen.add((nr, nc))
                            q.append((nr, nc))
                if len(seen) == base_size:
                    return [tuple(sorted(current))]
                return []
            
            if idx == len(sorted_cells):
                return []
            
            res = []
            cell = sorted_cells[idx]
            
            # If current is empty, we MUST take this cell as the start
            if not current:
                res.extend(generate_components(idx+1, current | {cell}))
            else:
                # Check if cell can be added (connectivity)
                can_add = False
                for p in current:
                    if abs(p[0]-cell[0]) + abs(p[1]-cell[1]) == 1:
                        can_add = True
                        break
                
                if can_add:
                    res.extend(generate_components(idx+1, current | {cell}))
                # Try skipping
                res.extend(generate_components(idx+1, current))
            
            return res

        base_shapes = generate_components(0, set())
        
        if not base_shapes:
            continue

        # Now for each base shape, try to tile the grid with k translations
        for base in base_shapes:
            # base is a tuple of (r,c)
            # We need to find k translation vectors T1, T2, ..., Tk such that:
            # 1. The union of (base + Ti) is exactly 'cells'
            # 2. The sets (base + Ti) are disjoint
            
            # Since k is small (2..5) and grid is small, we can try to determine the translation vectors.
            # One of the translations must be (0,0) relative to the base's position in the grid?
            # Not necessarily. The base shape is defined by relative coordinates.
            # Let's fix the first copy to be placed such that its "origin" (min element of base) maps to some cell in 'cells'.
            # Actually, simpler: The set of all cells is the union of k shifted copies of 'base'.
            # Let the translation vectors be v1, v2, ..., vk.
            # Then cells = { (r+vr, c+vc) | (r,c) in base, v in {v1..vk} }
            # And these sets must be disjoint.
            
            # We can iterate over possible translation vectors.
            # The range of translations is bounded by the grid size.
            # Let's collect all possible translation vectors that map 'base' into 'cells'.
            # A translation vector v is valid if (base + v) is a subset of 'cells'.
            
            possible_translations = []
            # The bounding box of base is small.
            # We can try all v such that base+v fits in the grid and is inside 'cells'.
            # But we don't know the absolute position of the first copy.
            # However, we know that the union covers 'cells'.
            # Let's pick the cell with the minimum index in 'cells'. It MUST be covered by some copy.
            # Let's assume the first copy (index 0) covers the min cell of 'cells'.
            # But which part of 'base' covers it?
            # This suggests we need to try all alignments.
            
            # Alternative approach:
            # The set of translation vectors must be such that their sum of indicator functions equals 1 on 'cells'.
            # Let's try to find k vectors.
            # Since k is small, we can try to fix the first vector to be (0,0) relative to some alignment?
            # No, the base shape is abstract.
            
            # Let's try this:
            # The set of cells 'cells' is fixed.
            # We need to partition 'cells' into k sets S1, S2, ..., Sk, each congruent to 'base' via translation.
            # This means for each Si, there exists a vector vi such that Si = { (r+vi_r, c+vi_c) for (r,c) in base }.
            
            # Algorithm:
            # 1. Pick the first cell in 'cells' (min index). It must belong to some Si.
            # 2. Determine which part of 'base' maps to this cell.
            #    For each cell b in base, assume b maps to min_cell. Then the translation vector for that copy is v = min_cell - b.
            # 3. Generate the full copy using this v. Check if it is a subset of 'cells'.
            # 4. If valid, remove these cells from 'cells' and recurse to find k-1 more copies.
            
            min_cell = min(cells)
            
            # Try each cell in base as the one that maps to min_cell
            for b in base:
                # Assume b maps to min_cell
                v0 = (min_cell[0] - b[0], min_cell[1] - b[1])
                
                # Generate the first copy
                copy0 = set()
                valid0 = True
                for br, bc in base:
                    nr, nc = br + v0[0], bc + v0[1]
                    if (nr, nc) not in cells:
                        valid0 = False
                        break
                    copy0.add((nr, nc))
                
                if not valid0:
                    continue
                
                # Now we need to find k-1 more copies from the remaining cells
                remaining = cells - copy0
                if len(remaining) != (k-1) * base_size:
                    continue
                
                # Recursive search for k-1 copies
                # We need to pick k-1 translation vectors from the remaining cells.
                # Again, pick the min cell of remaining, try all alignments.
                
                def search(k_left, current_remaining):
                    if k_left == 0:
                        return True
                    
                    if len(current_remaining) != k_left * base_size:
                        return False
                    
                    # Pick min cell
                    curr_min = min(current_remaining)
                    
                    # Try each b in base mapping to curr_min
                    for b in base:
                        v = (curr_min[0] - b[0], curr_min[1] - b[1])
                        
                        # Generate copy
                        copy = set()
                        valid = True
                        for br, bc in base:
                            nr, nc = br + v[0], bc + v[1]
                            if (nr, nc) not in current_remaining:
                                valid = False
                                break
                            copy.add((nr, nc))
                        
                        if not valid:
                            continue
                        
                        # Recurse
                        new_remaining = current_remaining - copy
                        if search(k_left - 1, new_remaining):
                            return True
                    return False

                if search(k-1, remaining):
                    # Found a solution!
                    # Now reconstruct the grid
                    # We need to store the copies to assign numbers 1..k
                    # Let's re-run the search to collect the copies
                    final_copies = []
                    
                    def collect(k_left, current_remaining, copies_list):
                        if k_left == 0:
                            copies_list.append(current_remaining) # This is not right, we need the sets
                            return True
                        if len(current_remaining) != k_left * base_size:
                            return False
                        
                        curr_min = min(current_remaining)
                        for b in base:
                            v = (curr_min[0] - b[0], curr_min[1] - b[1])
                            copy = set()
                            valid = True
                            for br, bc in base:
                                nr, nc = br + v[0], bc + v[1]
                                if (nr, nc) not in current_remaining:
                                    valid = False
                                    break
                                copy.add((nr, nc))
                            if not valid:
                                continue
                            new_remaining = current_remaining - copy
                            if collect(k_left - 1, new_remaining, copies_list):
                                copies_list.append(copy)
                                return True
                        return False

                    # We need to collect the copies in order 1..k
                    # But the order doesn't matter for correctness, just need to label them.
                    # Let's collect them.
                    collected = []
                    # We need to pass the state correctly.
                    # Let's rewrite the collection logic to be simpler.
                    
                    # Re-do the search to store copies
                    # We'll use a stack or recursion that builds the list.
                    
                    def build_copies(k_left, current_remaining, result_list):
                        if k_left == 0:
                            result_list.append(current_remaining) # Wait, current_remaining is the set of cells for the last copy? No.
                            # My logic above was flawed in collection.
                            # Let's fix:
                            return True
                        
                        curr_min = min(current_remaining)
                        for b in base:
                            v = (curr_min[0] - b[0], curr_min[1] - b[1])
                            copy = set()
                            valid = True
                            for br, bc in base:
                                nr, nc = br + v[0], bc + v[1]
                                if (nr, nc) not in current_remaining:
                                    valid = False
                                    break
                                copy.add((nr, nc))
                            if not valid:
                                continue
                            
                            new_remaining = current_remaining - copy
                            if build_copies(k_left - 1, new_remaining, result_list):
                                result_list.append(copy)
                                return True
                        return False

                    # We need to collect k copies.
                    # The first copy was copy0.
                    # Then we collect k-1 more.
                    temp_copies = []
                    if build_copies(k-1, remaining, temp_copies):
                        all_found_copies = [copy0] + temp_copies
                        # Verify we have k copies
                        if len(all_found_copies) == k:
                            # Construct output
                            output_grid = [['.' for _ in range(w)] for _ in range(h)]
                            for idx, copy in enumerate(all_found_copies):
                                label = idx + 1
                                for r, c in copy:
                                    output_grid[r][c] = str(label)
                            
                            # Print
                            for row in output_grid:
                                print("".join(row))
                            return

        # If we finish the loop without returning, no solution for this k
        # Continue to next k

    print("No solution")

if __name__ == "__main__":
    solve()