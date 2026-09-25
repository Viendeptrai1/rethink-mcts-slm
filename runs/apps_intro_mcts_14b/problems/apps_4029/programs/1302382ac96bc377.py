import sys

def min_swaps_to_divisible_by_25(n):
    str_n = str(n)
    length = len(str_n)
    
    # Find all positions of '0' and '5'
    zero_positions = [i for i, digit in enumerate(str_n) if digit == '0']
    five_positions = [i for i, digit in enumerate(str_n) if digit == '5']
    
    # Check for '00'
    if len(zero_positions) >= 2:
        # Find the closest pair of '0's
        min_swap_count = float('inf')
        for i in range(len(zero_positions)):
            for j in range(i + 1, len(zero_positions)):
                # Calculate swaps needed to bring both '0's to the end
                swaps = zero_positions[i] + (length - 1 - zero_positions[j]) + (zero_positions[j] - zero_positions[i] - 1)
                min_swap_count = min(min_swap_count, swaps)
        if min_swap_count < float('inf'):
            return min_swap_count
    
    # Check for '25', '50', '75'
    for target in ['25', '50', '75']:
        target_digits = list(target)
        target_length = len(target)
        
        # Find the closest occurrence of the target digits
        min_swap_count = float('inf')
        for i in range(length - target_length + 1):
            if str_n[i:i + target_length] == target:
                return 0
            else:
                # Try to form the target by swapping
                swaps = 0
                temp_str = list(str_n)
                for j in range(target_length):
                    if temp_str[i + j] != target_digits[j]:
                        # Find the nearest occurrence of the correct digit
                        for k in range(j, length):
                            if temp_str[k] == target_digits[j]:
                                # Swap adjacent digits to bring the correct digit to the right position
                                for l in range(k, i + j, -1):
                                    temp_str[l], temp_str[l - 1] = temp_str[l - 1], temp_str[l]
                                    swaps += 1
                                break
                        else:
                            # If we can't find the digit, it's impossible
                            break
                else:
                    min_swap_count = min(min_swap_count, swaps)
        
        if min_swap_count < float('inf'):
            return min_swap_count
    
    return -1

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_swaps_to_divisible_by_25(n))