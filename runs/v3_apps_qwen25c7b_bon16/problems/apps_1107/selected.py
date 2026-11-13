def max_juice_drunk(n, moves):
    vasya_turns = [i+1 for i, move in enumerate(moves) if (move == 'b')]
    max_drunk = 0
    
    for turn in vasya_turns:
        if turn < 4:
            continue
        
        previous_moves = moves[turn-3:turn]
        if previous_moves.count('a') == 3 or previous_moves.count('b') == 3:
            max_drunk += 1
    
    return max_drunk

# Example usage
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
moves = data[1]
print(max_juice_drunk(n, moves))