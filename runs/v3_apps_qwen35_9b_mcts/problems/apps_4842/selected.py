import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    values = [int(x) for x in input_data[1:n+1]]

    # Store all difference levels
    levels = [values[:]]
    
    # Compute differences until we find a constant row
    while True:
        current_level = levels[-1]
        if len(current_level) <= 1:
            break
        
        # Check if all elements in the current level are the same
        is_constant = True
        first_val = current_level[0]
        for val in current_level[1:]:
            if val != first_val:
                is_constant = False
                break
        
        if is_constant:
            break
        
        # Compute next level of differences
        next_level = [current_level[i+1] - current_level[i] for i in range(len(current_level)-1)]
        levels.append(next_level)

    # The degree d is the number of difference levels computed minus 1
    # Actually, if the original sequence is constant, degree is 0.
    # If we needed 1 level of diff to get constant, degree is 1.
    # So degree = len(levels) - 1
    d = len(levels) - 1

    # Now extrapolate to find the next value
    # Start from the bottom (constant row) and work our way up
    # The last row (levels[-1]) is constant. Its next value is the same as its last value.
    # Then we add that to the last value of the previous row, and so on.

    next_val = levels[-1][-1]  # The constant value in the last row

    # Propagate upwards
    for i in range(len(levels) - 2, -1, -1):
        next_val = levels[i][-1] + next_val

    print(f"{d} {next_val}")

if __name__ == "__main__":
    solve()