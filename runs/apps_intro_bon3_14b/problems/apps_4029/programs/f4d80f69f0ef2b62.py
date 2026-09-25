import sys

def min_moves_to_divisible_by_25(n):
    n_str = str(n)
    length = len(n_str)
    
    # Check for the presence of '00', '25', '50', '75'
    positions = []
    for i in range(length - 1):
        if n_str[i:i+2] in ['00', '25', '50', '75']:
            positions.append(i)
    
    if not positions:
        return -1
    
    min_moves = float('inf')
    
    for pos in positions:
        # Count the number of moves needed to bring the pair to the end
        moves = pos + (length - 2 - pos) - (length - 2 - pos >= 0)
        # Ensure no leading zeros are created
        if all(n_str[i] != '0' or i <= pos for i in range(pos)):
            min_moves = min(min_moves, moves)
    
    return min_moves if min_moves != float('inf') else -1

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_moves_to_divisible_by_25(n))