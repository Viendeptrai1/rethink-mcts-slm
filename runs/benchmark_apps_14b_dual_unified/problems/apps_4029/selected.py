def min_moves_to_divisible_by_25(n):
    str_n = str(n)
    length = len(str_n)
    
    # Check for possible endings that make the number divisible by 25
    possible_endings = ['00', '25', '50', '75']
    
    min_moves = float('inf')
    
    for ending in possible_endings:
        if ending in str_n:
            # Find the last occurrence of the ending
            last_index = str_n.rfind(ending)
            
            # Calculate the number of moves needed to bring this ending to the end
            moves = 0
            for i in range(last_index + 1, length):
                if str_n[i] == '0':
                    # If there's a '0' after the ending, we need to move it to the end
                    # but we can't introduce leading zeros
                    moves += 1
                else:
                    break
            
            # Calculate the total moves to bring the ending to the end
            total_moves = length - (last_index + 1) + moves
            
            # Update the minimum moves
            min_moves = min(min_moves, total_moves)
    
    if min_moves == float('inf'):
        return -1
    else:
        return min_moves

# Read input
import sys
input = sys.stdin.read
data = input().strip()
n = int(data)

# Output the result
print(min_moves_to_divisible_by_25(n))