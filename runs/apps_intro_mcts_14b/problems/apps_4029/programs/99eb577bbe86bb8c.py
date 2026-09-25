import sys

def min_swaps_to_divisible_by_25(n):
    n_str = str(n)
    length = len(n_str)
    
    # Check if the number already ends in '00', '25', '50', or '75'
    if n_str.endswith('00') or n_str.endswith('25') or n_str.endswith('50') or n_str.endswith('75'):
        return 0
    
    # Find the positions of '0' and '5' in the string
    zero_positions = [i for i, c in enumerate(n_str) if c == '0']
    five_positions = [i for i, c in enumerate(n_str) if c == '5']
    
    # Try to find a valid pair of digits to swap
    for i in range(length - 1, -1, -1):
        if n_str[i] == '0':
            # Check for '25' ending
            for j in five_positions:
                if j > i:
                    continue
                # Calculate the number of swaps needed
                swaps = i - j + (length - 1 - i)
                # Ensure no leading zeros
                if all(n_str[k] != '0' for k in range(1, j)):
                    return swaps
        elif n_str[i] == '5':
            # Check for '00' or '50' ending
            for j in zero_positions:
                if j > i:
                    continue
                # Calculate the number of swaps needed
                swaps = i - j + (length - 1 - i)
                # Ensure no leading zeros
                if all(n_str[k] != '0' for k in range(1, j)):
                    return swaps
    
    return -1

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_swaps_to_divisible_by_25(n))