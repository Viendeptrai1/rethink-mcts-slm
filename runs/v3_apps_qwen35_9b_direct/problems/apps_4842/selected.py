import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    values = [int(x) for x in input_data[1:]]

    # Create a list of lists for difference tables
    # diff_tables[0] will be the original values
    diff_tables = [values]

    current_level = values
    degree = 0

    # Compute differences until we reach a constant level (all elements equal)
    while True:
        if len(current_level) < 2:
            break
        
        next_level = []
        for i in range(len(current_level) - 1):
            next_level.append(current_level[i+1] - current_level[i])
        
        # Check if the next level is constant
        is_constant = True
        if len(next_level) > 0:
            first_val = next_level[0]
            for val in next_level:
                if val != first_val:
                    is_constant = False
                    break
        
        if is_constant:
            degree = len(diff_tables) - 1
            break
        
        diff_tables.append(next_level)
        current_level = next_level
        degree += 1

    # If we broke out because the list had length < 2, it means we only had 1 point initially?
    # But problem says n >= 2 and at least two values differ.
    # So the loop should find a constant level eventually.
    # However, if the sequence is constant from the start, degree is 0.
    # Let's re-verify the logic for degree 0.
    # If values are [5, 5, 5], first diff is [0, 0], which is constant.
    # diff_tables = [[5,5,5], [0,0]]. 
    # Loop: current_level = [5,5,5]. next_level = [0,0]. is_constant = True.
    # degree = 1. But degree should be 0.
    
    # Correction: The degree is the number of times we had to take differences to get a constant.
    # If the original sequence is constant, degree is 0.
    # If we take 1 difference and get constant, degree is 1.
    
    # Let's restart the logic cleanly.
    diff_tables = [values]
    degree = 0
    
    current = values
    while True:
        if len(current) < 2:
            break
        
        next_diff = []
        for i in range(len(current) - 1):
            next_diff.append(current[i+1] - current[i])
        
        # Check if next_diff is constant
        is_const = True
        if len(next_diff) > 0:
            ref = next_diff[0]
            for x in next_diff:
                if x != ref:
                    is_const = False
                    break
        
        if is_const:
            degree = len(diff_tables) - 1
            break
        
        diff_tables.append(next_diff)
        current = next_diff
        degree += 1
    
    # Now predict the next value
    # We work backwards from the last constant row
    # The last row (constant) has length 1 effectively for prediction purposes?
    # Actually, the last row we computed is constant. Let's say it has k elements.
    # We need to extend it by one element (same as the constant value).
    # Then move up to the previous row, add the extended value to the last element, etc.
    
    # Identify the last computed difference table which is constant
    # In our loop, 'current' holds the last non-constant or the constant one?
    # If we broke because is_const, 'current' is the one that produced the constant 'next_diff'.
    # Wait, in the loop:
    # 1. Compute next_diff from current.
    # 2. Check if next_diff is constant.
    # 3. If yes, degree = len(diff_tables)-1. Break.
    # So 'current' is the table at index 'degree'. 'next_diff' is the table at index 'degree+1' (which is constant).
    # But we didn't append next_diff to diff_tables in the break case.
    
    # Let's reconstruct the constant row.
    # If degree == 0, the original values are constant.
    # If degree > 0, the last row in diff_tables is the constant one?
    # Example: 3, 6, 9, 12, 15
    # diff_tables[0] = [3, 6, 9, 12, 15]
    # next_diff = [3, 3, 3, 3] -> constant.
    # degree = 1.
    # diff_tables = [[3,6,9,12,15]]
    # We need to extend [3,3,3,3] to [3,3,3,3,3].
    # Then add to last element of [3,6,9,12,15] -> 15+3 = 18.
    
    # Example: 9, 25, 49, 81
    # diff0: 9, 25, 49, 81
    # diff1: 16, 24, 32
    # diff2: 8, 8 -> constant.
    # degree = 2.
    # diff_tables = [diff0, diff1]
    # We need to extend diff2 (which is [8,8]) to [8,8,8].
    # Add to last of diff1: 32 + 8 = 40.
    # Add to last of diff0: 81 + 40 = 121.
    
    # So we need to generate the constant row explicitly.
    # The constant row is the one we found in the loop.
    # If degree == 0, the constant row is [values[0]].
    # If degree > 0, the constant row is the one we computed but didn't store?
    # Actually, let's just store all rows including the constant one to make it easier.
    
    # Re-run logic to store all rows
    diff_tables = [values]
    current = values
    degree = 0
    
    while True:
        if len(current) < 2:
            break
        
        next_diff = []
        for i in range(len(current) - 1):
            next_diff.append(current[i+1] - current[i])
        
        is_const = True
        if len(next_diff) > 0:
            ref = next_diff[0]
            for x in next_diff:
                if x != ref:
                    is_const = False
                    break
        
        if is_const:
            degree = len(diff_tables)
            diff_tables.append(next_diff)
            break
        
        diff_tables.append(next_diff)
        current = next_diff
        degree += 1
    
    # Now diff_tables has rows 0 to degree.
    # Row 'degree' is the constant row.
    # We need to extend row 'degree' by one element (same as the existing elements).
    # Then propagate up.
    
    # Get the constant row
    const_row = diff_tables[degree]
    # The value to add is the constant value
    const_val = const_row[0]
    
    # Start from the second to last row (degree-1) down to 0
    # We need to compute the next value for each row starting from the bottom.
    # The bottom row (degree) becomes [c, c, ..., c, c]
    # The row above (degree-1) last element becomes last_element + c
    # And so on.
    
    # Initialize the extended value for the next step
    next_val = const_val
    
    # Iterate from degree-1 down to 0
    for i in range(degree - 1, -1, -1):
        last_elem = diff_tables[i][-1]
        next_val = last_elem + next_val
        diff_tables[i].append(next_val)
    
    # The final answer is the last element of the original row (row 0)
    v_next = diff_tables[0][-1]
    
    print(f"{degree} {v_next}")

if __name__ == "__main__":
    solve()