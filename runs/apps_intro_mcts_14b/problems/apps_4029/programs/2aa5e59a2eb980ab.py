import sys

def min_swaps_to_divisible_by_25(n):
    n_str = str(n)
    length = len(n_str)
    
    # Check for '00', '25', '50', '75'
    targets = ['00', '25', '50', '75']
    min_swaps = float('inf')
    
    for target in targets:
        if target in n_str:
            # Find the positions of the target digits
            pos1 = n_str.index(target[0])
            pos2 = n_str.index(target[1], pos1 + 1)
            
            # Calculate the number of swaps needed
            swaps = pos1 + (length - pos2 - 1)
            
            # Ensure no leading zeros are introduced
            if pos2 > 0 and n_str[:pos2].count('0') == 0:
                min_swaps = min(min_swaps, swaps)
    
    if min_swaps == float('inf'):
        return -1
    else:
        return min_swaps

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_swaps_to_divisible_by_25(n))