import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        H = int(next(iterator))
        W = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Use sets for O(1) lookup if needed, but we primarily need counts per row and column
    # However, M is up to 3*10^5, so we can just count frequencies.
    
    row_counts = [0] * (H + 1)
    col_counts = [0] * (W + 1)
    
    # Read M targets
    for _ in range(M):
        r = int(next(iterator))
        c = int(next(iterator))
        row_counts[r] += 1
        col_counts[c] += 1

    # We want to find max(row_counts[r] + col_counts[c]) for all r, c.
    # However, if we pick a cell (r, c) that has a target, we don't double count that target.
    # But note: the problem says "destroy all targets that are in the row or the column".
    # If a target is at (r, c), it is in row r AND in column c. But it's one target.
    # So the number of destroyed targets at (r, c) is:
    #   (number of targets in row r) + (number of targets in col c) - (1 if there is a target at (r, c) else 0)
    
    # To efficiently compute this, we can:
    # 1. Find the maximum value of (row_counts[r] + col_counts[c]) over all r, c.
    # 2. Check if the cell (r, c) that achieves this maximum actually has a target.
    #    If it does, subtract 1 from the sum.
    #    If it doesn't, the sum is correct.
    # But wait: there might be multiple cells (r, c) with the same (row_counts[r] + col_counts[c]).
    # Some might have a target, some might not. We want the maximum possible destroyed count.
    # So:
    #   candidate = max(row_counts[r] + col_counts[c] for all r, c)
    #   However, if for the (r, c) that gives candidate, there is NO target, then the answer is candidate.
    #   If for the (r, c) that gives candidate, there IS a target, then the answer is candidate - 1.
    # BUT: it's possible that the maximum sum is achieved by a cell with a target, but there exists another cell (r', c') 
    # with the same sum that does NOT have a target. Then the answer would be the sum (without subtracting).
    # So:
    #   Let max_sum = max(row_counts[r] + col_counts[c] for all r, c)
    #   Check if there exists ANY cell (r, c) such that row_counts[r] + col_counts[c] == max_sum AND (r, c) is NOT a target.
    #   If yes, then answer = max_sum.
    #   If no (meaning all cells achieving max_sum have a target), then answer = max_sum - 1.
    
    # However, iterating over all r and c (H*W) is too slow (up to 9e10).
    # We need a better way.
    
    # Observation:
    # The maximum possible value of row_counts[r] + col_counts[c] is at most M.
    # Let max_r = max(row_counts) and max_c = max(col_counts).
    # Then max_sum = max_r + max_c.
    # This maximum sum is achievable if we pick r0 such that row_counts[r0] == max_r and c0 such that col_counts[c0] == max_c.
    # Now, does the cell (r0, c0) have a target?
    #   If no, then answer = max_r + max_c.
    #   If yes, then answer = max_r + max_c - 1.
    # BUT: is it possible that max_r + max_c is not the true maximum? No, because row_counts[r] <= max_r and col_counts[c] <= max_c.
    # So the maximum sum is exactly max_r + max_c.
    # Now the only question is: is there at least one pair (r, c) with row_counts[r] == max_r and col_counts[c] == max_c that does NOT have a target?
    #   If yes, then we can achieve max_r + max_c.
    #   If for EVERY pair (r, c) with row_counts[r] == max_r and col_counts[c] == max_c, the cell (r, c) has a target, then we must subtract 1.
    
    # How to check if there exists a pair (r, c) with row_counts[r] == max_r, col_counts[c] == max_c, and no target at (r, c)?
    # Let R_max = set of rows with row_counts[r] == max_r.
    # Let C_max = set of cols with col_counts[c] == max_c.
    # We need to check if there is any (r in R_max, c in C_max) such that (r, c) is not in the target set.
    # The total number of pairs in R_max x C_max is |R_max| * |C_max|.
    # The number of targets in R_max x C_max is the count of targets with row in R_max and col in C_max.
    # If |R_max| * |C_max| > (number of targets in R_max x C_max), then there is at least one missing cell -> answer = max_r + max_c.
    # Otherwise (if |R_max| * |C_max| == number of targets in R_max x C_max), then every cell in R_max x C_max has a target -> answer = max_r + max_c - 1.
    
    # Steps:
    # 1. Compute max_r = max(row_counts[1:]), max_c = max(col_counts[1:]).
    # 2. Identify R_max = [r for r in 1..H if row_counts[r] == max_r]
    # 3. Identify C_max = [c for c in 1..W if col_counts[c] == max_c]
    # 4. Count how many targets have row in R_max and col in C_max.
    #    We can do this by iterating over the M targets and checking if row in R_max and col in C_max.
    #    But to do this efficiently, we can mark rows in R_max and cols in C_max.
    #    However, H and W are large, but |R_max| and |C_max| might be large too.
    #    But note: the total number of targets is M (<= 3e5). So we can iterate over targets.
    # 5. Let total_pairs = len(R_max) * len(C_max).
    # 6. Let target_in_max = count of targets with row in R_max and col in C_max.
    # 7. If total_pairs > target_in_max: ans = max_r + max_c
    #    Else: ans = max_r + max_c - 1
    
    # However, there is a catch: what if max_r + max_c is not the maximum possible? 
    # Actually, it is the maximum possible because row_counts[r] <= max_r and col_counts[c] <= max_c.
    # So the maximum sum is always max_r + max_c.
    
    # Implementation:
    
    max_r = 0
    for r in range(1, H+1):
        if row_counts[r] > max_r:
            max_r = row_counts[r]
            
    max_c = 0
    for c in range(1, W+1):
        if col_counts[c] > max_c:
            max_c = col_counts[c]
            
    # Identify rows with max_r
    # We can use a boolean array or set. Since H is up to 3e5, a boolean array is fine.
    is_r_max = [False] * (H + 1)
    count_r_max = 0
    for r in range(1, H+1):
        if row_counts[r] == max_r:
            is_r_max[r] = True
            count_r_max += 1
            
    # Identify cols with max_c
    is_c_max = [False] * (W + 1)
    count_c_max = 0
    for c in range(1, W+1):
        if col_counts[c] == max_c:
            is_c_max[c] = True
            count_c_max += 1
            
    # Count targets that are in (R_max x C_max)
    target_in_max = 0
    # We already have the targets in the input, but we didn't store them. 
    # We need to store them? Or we can re-iterate? 
    # Since we read the input as a list of tokens, we can reconstruct or store the targets.
    # Let's store the targets as we read. But we already consumed the iterator.
    # Better: store the targets in a list during reading.
    
    # Actually, we didn't store them. Let's re-read? No, we can't. 
    # We should have stored them. Let's refactor: store targets in a list.
    
    # Since we are in the middle of solving, let's assume we store the targets.
    # But in the above code, we didn't. So let's rewrite the reading part to store targets.
    
    # Given the constraints and the fact that we are writing a complete solution, let's adjust.
    pass

# Let's rewrite the solution properly with storing targets.

import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        H = int(next(iterator))
        W = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    row_counts = [0] * (H + 1)
    col_counts = [0] * (W + 1)
    targets = []  # Store as (r, c)

    for _ in range(M):
        r = int(next(iterator))
        c = int(next(iterator))
        targets.append((r, c))
        row_counts[r] += 1
        col_counts[c] += 1

    max_r = 0
    for r in range(1, H+1):
        if row_counts[r] > max_r:
            max_r = row_counts[r]
            
    max_c = 0
    for c in range(1, W+1):
        if col_counts[c] > max_c:
            max_c = col_counts[c]

    # Identify rows with max_r
    is_r_max = [False] * (H + 1)
    count_r_max = 0
    for r in range(1, H+1):
        if row_counts[r] == max_r:
            is_r_max[r] = True
            count_r_max += 1

    # Identify cols with max_c
    is_c_max = [False] * (W + 1)
    count_c_max = 0
    for c in range(1, W+1):
        if col_counts[c] == max_c:
            is_c_max[c] = True
            count_c_max += 1

    # Count targets in R_max x C_max
    target_in_max = 0
    for r, c in targets:
        if is_r_max[r] and is_c_max[c]:
            target_in_max += 1

    total_pairs = count_r_max * count_c_max

    if total_pairs > target_in_max:
        print(max_r + max_c)
    else:
        print(max_r + max_c - 1)

if __name__ == '__main__':
    main()