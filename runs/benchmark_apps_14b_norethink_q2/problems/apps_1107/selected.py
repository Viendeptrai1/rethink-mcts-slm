import sys

def max_juice(n, moves):
    vasya_turns = [i for i in range(len(moves)) if i % n == 0]
    max_drunk = 0
    
    for turn in vasya_turns:
        if turn >= 3:
            if moves[turn] == moves[turn-1] == moves[turn-2] == moves[turn-3]:
                continue
            # Try changing the move to see if it forms a pattern
            original_move = moves[turn]
            new_move = 'a' if original_move == 'b' else 'b'
            temp_moves = list(moves)
            temp_moves[turn] = new_move
            
            # Check if the new move forms a pattern with the previous three
            if temp_moves[turn] == temp_moves[turn-1] == temp_moves[turn-2] == temp_moves[turn-3]:
                max_drunk += 1
    
    return max_drunk

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
moves = data[1]

# Output the result
print(max_juice(n, moves))