import sys

def min_swaps_to_divisible_by_25(n):
    n_str = str(n)
    length = len(n_str)
    
    # Check for the presence of '00', '25', '50', '75'
    targets = ['00', '25', '50', '75']
    target_positions = []
    
    for target in targets:
        pos = n_str.rfind(target)
        if pos != -1:
            target_positions.append(pos)
    
    if not target_positions:
        return -1
    
    min_swaps = float('inf')
    
    for pos in target_positions:
        swaps = 0
        # Move the target to the end of the string
        for i in range(pos, length - 2):
            if n_str[i] == '0':
                # If there's a '0' before the target, we need to move it to the end
                swaps += length - 2 - i
                break
            else:
                swaps += 1
        
        # Check if the resulting number has leading zeros
        if swaps < min_swaps:
            min_swaps = swaps
    
    return min_swaps if min_swaps != float('inf') else -1

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_swaps_to_divisible_by_25(n))