import sys

def min_swaps_to_divisible_by_25(n):
    n_str = str(n)
    length = len(n_str)
    
    # Find all positions of '0' and '5'
    zero_positions = [i for i, digit in enumerate(n_str) if digit == '0']
    five_positions = [i for i, digit in enumerate(n_str) if digit == '5']
    
    # If there are no '0's or '5's, it's impossible to form a number divisible by 25
    if not zero_positions and not five_positions:
        return -1
    
    min_swaps = float('inf')
    
    # Check for '00'
    if len(zero_positions) >= 2:
        for i in range(len(zero_positions)):
            for j in range(i + 1, len(zero_positions)):
                swaps = zero_positions[i] + (length - zero_positions[j] - 1)
                min_swaps = min(min_swaps, swaps)
    
    # Check for '25', '50', '75'
    for target in ['25', '50', '75']:
        for i in five_positions:
            for j in zero_positions:
                if n_str[i-1] == target[0] and j > i:
                    swaps = i + (length - j - 1)
                    min_swaps = min(min_swaps, swaps)
    
    return min_swaps if min_swaps != float('inf') else -1

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_swaps_to_divisible_by_25(n))