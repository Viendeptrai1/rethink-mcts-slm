import sys

def min_swaps_to_divisible_by_25(n):
    n = str(n)
    length = len(n)
    
    # Check for '00' or '25' or '50' or '75' at the end
    if n[-2:] in ['00', '25', '50', '75']:
        return 0
    
    # Find the positions of '0' and '5'
    zero_positions = [i for i, digit in enumerate(n) if digit == '0']
    five_positions = [i for i, digit in enumerate(n) if digit == '5']
    
    # If there are no '0's or '5's, it's impossible to form a number divisible by 25
    if not zero_positions and not five_positions:
        return -1
    
    min_swaps = float('inf')
    
    # Try to place '0' at the second last position
    for z in zero_positions:
        if z < length - 1:
            swaps = z + (length - 2 - z)  # Move '0' to the second last position
            # Check if we can place '5' at the last position
            for f in five_positions:
                if f > z:
                    swaps += f - z - 1  # Move '5' to the last position
                    min_swaps = min(min_swaps, swaps)
                    break
    
    # Try to place '5' at the second last position
    for f in five_positions:
        if f < length - 1:
            swaps = f + (length - 2 - f)  # Move '5' to the second last position
            # Check if we can place '0' at the last position
            for z in zero_positions:
                if z > f:
                    swaps += z - f - 1  # Move '0' to the last position
                    min_swaps = min(min_swaps, swaps)
                    break
    
    return min_swaps if min_swaps != float('inf') else -1

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_swaps_to_divisible_by_25(n))