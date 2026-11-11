def max_juice_drunk(n, moves):
    # Initialize the count of glasses of juice Vasya can drink
    max_juice = 0
    
    # Iterate over each possible move Vasya can make on his turns
    for vasya_move in ['a', 'b']:
        # Create a new list of moves where Vasya's moves are replaced
        new_moves = list(moves)
        for i in range(0, len(moves), n):
            if i < len(moves):
                new_moves[i] = vasya_move
        
        # Count the number of times Vasya drinks juice in this scenario
        juice_count = 0
        for i in range(3, len(new_moves)):
            if new_moves[i] == new_moves[i-1] == new_moves[i-2] == new_moves[i-3]:
                juice_count += 1
        
        # Update the maximum juice count
        max_juice = max(max_juice, juice_count)
    
    return max_juice

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
moves = data[1]

# Print the result
print(max_juice_drunk(n, moves))