import sys

def min_swaps_to_divisible_by_25(n):
    n_str = str(n)
    length = len(n_str)
    
    # Find all positions of '0' and '5'
    zeros = [i for i, c in enumerate(n_str) if c == '0']
    fives = [i for i, c in enumerate(n_str) if c == '5']
    
    min_swaps = float('inf')
    
    # Check for '00'
    if len(zeros) >= 2:
        for i in range(len(zeros)):
            for j in range(i + 1, len(zeros)):
                # Calculate swaps needed to bring zeros[i] and zeros[j] to the end
                swaps = zeros[i] + (length - zeros[j] - 1) + (zeros[j] - zeros[i] - 1)
                min_swaps = min(min_swaps, swaps)
    
    # Check for '25', '50', '75'
    for five in fives:
        # Check for '25'
        if five > 0 and n_str[five - 1] in '2':
            swaps = five - 1 + (length - five - 1)
            min_swaps = min(min_swaps, swaps)
        
        # Check for '50'
        for zero in zeros:
            if zero > five:
                swaps = five + (zero - five - 1) + (length - zero - 1)
                min_swaps = min(min_swaps, swaps)
        
        # Check for '75'
        if five > 0 and n_str[five - 1] in '7':
            swaps = five - 1 + (length - five - 1)
            min_swaps = min(min_swaps, swaps)
    
    if min_swaps == float('inf'):
        return -1
    else:
        return min_swaps

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_swaps_to_divisible_by_25(n))