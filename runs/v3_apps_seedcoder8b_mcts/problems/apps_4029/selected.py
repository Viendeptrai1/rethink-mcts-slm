def min_moves_to_divisible_by_25(n: int) -> int:
    s = str(n)
    length = len(s)
    
    # Check if it's already divisible by 25
    if length >= 2 and s[-2:] == '25' or s[-2:] == '50' or s[-2:] == '75' or s[-2:] == '00':
        return 0
    
    # Initialize the minimum moves to a large number
    min_moves = float('inf')
    
    # Try to make the number end with '25', '50', '75', or '00'
    for i in range(length):
        for j in range(i + 1, length):
            # Swap s[i] and s[j]
            swapped = list(s)
            swapped[i], swapped[j] = swapped[j], swapped[i]
            
            # Check if the swapped number ends with '25', '50', '75', or '00'
            if swapped[0] != '0':  # Ensure no leading zero
                swapped_str = ''.join(swapped)
                if swapped_str[-2:] in {'25', '50', '75', '00'}:
                    # Calculate the number of swaps needed
                    swaps_needed = abs(i - j)
                    min_moves = min(min_moves, swaps_needed)
    
    return min_moves if min_moves != float('inf') else -1

# Read input
n = int(input().strip())

# Get the result
result = min_moves_to_divisible_by_25(n)

# Print the result
print(result)