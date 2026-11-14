import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    H = int(data[0])
    W = int(data[1])
    M = int(data[2])
    
    row_counts = [0] * (H + 1)
    col_counts = [0] * (W + 1)
    
    idx = 3
    for _ in range(M):
        r = int(data[idx])
        c = int(data[idx+1])
        idx += 2
        row_counts[r] += 1
        col_counts[c] += 1
    
    max_destroyed = 0
    
    # Check every row to see if placing a bomb in that row (at any column) could be optimal
    # The best column in a given row r is the one with the maximum col_counts
    # However, we must account for whether the intersection (r, c) has a target.
    # If (r, c) has a target: destroyed = row_counts[r] + col_counts[c] - 1
    # If (r, c) has no target: destroyed = row_counts[r] + col_counts[c]
    
    # To optimize, we can precompute the max col count and the second max col count.
    # Why? Because for a fixed row r:
    # - If there exists a column c with a target in row r such that col_counts[c] is maximal, 
    #   then the result is row_counts[r] + max_col - 1.
    # - If the column with the maximal col_counts does NOT have a target in row r,
    #   then the result is row_counts[r] + max_col.
    # - If the column with the maximal col_counts has a target, but we choose a different column 
    #   (with second max col count) that also has a target? Actually, if the max col has a target,
    #   we get max_col - 1. If we pick a non-target column with max_col, we get max_col.
    #   So if there is ANY column with count = max_col that does NOT have a target in row r,
    #   we can achieve row_counts[r] + max_col.
    #   Only if ALL columns with count = max_col have a target in row r, are we forced to take max_col - 1?
    #   Wait, no. If a column c has count K, and (r,c) has no target, we get row_counts[r] + K.
    #   If (r,c) has a target, we get row_counts[r] + K - 1.
    #   So for a fixed row r, the maximum we can get is:
    #   row_counts[r] + max( col_counts[c] if (r,c) not in targets else col_counts[c]-1 for all c )
    #   This is equivalent to:
    #   Let max_c = max(col_counts).
    #   If there exists a column c with col_counts[c] == max_c such that (r,c) is NOT a target,
    #   then answer for row r is row_counts[r] + max_c.
    #   Otherwise (all columns with max_c have a target in row r), the answer is row_counts[r] + max_c - 1.
    
    # We need to know for each row, does it contain a target in a column that has the global maximum column count?
    # Actually, simpler approach:
    # Find the global maximum column count, say max_col_val.
    # Also, we need to know if for a specific row r, there is at least one column c with col_counts[c] == max_col_val
    # such that (r, c) is NOT a target.
    
    # Let's collect all columns that have the maximum count.
    max_col_val = 0
    for c in range(1, W + 1):
        if col_counts[c] > max_col_val:
            max_col_val = col_counts[c]
    
    # Identify columns with max_col_val
    max_cols = [c for c in range(1, W + 1) if col_counts[c] == max_col_val]
    
    # For each row, check if there is a target in any of the max_cols.
    # If there is NO target in any of the max_cols for row r, then we can pick one of those columns
    # and get row_counts[r] + max_col_val.
    # If there IS a target in some max_col for row r, we have two cases:
    #   1. There is also a max_col that does NOT have a target in row r -> we can pick that -> row_counts[r] + max_col_val
    #   2. All max_cols have a target in row r -> we must pick one with a target -> row_counts[r] + max_col_val - 1
    #
    # So for each row r:
    #   has_target_in_max_cols = any (r, c) is a target for c in max_cols
    #   if not has_target_in_max_cols:
    #       candidate = row_counts[r] + max_col_val
    #   else:
    #       # Check if there is at least one max_col that does NOT have a target in row r
    #       # Since we know at least one max_col HAS a target, we need to check if ALL max_cols have targets.
    #       # If count(max_cols) > count of max_cols that have a target in row r, then there is a safe one.
    #       # Actually, simpler: if the number of max_cols that have a target in row r is less than len(max_cols),
    #       # then there exists a max_col without a target.
    #       # But iterating all max_cols for each row might be slow if many max_cols.
    #       # However, M is up to 3e5. The number of max_cols can be up to W.
    #       # We need a faster way.
    #
    # Alternative logic:
    # The maximum possible value for a row r is row_counts[r] + max_col_val.
    # This value is achievable if there exists a column c with col_counts[c] == max_col_val such that (r,c) is not a target.
    # If for a row r, EVERY column c with col_counts[c] == max_col_val has a target at (r,c), then the best we can do is row_counts[r] + max_col_val - 1.
    #
    # So for each row r:
    #   Let S_r be the set of columns c where (r,c) is a target.
    #   Let T be the set of columns with col_counts[c] == max_col_val.
    #   If S_r and T are disjoint, then max = row_counts[r] + max_col_val.
    #   If S_r and T are not disjoint, we need to check if S_r covers all of T.
    #   If S_r covers all of T (i.e., T is a subset of S_r), then max = row_counts[r] + max_col_val - 1.
    #   Otherwise (partial overlap), max = row_counts[r] + max_col_val.
    #
    # To implement efficiently:
    #   We can store the targets in a way that allows quick lookup.
    #   Since M is up to 3e5, we can store targets in a dictionary: row -> set of cols.
    #   Or since we only care about rows that have targets, we can iterate over rows that have targets.
    #   For rows with 0 targets, the answer is 0 + max_col_val (since no target in any column, so definitely no target in max_cols).
    #   Wait, if row_counts[r] == 0, then row r has no targets. So for any column c, (r,c) is not a target.
    #   So we can always pick a column with max_col_val and get 0 + max_col_val.
    #
    # So:
    #   Initialize global_max = 0.
    #   For each row r from 1 to H:
    #       if row_counts[r] == 0:
    #           current = max_col_val
    #       else:
    #           # Check intersection with max_cols
    #           # We need to know if all max_cols have a target in row r.
    #           # Let's precompute for each row, which of the max_cols have targets.
    #           # But iterating max_cols for each row is O(H * |max_cols|) which is too slow.
    #
    # Better approach:
    #   Instead of checking per row, let's consider the structure.
    #   The maximum possible answer is max(row_counts[r] + col_counts[c] - (1 if (r,c) in targets else 0)) over all r, c.
    #   We can iterate over all rows r.
    #   For a fixed r, we want max over c of (col_counts[c] - (1 if (r,c) in targets else 0)).
    #   Let base = max(col_counts).
    #   If there is a c with col_counts[c] == base and (r,c) not in targets, then max_c_term = base.
    #   Else, max_c_term = base - 1.
    #   So for each r, we need to know: is there a column with count == base that does NOT have a target in row r?
    #
    #   Let's create a set of "bad" columns for each row? No, too much memory/time.
    #   Instead, let's count how many max_cols have a target in row r.
    #   Let K = number of max_cols.
    #   For each row r, let count_r = number of c in max_cols such that (r,c) is a target.
    #   If count_r < K, then there is a max_col without a target -> result = row_counts[r] + base.
    #   If count_r == K, then all max_cols have a target -> result = row_counts[r] + base - 1.
    #
    #   How to compute count_r efficiently?
    #   We can iterate over all targets. For each target (r, c), if col_counts[c] == base, then increment count_r for row r.
    #   We can use an array `row_max_col_hits` of size H+1, initialized to 0.
    #   Iterate over all M targets:
    #       if col_counts[target_c] == base:
    #           row_max_col_hits[target_r] += 1
    #
    #   Then for each row r:
    #       if row_counts[r] == 0:
    #           ans = max(ans, base)
    #       else:
    #           hits = row_max_col_hits[r]
    #           if hits < K:
    #               ans = max(ans, row_counts[r] + base)
    #           else:
    #               ans = max(ans, row_counts[r] + base - 1)
    #
    #   Also, we must consider the case where we don't pick a max_col? 
    #   No, because col_counts[c] <= base for all c.
    #   If we pick a column with count < base, the sum would be row_counts[r] + (count - (1 if target else 0))
    #   <= row_counts[r] + (base - 1) < row_counts[r] + base (if we can get base)
    #   or <= row_counts[r] + (base - 1) which is the same as the "all max_cols hit" case.
    #   So we only need to consider columns with count == base.
    #
    #   One edge case: what if K=0? Impossible since W>=1 and M>=1, so at least one column has count >=1.
    #   What if base=0? Only if M=0, but M>=1.
    
    # Implementation:
    # 1. Read input, build row_counts, col_counts.
    # 2. Find base = max(col_counts).
    # 3. Count K = number of columns with col_counts[c] == base.
    # 4. Initialize row_max_col_hits = [0]*(H+1).
    # 5. Iterate over all targets again (we need to store them or re-read).
    #    Since we read all data into a list, we can iterate the list of targets.
    #    But we didn't store the targets explicitly as a list of tuples.
    #    We can store them in a list while reading.
    
    targets = []
    idx = 3
    for _ in range(M):
        r = int(data[idx])
        c = int(data[idx+1])
        idx += 2
        targets.append((r, c))
    
    # Re-calculate row_counts and col_counts from targets to be sure (or use the ones we built)
    # We already built them, but let's verify consistency.
    # Actually, we built them correctly.
    
    # Find base and K
    base = 0
    for c in range(1, W + 1):
        if col_counts[c] > base:
            base = col_counts[c]
    
    K = 0
    for c in range(1, W + 1):
        if col_counts[c] == base:
            K += 1
    
    row_max_col_hits = [0] * (H + 1)
    
    for r, c in targets:
        if col_counts[c] == base:
            row_max_col_hits[r] += 1
    
    ans = 0
    
    for r in range(1, H + 1):
        rc = row_counts[r]
        if rc == 0:
            current = base
        else:
            hits = row_max_col_hits[r]
            if hits < K:
                current = rc + base
            else:
                current = rc + base - 1
        if current > ans:
            ans = current
            
    print(ans)

if __name__ == '__main__':
    solve()