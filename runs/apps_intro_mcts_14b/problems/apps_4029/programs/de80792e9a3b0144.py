import sys

def min_swaps_to_divisible_by_25(n):
    n = str(n)
    length = len(n)
    
    # Check for impossible cases
    if '0' not in n and '5' not in n:
        return -1
    
    # Find the rightmost '0' and '5'
    zero_pos = -1
    five_pos = -1
    for i in range(length):
        if n[i] == '0':
            zero_pos = i
        if n[i] == '5':
            five_pos = i
    
    # If there is no '0' or '5', it's impossible
    if zero_pos == -1 and five_pos == -1:
        return -1
    
    # Calculate minimum swaps for '00'
    if zero_pos != -1 and zero_pos < length - 1:
        swaps_for_00 = zero_pos + (length - 1 - zero_pos) - 1
    else:
        swaps_for_00 = float('inf')
    
    # Calculate minimum swaps for '25'
    swaps_for_25 = float('inf')
    if five_pos != -1:
        for i in range(length):
            if n[i] == '2':
                swaps_for_25 = min(swaps_for_25, i + (length - 1 - five_pos))
    
    # Calculate minimum swaps for '50'
    swaps_for_50 = float('inf')
    if zero_pos != -1:
        for i in range(length):
            if n[i] == '5':
                swaps_for_50 = min(swaps_for_50, i + (length - 1 - zero_pos))
    
    # Calculate minimum swaps for '75'
    swaps_for_75 = float('inf')
    if five_pos != -1:
        for i in range(length):
            if n[i] == '7':
                swaps_for_75 = min(swaps_for_75, i + (length - 1 - five_pos))
    
    # Find the minimum swaps among all possibilities
    min_swaps = min(swaps_for_00, swaps_for_25, swaps_for_50, swaps_for_75)
    
    return min_swaps if min_swaps != float('inf') else -1

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_swaps_to_divisible_by_25(n))