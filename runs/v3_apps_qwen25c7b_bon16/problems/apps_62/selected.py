def determine_winner(n, a):
    min_value = min(a)
    remaining_moves = sum(1 for x in a if x > 0)
    
    # If there's only one element left and it's greater than 0, the current player can always win
    if remaining_moves == 1:
        return "BitLGM" if n % 2 == 1 else "BitAryo"
    
    # If the minimum value is greater than 1, the first player can reduce all elements to 0 in one move
    if min_value > 1:
        return "BitLGM"
    
    # If the number of positive elements is odd, the second player will win if both play optimally
    return "BitAryo" if remaining_moves % 2 == 0 else "BitLGM"

# Example usage
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

print(determine_winner(n, a))