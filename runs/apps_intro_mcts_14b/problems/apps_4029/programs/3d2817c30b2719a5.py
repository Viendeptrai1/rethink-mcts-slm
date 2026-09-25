import sys

def min_swaps_to_divisible_by_25(n):
    n_str = str(n)
    length = len(n_str)
    
    # Check for '00', '25', '50', '75' from the end
    for i in range(length - 2, -1, -1):
        if n_str[i:i+2] in ['00', '25', '50', '75']:
            # Count the number of swaps needed to bring this pair to the end
            swaps = 0
            for j in range(i, length - 2):
                if n_str[j] != '0':
                    swaps += 1
            return swaps
    
    # If no valid pair is found, check if we can form '00' by swapping
    for i in range(length - 1):
        if n_str[i] == '0':
            for j in range(i + 1, length):
                if n_str[j] in ['0', '2', '5', '7']:
                    swaps = 0
                    for k in range(i, j):
                        if n_str[k] != '0':
                            swaps += 1
                    return swaps + (length - j - 1)
    
    return -1

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_swaps_to_divisible_by_25(n))