def min_moves_to_divisible_by_25(n):
    str_n = str(n)
    length = len(str_n)
    
    # Check for immediate impossible cases
    if '0' not in str_n or '5' not in str_n:
        return -1
    
    # Find the positions of '0' and '5'
    zero_positions = [i for i, c in enumerate(str_n) if c == '0']
    five_positions = [i for i, c in enumerate(str_n) if c == '5']
    
    # Check for pairs that can form 00, 25, 50, 75
    possible_pairs = []
    for z in zero_positions:
        for f in five_positions:
            if abs(z - f) == 1:
                possible_pairs.append((z, f))
    
    if not possible_pairs:
        return -1
    
    # Calculate the minimum moves needed
    min_moves = float('inf')
    for z, f in possible_pairs:
        # Calculate moves to bring '0' or '5' to the end
        moves = z + (length - 1 - f) if z < f else f + (length - 1 - z)
        min_moves = min(min_moves, moves)
    
    return min_moves

# Read input
import sys
input = sys.stdin.read
data = input().strip()
n = int(data)

# Output the result
print(min_moves_to_divisible_by_25(n))