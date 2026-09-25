import sys

def min_swaps_to_divisible_by_25(n):
    n_str = str(n)
    length = len(n_str)
    
    # Check for '00' at the end
    if n_str[-2:] == '00':
        return 0
    
    # Find the positions of '0' and '5'
    zero_positions = [i for i, c in enumerate(n_str) if c == '0']
    five_positions = [i for i, c in enumerate(n_str) if c == '5']
    
    # Try to form '25' or '75' by moving '5' to the last position
    min_swaps = float('inf')
    for five_pos in five_positions:
        if five_pos < length - 1:
            # Move '5' to the last position
            swaps = five_pos + (length - 1 - five_pos)
            # Check if we can place '0' in the second last position
            for zero_pos in zero_positions:
                if zero_pos < five_pos:
                    swaps += five_pos - zero_pos - 1
                    min_swaps = min(min_swaps, swaps)
                    break
    
    # Try to form '50' by moving '0' to the last position
    for zero_pos in zero_positions:
        if zero_pos < length - 1:
            # Move '0' to the last position
            swaps = zero_pos + (length - 1 - zero_pos)
            # Check if we can place '5' in the second last position
            for five_pos in five_positions:
                if five_pos > zero_pos:
                    swaps += five_pos - zero_pos - 1
                    min_swaps = min(min_swaps, swaps)
                    break
    
    if min_swaps == float('inf'):
        return -1
    else:
        return min_swaps

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_swaps_to_divisible_by_25(n))