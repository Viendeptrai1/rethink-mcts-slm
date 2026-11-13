def min_moves_to_divisible_by_25(n: int) -> int:
    n_str = str(n)
    length = len(n_str)
    
    # Check if the number is already divisible by 25
    if n % 25 == 0:
        return 0
    
    # We need to find the last two digits that form a number divisible by 25
    # The possible pairs are (00, 25, 50, 75)
    target_pairs = ['00', '25', '50', '75']
    
    # We will try to move the last digit to the right position
    for i in range(length - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            # Form the number with the last two digits swapped
            swapped = list(n_str)
            swapped[i], swapped[j] = swapped[j], swapped[i]
            
            # Check if the swapped number is divisible by 25
            if swapped[0] != '0' and ''.join(swapped)[-2:] in target_pairs:
                # Calculate the number of swaps needed
                return (i - j) + (length - 1 - i)
    
    # If no valid swap is found, return -1
    return -1

# Read input
n = int(input().strip())

# Get the result
result = min_moves_to_divisible_by_25(n)

# Print the result
print(result)