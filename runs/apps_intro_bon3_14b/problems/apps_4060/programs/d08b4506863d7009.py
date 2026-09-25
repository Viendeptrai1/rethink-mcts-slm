import sys

def count_positions_to_make_regular(n, s):
    # Initialize counters
    open_count = 0
    close_count = 0
    imbalance = 0
    valid_changes = 0

    # First pass: count imbalances
    for char in s:
        if char == '(':
            open_count += 1
        else:
            close_count += 1
        if close_count > open_count:
            imbalance += 1

    # Second pass: count valid changes
    open_count = 0
    close_count = 0
    for char in s:
        if char == '(':
            open_count += 1
        else:
            close_count += 1
        if close_count > open_count:
            if imbalance > 0:
                valid_changes += 1
                imbalance -= 1
        elif open_count > close_count + 1:
            valid_changes += 1

    return valid_changes

# Read input
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Calculate and print the result
result = count_positions_to_make_regular(n, s)
print(result)