def find_final_player(K, N, questions):
    cumulative_time = 0
    current_player = K
    
    for T, Z in questions:
        cumulative_time += T
        if cumulative_time >= 210:
            break
        if Z == 'T':
            current_player = (current_player % 8) + 1
    
    return current_player

# Read input
import sys
input = sys.stdin.read
data = input().split()

K = int(data[0])
N = int(data[1])
questions = [(int(data[2 + 2 * i]), data[3 + 2 * i]) for i in range(N)]

# Find and print the final player
final_player = find_final_player(K, N, questions)
print(final_player)