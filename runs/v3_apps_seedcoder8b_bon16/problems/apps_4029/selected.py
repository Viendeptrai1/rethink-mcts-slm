def min_moves_to_divisible_by_25(n):
    n_str = str(n)
    
    # Check if the number already ends in '00', '25', '50', or '75'
    if n_str.endswith('00') or n_str.endswith('25') or n_str.endswith('50') or n_str.endswith('75'):
        return 0
    
    # Check if there are no '2' or '5' in the last two positions
    # If there are none, it's impossible to form a number divisible by 25
    if len(n_str) >= 2 and n_str[-1] not in '025' and n_str[-2] not in '25':
        return -1
    
    n_list = list(n_str)
    length = len(n_list)
    
    # Find the rightmost '2' and '5' for a valid combination
    rightmost_2 = -1
    rightmost_5 = -1
    
    for i in range(length - 1, -1, -1):
        if n_list[i] == '2':
            rightmost_2 = i
        elif n_list[i] == '5':
            rightmost_5 = i
            if rightmost_2 != -1:
                break
    
    if rightmost_2 == -1 or rightmost_5 == -1:
        return -1
    
    moves = 0
    
    # Move the rightmost '2' to the second last position if needed
    if rightmost_2 != length - 2:
        if rightmost_2 == length - 1:
            # If '2' is at the end, swap it with the '5' before it
            moves += 1
            n_list[rightmost_2], n_list[rightmost_2 - 1] = n_list[rightmost_2 - 1], n_list[rightmost_2]
        else:
            # Otherwise, move '2' one step to the right until it reaches the second last position
            for i in range(rightmost_2, length - 2):
                n_list[i], n_list[i + 1] = n_list[i + 1], n_list[i]
                moves += 1
    
    # Move the rightmost '5' to the last position if needed
    if rightmost_5 != length - 1:
        for i in range(rightmost_5, length - 1):
            n_list[i], n_list[i + 1] = n_list[i + 1], n_list[i]
            moves += 1
    
    return moves

# Read input
n = int(input().strip())

# Get the result and print it
result = min_moves_to_divisible_by_25(n)
print(result)