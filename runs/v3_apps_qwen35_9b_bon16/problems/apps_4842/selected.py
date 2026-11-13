import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    values = [int(x) for x in input_data[1:]]
    
    # Create a list of lists for difference tables
    # diff_levels[0] will be the original values
    # diff_levels[k] will be the k-th level of differences
    diff_levels = []
    current_level = values[:]
    
    while True:
        diff_levels.append(current_level)
        if len(current_level) == 1:
            break
        next_level = []
        for i in range(len(current_level) - 1):
            next_level.append(current_level[i+1] - current_level[i])
        current_level = next_level
    
    # Find the degree d
    # The degree is the index of the first level that has constant values
    # Since at least two values differ, degree >= 1
    # We look for the level where all elements are equal
    degree = 0
    for i, level in enumerate(diff_levels):
        if len(level) == 1:
            # If the last level has 1 element, it is constant by definition
            # But we need to check if it's the minimal degree.
            # Actually, the problem states that for an n-th degree polynomial,
            # the n-th row of differences is constant.
            # Since we have n inputs, the maximum degree is n-1.
            # The first level with constant values determines the degree.
            # If the level has 1 element, it is trivially constant.
            degree = i
            break
        elif len(level) > 1:
            # Check if all elements are the same
            is_constant = True
            first_val = level[0]
            for val in level:
                if val != first_val:
                    is_constant = False
                    break
            if is_constant:
                degree = i
                break
    
    # Calculate the next value v_{n+1}
    # We extend the difference table backwards from the top (constant level)
    # down to the original level to get the next value
    
    # Start with the next value in the last (constant) difference level
    next_val = diff_levels[-1][0]
    
    # Propagate down
    for i in range(len(diff_levels) - 2, -1, -1):
        # The last element of the current level is the one we just computed (next_val)
        # The previous level has len = len(diff_levels[i])
        # The last element of level i is (last element of level i+1) - (next value to be added to level i)
        # Actually, diff[i][j] = diff[i+1][j] - diff[i+1][j+1] (if going down)
        # But we are building forward.
        # Relationship: level[i][j] = level[i+1][j] - level[i+1][j+1]
        # So level[i+1][j+1] = level[i+1][j] - level[i][j]
        # We need the last element of level i+1, which is next_val.
        # We need the last element of level i, which is the last element of the original list at this stage.
        
        # Let's re-verify the indexing.
        # diff_levels[i] has length L_i
        # diff_levels[i+1] has length L_i - 1
        # We have computed the next value for diff_levels[-1], let's call it `last_diff`
        # This `last_diff` corresponds to the next value in the bottom-most difference sequence.
        # Now we move up to the previous level.
        # The last element of the previous level (diff_levels[i]) is known. Let's call it `last_prev`.
        # The relation is: diff_levels[i+1][-1] = diff_levels[i][-1] - next_element_in_diff_levels[i]
        # Wait, the standard forward difference is: diff[i] = f[i+1] - f[i]
        # So f[i+1] = f[i] + diff[i]
        # In the table:
        # Level 0: f[0], f[1], ..., f[n-1]
        # Level 1: d[0], d[1], ..., d[n-2] where d[j] = f[j+1] - f[j]
        # Level 2: dd[0], ..., dd[n-3] where dd[j] = d[j+1] - d[j]
        #
        # To find f[n], we need to extend the table.
        # The bottom level (constant) has been extended by one value: next_val.
        # This next_val is the next term in the sequence for that level.
        # Let's say level k is the constant level. Its last term was dd[-1]. We added next_val.
        # Now we go to level k-1. The last term of level k-1 is dd_level[k-1][-1].
        # The relationship is: next_val (for level k) = dd_level[k-1][-1] - next_val_for_level_k_minus_1?
        # No.
        # dd[j] = d[j+1] - d[j]
        # So d[j+1] = dd[j] + d[j]
        # We know d[j] (the last element of level k-1) and dd[j] (the last element of level k, which we just extended).
        # So the next element for level k-1 is: next_val (level k) + last_element(level k-1)
        # Let's trace:
        # Level k (constant): ... , L_k_last
        # We computed next_val = L_k_last (since it's constant, the next one is same)
        # Level k-1: ... , L_{k-1}_last
        # We know L_k_last = L_{k-1}_next - L_{k-1}_last  => L_{k-1}_next = L_k_last + L_{k-1}_last
        # Wait, L_k is derived from L_{k-1}. L_k[j] = L_{k-1}[j+1] - L_{k-1}[j]
        # So L_k_last = L_{k-1}_next - L_{k-1}_last
        # Therefore L_{k-1}_next = L_k_last + L_{k-1}_last
        # Correct.
        
        last_current = next_val
        last_prev = diff_levels[i][-1]
        next_val = last_prev + last_current
    
    print(degree, next_val)

if __name__ == "__main__":
    solve()